#!/usr/bin/env python
# .//pybaseball/league_batting_stats.py:    url = "http://www.baseball-reference.com/leagues/daily.cgi?user_team=&bust_cache=&type=b&lastndays=7&dates=fromandto&fromandto={}.{}&level=mlb&franch=&stat=&stat_value=0".format(start_dt, end_dt)
# .//pybaseball/league_pitching_stats.py:    url = "http://www.baseball-reference.com/leagues/daily.cgi?user_team=&bust_cache=&type=p&lastndays=7&dates=fromandto&fromandto={}.{}&level=mlb&franch=&stat=&stat_value=0".format(start_dt, end_dt)
# .//pybaseball/team_game_logs.py:_URL = "https://www.baseball-reference.com/teams/tgl.cgi?team={}&t={}&year={}"
import requests
from util.runcommand import HTML2XMLParser
import json
import xml.etree.ElementTree as ET
import sys
import urllib3


class BaseballReference:

    def __init__(self,
                 fileprefix='xxxx',
                 debug=False,
                 urlprefix='https://www.baseball-reference.com',
                 urlpattern="/leagues/daily.cgi?user_team=&bust_cache=&type={type}&lastndays=7&dates=fromandto&fromandto={start_dt}.{end_dt}&level={level}&franch={franch}&stat=&stat_value=0",
                 csvfile=None
                 ):
        self.fileprefix = fileprefix
        self.debug = debug
        self.urlprefix = urlprefix
        self.urlpattern = urlpattern
        self.csvfile = csvfile
        return

    def getdata(self, args):
        url = self.urlprefix+self.urlpattern.format(**args)
        if self.debug:
            self.printd(url)
        result = requests.get(url)
        html = result.content.decode()
        if self.debug:
            with open(f"{self.fileprefix}.html", "w") as f:
                f.write(html)
        newtree = ET.ElementTree()
        newtree._setroot(ET.Element('root'))
        parser = HTML2XMLParser(newtree.getroot())
        parser.feed(html)
        tree = newtree
        root = tree.getroot()
        typ = 'b'  # batter
        franch = list(map(lambda o:
                          {o.attrib['value']: o.attrib['data']}, tree.findall(
                              ".//select[@id='franch']/option")))
        level = list(map(lambda o:
                         {o.attrib['value']: o.attrib['data']}, tree.findall(
                             ".//select[@id='level']/option")))
        stat = list(map(lambda o:
                        {o.attrib['value']: o.attrib['data']}, tree.findall(
                            ".//select[@id='stat']/option")))

        table = tree.find(".//table")
        ET.indent(tree, space='  ', level=0)
        if self.debug:
            tree.write(f"{self.fileprefix}.xml")
            ET.ElementTree(table).write(f"{self.fileprefix}.table.xml")
        th = tree.findall(".//table//thead/tr/th")

        def addtojson(element, field, json, key=None):
            if field in element.attrib:
                json[key if key is not None else field] = element.attrib[field]
            return json

        data = {'columns': [], 'rows': [], "url": url}
        fields = {'data': 'data', 'data-stat': 'key', 'csk': 'csk',
                  'title': 'title'}
        for t in th:
            j = {}
            for f in fields:
                addtojson(t, f, j, fields[f])
            data['columns'].append(j)
            if self.debug:
                print(
                    f"label:{t.attrib['aria-label']}; stat: {t.attrib['data-stat']}")
        rows = tree.findall(".//table//tbody/tr")
        for r in rows:
            tds = r.findall('./td')
            jj = []
            for td in tds:
                j = {}
                for f in fields:
                    addtojson(td, f, j, fields[f])
                a = td.find('./a')
                if a is not None:
                    j['href'] = a.attrib['href']
                    addtojson(a, 'title', j)
                jj.append(j)
            data['rows'].append(jj)
            pass
        if self.debug:
            json.dump(data, open(f'{self.fileprefix}.json', 'w'),  indent=2)
        # with sys.stdout as f:
        self.csvfile = self.csvfile if self.csvfile is not None else f"{self.fileprefix}.csv"
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
        return json.dumps(data,  indent=2)

    def printd(self, message):
        if self.debug:
            print(message)


if __name__ == '__main__':
    args = {"franch":  'ANY',
            "level": 'mlb',
            "end_dt": '2024-08-29',
            "start_dt": '2024-04-01'
            }
    args = {"franch":  'ANY',
            "level": 'mlb',
            "end_dt": '2024-04-01',
            "start_dt": '2024-04-01',
            "type": 'b'
            }
    options = {}
    if len(sys.argv) > 1:
        args = json.loads(sys.argv[1])
    if len(sys.argv) > 2:
        options = json.loads(sys.argv[2])
    result = BaseballReference(
        fileprefix='yyyy', debug=False, **options).getdata(args)
    print(result)
pass
