#!/usr/bin/env python
import datetime
import sys
import subprocess
import os
import urllib.parse
from util.runcommand import runcommand
import json
outdir = '/Volumes/Swap/data'
#
# start date argument 'yyyy-mm-dd'
# end date argument 'yyyy-mm-dd'
#
startyear = 2016
startmonth = 6
startday = 9
endyear = startyear
endmonth = startmonth
endday = startday


def setdates(start, end):
    global startyear, startmonth, startday, endyear, endmonth, endday
    [startyear, startmonth, startday] = map(
        lambda s: int(s), start.split("-"))
    endyear = startyear
    endmonth = startmonth
    endday = startday
    if end is not None:
        [endyear, endmonth, endday] = map(
            lambda s: int(s), end.split("-"))
    s = datetime.date(startyear, startmonth, startday)
    e = datetime.date(endyear, endmonth, endday)
    e = e if e < datetime.datetime.now().date() else datetime.datetime.now().date()
    return s, e


fields = json.load(open("queryfields.json"))
# fields = {
#     "all": "true",
#     "hfPT": "",  # pitch type FF
#     "hfPR": "",  # pitch result
#     "hfAB": "",
#     "hfBBT": "",
#     "hfZ": "",
#     "stadium": "",
#     "hfBBL": "",
#     "hfNewZones": "",
#     "hfGT": "",  # urllib.parse.unquote("R|PO|S|"),
#     "hfSea": "",
#     "hfSit": "",
#     "player_type": "{player_type}",
#     "hfOuts": "",
#     "opponent": "",
#     "pitcher_throws": "",
#     "batter_stands": "",
#     "hfSA": "",
#     "game_date_gt": "{startdate}",
#     "game_date_lt": "{enddate}",
#     "team": "",
#     "position": "",
#     "hfRO": "",
#     "home_road": "",
#     "hfFlag": "",
#     "metric_1": "",
#     "hfInn": "",
#     "min_pitches": "0",
#     "min_results": "0",
#     "group_by": "name",
#     # "sort_col": "pitches",
#     # "player_event_sort": "h_launch_speed",
#     "sort_order": "desc",
#     "min_abs": "0",
#     "type": "details"
# }
print(fields)
query_string = ""
prefix = ''
for f in fields:
    if fields[f] == '':
        continue
    query_string += f"""{prefix}{f}={fields[f]}"""
    prefix = '&'
s, e = setdates(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
if len(sys.argv) > 3:
    outdir = sys.argv[3]
while (s <= e):
    startdate = str(s)
    enddate = startdate
    s += datetime.timedelta(days=1)
    qs = query_string.format(
        startdate=startdate, enddate=enddate, player_type='')
    outfile = os.path.abspath(os.path.join(outdir, f"data.{startdate}.csv"))
    if os.path.exists(outfile):
        print(f"Skip {startdate}")
        continue
    print(f"getting data for {startdate}")
    url = f"https://baseballsavant.mlb.com/statcast_search/csv?{qs}"
    # hfPT=hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7CPO%7CS%7C=&hfSea=&hfSit=&player_type=pitcher&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt={startdate}&game_date_lt={enddate}&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=h_launch_speed&sort_order=desc&min_abs=0&type=details"
    # url = f"https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7CPO%7CS%7C=&hfSea=&hfSit=&player_type=pitcher&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt={startdate}&game_date_lt={enddate}&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=h_launch_speed&sort_order=desc&min_abs=0&type=details"
    command = f"curl -o {outfile} '{url}'"
    # print(command)
    out, err = runcommand(command)
    print(err)
    pass
