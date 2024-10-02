#!/usr/bin/env python
# .//pybaseball/league_batting_stats.py:    url = "http://www.baseball-reference.com/leagues/daily.cgi?user_team=&bust_cache=&type=b&lastndays=7&dates=fromandto&fromandto={}.{}&level=mlb&franch=&stat=&stat_value=0".format(start_dt, end_dt)
# .//pybaseball/league_pitching_stats.py:    url = "http://www.baseball-reference.com/leagues/daily.cgi?user_team=&bust_cache=&type=p&lastndays=7&dates=fromandto&fromandto={}.{}&level=mlb&franch=&stat=&stat_value=0".format(start_dt, end_dt)
# .//pybaseball/team_game_logs.py:_URL = "https://www.baseball-reference.com/teams/tgl.cgi?team={}&t={}&year={}"
import requests
import json
import sys
from lxml import etree
from util.runcommand import canonicalize
import traceback
import pandas
import os
import stat

import logging


def where():
    try:
        raise Exception
    except:
        stack = traceback.extract_stack()
        return {"filename": stack[-2].filename, "lineno": stack[-2].lineno}
        pass


class BaseballReference:
    '''
    The BaseballReference object represent a connection to baseballref and an html scraper. 
    So far, only the dauly.cgi is invoked.
    '''

    def getdtype(self, value):
        return str

    def __init__(self,
                 fileprefix: str = 'xxxx',
                 debug: bool = False,
                 urlprefix: str = 'https://www.baseball-reference.com',
                 urlpattern: str = "/leagues/daily.cgi?user_team=&bust_cache=&type={type}&lastndays=7&dates=fromandto&fromandto={start_dt}.{end_dt}&level={level}&franch={franch}&stat=&stat_value=0",
                 csvfile: str = None,
                 loglevel='WARN'
                 ):
        self.fileprefix = fileprefix
        self.debug = debug if isinstance(debug, bool) else debug == 'true'
        self.urlprefix = urlprefix
        self.urlpattern = urlpattern
        self.csvfile = csvfile
        format = '%(asctime)s %(levelname)s:%(name)s %(lineno)d :%(message)s'
        # setting level here doe not appear to work
        logging.basicConfig(format=format)
        self.logger = logging.getLogger('net.homeip.dljensen.getdata')
        self.logger.setLevel(getattr(logging, loglevel))
        self.count = 0
        self.xml_tree = None
        return

    def getdataframe(self, args):
        data = self.getdata(args)
        columns = list(map(lambda d: d["key"], data['columns']))
        rows = []
        for i, r in enumerate(data['rows']):
            row = []
            for j, c in enumerate(columns):
                if c == 'ranker':
                    row.append(i)
                    continue
                rr = r[j-1]
                value = None
                for f in ['data', 'text', 'csk', 'href']:
                    if f in rr:
                        value = rr[f]
                        break
                try:
                    value = int(value)
                except Exception as e:
                    try:
                        value = float(value)
                    except Exception as e:
                        pass
                row.append(value)
            rows.append(row)
        return pandas.DataFrame(columns=columns, data=rows)

    def getdata(self, args: dict) -> dict:
        logger = self.logger
        url = self.urlprefix+self.urlpattern.format(**args)
        logger.debug(url)
        result = requests.get(url)
        html = result.content.decode()
        if self.debug:
            with open(f"{self.fileprefix}.html", "w") as f:
                f.write(html)
        parser = etree.HTMLParser()
        xml_tree = etree.fromstring(html, parser)
        self.xml_tree = xml_tree
        type = 'b'  # batter
        xtable = xml_tree.find(".//table")
        etree.indent(xml_tree, space="  ")
        sxml_tree = etree.tostring(xml_tree).decode('utf-8')
        if self.debug:
            # tree.write(f"{self.fileprefix}.xml")
            # ET.ElementTree(table).write(f"{self.fileprefix}.table.xml")
            etree.ElementTree(xml_tree).write(
                f"{self.fileprefix}.xml")
            etree.ElementTree(xtable).write(f"{self.fileprefix}.table.xml")
        th = xml_tree.findall(".//table//thead/tr/th")

        data = {'columns': [], 'rows': [], "url": url}
        fields = {'data-stat': 'key',  'csk': 'csk',
                  'title': 'title', 'data': 'data', }
        for t in th:
            j = {}
            for f in fields:
                self.addtojson(t, f, j, fields[f])
            data['columns'].append(j)
            logger.debug(
                f"label:{t.attrib['aria-label']}; stat: {t.attrib['data-stat']}")
        rows = xml_tree.findall(".//table//tbody/tr")
        for r in rows:
            tds = r.findall('./td')
            jj = []
            for td in tds:
                j = {}
                if 'data' not in td.attrib and td.text is not None and len(canonicalize(td.text)) > 0:
                    td.attrib['data'] = canonicalize(td.text)
                for f in fields:
                    self.addtojson(td, f, j, fields[f])
                a = td.find('./a')
                if a is not None:
                    j['href'] = a.attrib['href']
                    self.addtojson(a, 'title', j)
                jj.append(j)
            if len(jj) > 0:
                data['rows'].append(jj)
            pass
        # xoption = toptions.xpath('contains("fieldset")')
        # data['options'] = options
        return data

    def getAllOptions(self) -> object:
        logger = self.logger
        url = self.urlprefix+self.urlpattern
        logger.debug(url)
        html = requests.get(url).content.decode()
        xml_tree = etree.fromstring(html,  etree.HTMLParser())
        j = {}
        unknown = 0
        xoptions = xml_tree.xpath(
            './/div[@id="content"]//div[contains(concat(" ",@class," ")," options ") or contains(concat(" ",@class," ")," criteria ")]')
        for xoption in xoptions:
            toption = etree.ElementTree(xoption)
            logger.debug(self.treetostring(toption))
            for s in xoption.xpath('.//div[contains(concat(" ",@class," ")," fieldset ") and not(contains(concat(" ",@class," "),"final"))]'):
                if 'data-type' in s.attrib:
                    if s.attrib['data-type'] == 'hidden':
                        continue
                if len(s.xpath('./div[concat(" ",@class," ")=" formlabel "]')) > 0:
                    option = canonicalize(canonicalize(
                        s.xpath('./div[concat(" ",@class," ")=" formlabel "]')[0].text))
                    logger.info(option)
                    pass
                else:
                    option = s.xpath(
                        './/div[concat(" ",@class," ")=" choicefield "]/input')[0]
                    if option is not None:
                        option = option.attrib['name']
                    else:
                        option = f"<unknown_{unknown}>"
                        unknown += 1
                if 'data-type' in s.attrib:
                    if s.attrib['data-type'] == 'dropdown':
                        # logger.info(treetostring(s))
                        j[option] = {'values': self.getchoices(
                            s), 'attributes': None}
                        pass
                    elif s.attrib['data-type'] == 'radio':
                        j[option] = {'values': self.getchoices(
                            s), 'attributes': None}
                        pass
                    else:
                        j[option] = {'values': self.getchoices(
                            s), 'attributes': None}
                    pass
                else:
                    logger.debug(self.treetostring(s))
                    j[option] = {'values': [], 'attributes': {}}
                    l = set(s.xpath('.//div[contains(concat(" ",@class," ")," formfield ")]'))-set(
                        s.xpath(""".//div[contains(concat(' ',@class,' ')," choice ")]//div[contains(concat(" ",@class," ")," formfield ")]"""))
                    for f in l:
                        logger.debug(self.treetostring(f))
                        if 'number' in f.attrib['class']:
                            pass
                        else:
                            j[option]['values'].extend(self.getchoices(f))
                            j[option]['attributes']['textinput'] = len(
                                s.xpath('.//div[contains(concat(" ",@class," "),"number")]')) > 0
                    pass
        return j

    def buildtable(self, data):
        if self.debug:
            json.dump(data, open(f'{self.fileprefix}.json', 'w'),  indent=2)
        # with sys.stdout as f:
        self.csvfile = self.csvfile if self.csvfile is not None else f"{self.fileprefix}.csv"
        try:
            os.remove(self.csvfile)
        except Exception as e:
            pass
        with open(self.csvfile, "w") as f:
            prefix = ''
            for j in data['columns']:
                f.write(prefix)
                f.write(j['key'])
                prefix = ','
            f.write('\n')
            for i, r in enumerate(data['rows']):
                if len(r) == 0:
                    continue
                f.write(str(i+1))
                for c in r:
                    f.write(prefix)
                    if 'csk' in c:
                        f.write(f"""\"{c['csk']}\"""")
                    elif 'data' in c:
                        if c['key'] in ['level', 'team_ID', 'date_game', 'homeORvis', 'opp_ID']:
                            f.write(f"""\"{c['data']}\"""")
                        else:
                            f.write(c['data'])
                    elif 'href' in c:
                        f.write(f"""\"{self.urlprefix}{c['href']}\"""")
                    else:
                        continue
                f.write('\n')
        os.chmod(
            self.csvfile,
            stat.S_IRUSR |
            stat.S_IWUSR |
            stat.S_IRGRP |
            stat.S_IWGRP |
            stat.S_IROTH |
            stat.S_IWOTH
        )

    def printd(self, message):
        logger = self.logger
        if self.debug:
            logger.info(message)

    def treetostring(self, xml_tree):
        etree.indent(xml_tree, space="  ")
        return etree.tostring(xml_tree).decode('utf-8')

    def getoptions(self, s):
        j = []
        logger = self.logger
        xpath = ".//option"
        if s.find(xpath) is not None:
            for o in s.findall(xpath):
                option = {'label': canonicalize(o.text),
                          'value': o.attrib['value']}
                option['disabled'] = 'disabled' in o.attrib
                if self.debug:
                    option.update({"where": where(),
                                   "count": self.count})
                j.append(option)
                self.count += 1
        if len(j) > 0:
            logger.info(json.dumps(j, indent=2))
        return j

    def getchoices(self, s):
        j = []
        logger = self.logger
        choices = s.xpath(
            './/div[concat(" ",@class," ")=" choicefield "]')
        # choices += s.xpath('.//div[contains(concat(" ",@class," "), "choicefield ")]')
        if (len(choices)) > 0:
            for choice in choices:
                choiceoption = choice.xpath(
                    '../div[concat(" ",@class," ")=" choiceoption "]')[0]
                if choiceoption is not None:
                    label = canonicalize(choiceoption.text)
                else:
                    label = None
                    continue
                value = choice.find(
                    './input').attrib['value']
                selected = 'selected' in choice.xpath(
                    './ancestor::div')[-1].attrib['class'].split(" ")
                parent = choice.xpath('..')[0]
                option = {'label': label, 'value': value,
                          'choices': self.getoptions(parent), 'selected': selected}
                option.update({"textinput": len(choice.xpath(
                    '../div[concat(" ",@class," ")=" choiceoption "]//input[@type="text"]')) > 0})
                if self.debug:
                    option.update({'where': where(),
                                   "count": self.count})
                j.append(option)
                self.count += 1
                pass
        else:
            options = self.getoptions(s)
            for option in options:
                option['choices'] = []
                # option.update({"textinput": len(choice.xpath(
                #     '../div[concat(" ",@class," ")=" choiceoption "]//input[@type="text"]')) > 0})
                option.update({"textinput": False})
            j.extend(options)
            pass
        if (len(j) > 0):
            logger.info(json.dumps(j, indent=2))
        return j

    def addtojson(self, element, field, json, key=None):
        if field in element.attrib:
            if key == 'csk':
                json['text'] = element.xpath('a')[0].text
            json[key if key is not None else field] = element.attrib[field]
        return json

    pass
