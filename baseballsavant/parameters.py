#!/usr/bin/env python
import sys
import xml.etree.ElementTree as ET
import json
from util.runcommand import runcommand
import os
import re
from util.runcommand import HTML2XMLParser
# import requests
# https://baseballsavant.mlb.com/statcast_search
#
# uses the baseballsavent wbesite to infer query structure - can't find documentation
# inferred api is encoded in baseballsavant.json
#
# Doesn't work - fileds are populated using javascritp after page loadings
#
# Copy the html from loaded page using the browser's inspector
#
# if not os.path.exists('statcast_search.html'):
#     html = requests.get(
#         'https://baseballsavant.mlb.com/statcast_search').content.decode('utf-8')
#     with open("statcast_search.0.html", "w") as f:
#         f.write(html)
#     # html is not correct - fixes
#     lines = html.split('\n')
#     for i, line in enumerate(lines):
#         if re.match('.*optgroup.*Lineup', line):
#             lines[i] = line + '>'
#             print(i)
#             continue

#     html = '\n'.join(lines)
#     with open("statcast_search.html", "w") as f:
#         f.write(html)
# else:
#     with open('newtree.html', 'r') as f:
#         html = f.read()

with open('newtree.html', 'r') as f:
    html = f.read()
if not os.path.exists('newtree.xml'):
    newtree = ET.ElementTree()
    newtree._setroot(ET.Element('root'))

    parser = HTML2XMLParser(newtree.getroot())
    parser.feed(html)

    def traverse(node, file=sys.stderr, depth=0):
        for child in node:
            prefix = ""
            for i in range(depth):
                prefix += " "
            tagtext = child.tag
            for a, c in child.attrib.items():
                tagtext += f""" {a}="{c}" """
                pass
            file.write(prefix+'<'+tagtext+'>\n')
            traverse(child, file, depth+1)
            file.write(prefix+'</'+child.tag+'>\n')
            pass

    # with open("newtree.xml", "w") as f:
    #     traverse(newtree.getroot(), file=f)
    ET.indent(newtree, ' ', level=0)
    newtree.write('newtree.xml')
else:
    newtree = ET.parse('newtree.xml')


def canonicalize(text):
    lines = text.split('\n')
    return ' '.join(list(map(lambda l: l.strip(), lines))).strip()


parameters = {}
if False:
    tree = ET.parse('baseballsavant.xml')
    root = tree.getroot()
    parameters = {}
    forms = tree.findall(".//div[@class='row']/div[@class='form-group']")
    for row in forms:
        container = row.findall(".//div[@class='vw-container']")
        if len(container) > 0:
            for child in container:
                field = child.find(".//input[@type='hidden']")
                shortid = child.find(
                    './/div[@data-short-id]').attrib['data-short-id']
                fieldid = field.attrib['id']
                parent = child.find(".//input[@type='hidden']/..")
                label = child.find('./div/span[@class="overlay-title"]').text
                print(f"""{child.attrib['id']} {fieldid}""")
                value = {}
                parameters[fieldid] = {}
                parameters[fieldid]['value'] = value
                parameters[fieldid]['shortid'] = shortid
                parameters[fieldid]['label'] = label
                if fieldid == 'hfPT':
                    span = parent.find('./span')
                    value['description'] = span.text
                    values = parent.findall(".//label")
                    div = parent.find(".//label/..")
                    value['multiple'] = div.attrib['class'].find(
                        'multi-select-input-wrapper') != -1
                    choice = {}
                    value['choice'] = choice
                    values = list(filter(lambda e: e.attrib['class'].find('search-pitch-label') != -1, parent.findall(
                        ".//span")))
                    for v in values:
                        # p = parents[v]
                        # print(v.text)
                        # print(v.tail.strip())
                        choice[v.text] = canonicalize(v.tail)
                    print(value)
                    print('\n')
                    pass
                elif fieldid in ['hfAB',
                                 'hfGT',
                                 'hfPR',
                                 'hfZ',
                                 'hfStadium',
                                 'hfBBL',
                                 'hfNewZones',
                                 'hfPull',
                                 'hfC',
                                 'hfSea',
                                 'hfSit',
                                 'hfOuts',
                                 'hfOpponent',
                                 'hfSA',
                                 'hfMo',
                                 'hfTeam',
                                 'hfRO',
                                 'hfInfield',
                                 'hfOutfield',
                                 'hfInn',
                                 'hfBBT',
                                 'hfFlag'
                                 ]:
                    span = parent.find('./span')
                    value['description'] = span.text
                    values = parent.findall(".//label")
                    div = parent.find(".//label/..")
                    value['multiple'] = div.attrib['class'].find(
                        'multi-select-input-wrapper') != -1
                    choice = {}
                    value['choice'] = choice
                    for v in values:
                        # p = parents[v]
                        # print(v.text)
                        # print(v.tail.strip())
                        if 'id' in v.attrib:
                            key = v.attrib['id'][len(f"lbl_{shortid}'"):]
                            choice[key] = v.text
                    print(value)
                    print('\n')
                    pass
                else:
                    # print(fieldid)
                    pass
        else:
            label = row.find('./label')
            if label is None:
                continue
            label = label.text
            if label in ['Game Date >=', 'Game Date <=']:
                continue
            print(label)
            fieldid = row.find('.//select').attrib['id']
            values = row.findall('.//option')
            value = {}
            choice = {}
            parameters[fieldid] = {}
            parameters[fieldid]['value'] = value
            parameters[fieldid]['shortid'] = label
            parameters[fieldid]['label'] = label
            value['multiple'] = False
            value['choice'] = choice
            for v in values:
                # p = parents[v]
                # print(v.text)
                # print(v.tail.strip())
                if 'value' in v.attrib:
                    key = v.attrib['value']
                    if key == '':
                        continue
                    choice[key] = canonicalize(v.text)
            print(value)
            print('\n')
        pass
