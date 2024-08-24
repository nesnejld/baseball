from pybaseball import statcast
from pybaseball.playerid_lookup import get_lookup_table
from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup
import requests
import xml.etree.ElementTree as ET
import json
# https://baseballsavant.mlb.com/statcast_search
tree = ET.parse('temp.xml')
root = tree.getroot()
esult = tree.find(".//div[@id='vwPitchTypes']")
parents = {}


def addparent(parent, node):
    parents[node] = parent
    for child in node:
        addparent(node, child)


addparent(None, root)
# result = tree.find(".//neighbor")
# result = result.find("..")
parameters = {}
result = tree.find(".//div[@id='vwPitchTypes']")
result = tree.findall(".//div[@class='vw-container']")
for child in result:
    field = child.find(".//input[@type='hidden']")
    shortid = child.find('.//div[@data-short-id]').attrib['data-short-id']
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
        values = list(filter(lambda e: e.attrib['class'].find('search-pitch-label') != -1, parent.findall(
            ".//span")))
        for v in values:
            # p = parents[v]
            # print(v.text)
            # print(v.tail.strip())
            value[v.text] = v.tail.strip()
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
        print(span.text)
        values = parent.findall(".//label")
        for v in values:
            # p = parents[v]
            # print(v.text)
            # print(v.tail.strip())
            if 'id' in v.attrib:
                value[v.text] = v.attrib['id']
        print(value)
        print('\n')
        pass
    else:
        # print(fieldid)
        pass
json.dump(parameters, open('parameters.json', 'w'))
result = requests.get(
    'http://github.com/chadwickbureau/register/tree/master/data/links.csv')
# Find Clayton Kershaw's player id
# from pybaseball import  get_lookup_table
# data=statcast(start_dt="2016-01-01", end_dt="2024-08-01")

# table = get_lookup_table()
# table=list(filter(lambda row :
# row['key_mlbam'] == 47732
# , table))
player = playerid_lookup('kershaw', 'clayton')
# His MLBAM ID is 477132, so we feed that as the player_id argument to the following function
id = player['key_mlbam'][0]
kershaw_stats = statcast_pitcher('2017-06-01', '2024-07-01', id)
kershaw_stats.groupby("pitch_type").release_speed.agg("mean")
print(kershaw_stats)
pass