if True:
    tree = newtree
    root = tree.getroot()
    forms = tree.findall(".//div[@class='row']/div[@class='form-group']")
    for row in forms:
        container = row.findall(".//div[@class='vw-container']")
        if len(container) > 0:
            for child in container:
                field = child.find(".//input[@type='hidden']")
                shortid = child.find(
                    './/div[@data-short-id]').attrib['data-short-id']
                fieldid = field.attrib['id']
                parent = child.find(".//input[@type='hidden']/..")
                label = child.find(
                    './div/span[@class="overlay-title"]').attrib['data']
                print(f"""{child.attrib['id']} {fieldid}""")
                value = {}
                parameters[fieldid] = {}
                parameters[fieldid]['value'] = value
                parameters[fieldid]['shortid'] = shortid
                parameters[fieldid]['label'] = label
                if fieldid == 'hfPT':
                    span = parent.find('./span')
                    value['description'] = span.attrib['data']
                    values = parent.findall(".//label")
                    div = parent.find(".//label/..")
                    value['multiple'] = div.attrib['class'].find(
                        'multi-select-input-wrapper') != -1
                    choice = {}
                    value['choice'] = choice
                    values = list(filter(lambda e: e.find('./span').attrib['class'].find('search-pitch-label') != -1, parent.findall(
                        ".//span/..")))
                    for v in values:
                        choice[v.find('./span').attrib['data']
                               ] = canonicalize(v.attrib['data'])
                    print(value)
                    print('\n')
                    pass
                elif fieldid in ['hfAB',
                                 'hfGT',
                                 'hfPR',
                                 'hfZ',
                                 'hfStadium',
                                 'hfBBL',
                                 'hfNewZones',
                                 'hfPull',
                                 'hfC',
                                 'hfSea',
                                 'hfSit',
                                 'hfOuts',
                                 'hfOpponent',
                                 'hfSA',
                                 'hfMo',
                                 'hfTeam',
                                 'hfRO',
                                 'hfInfield',
                                 'hfOutfield',
                                 'hfInn',
                                 'hfBBT',
                                 'hfFlag'
                                 ]:
                    span = parent.find('./span')
                    value['description'] = span.attrib['data']
                    values = parent.findall(".//label")
                    div = parent.find(".//label/..")
                    value['multiple'] = div.attrib['class'].find(
                        'multi-select-input-wrapper') != -1
                    choice = {}
                    value['choice'] = choice
                    for v in values:
                        if 'id' in v.attrib:
                            key = v.attrib['id'][len(f"lbl_{shortid}'"):]
                            choice[key] = canonicalize(v.attrib['data'])
                    print(value)
                    print('\n')
                    pass
                else:
                    # print(fieldid)
                    pass
        else:
            label = row.find('./label')
            if label is None:
                continue
            label = label.attrib['data']
            if label in ['Game Date >=', 'Game Date <=']:
                continue
            print(label)
            fieldid = row.find('.//select').attrib['id']
            values = row.findall('.//option')
            value = {}
            choice = {}
            parameters[fieldid] = {}
            parameters[fieldid]['value'] = value
            parameters[fieldid]['shortid'] = label
            parameters[fieldid]['label'] = label
            value['multiple'] = False
            value['choice'] = choice
            for v in values:
                if 'value' in v.attrib:
                    key = v.attrib['value']
                    if key == '':
                        continue
                    choice[key] = canonicalize(v.attrib['data'])
            print(value)
            print('\n')
        pass
json.dump(parameters, open('baseballsavant.json', 'w'), indent=2)
