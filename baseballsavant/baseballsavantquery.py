import json
import requests
import subprocess


def runcommand(command, verbose=True):
    result = subprocess.run(["bash", "-c", command], capture_output=True)
    commandoutput = result.stdout.decode()
    commanderror = result.stderr.decode()
    if verbose:
        print(commandoutput)
    return commandoutput, commanderror


def curl(url, outfile):
    command = f"curl -o {outfile} '{url}'"
    # print(command)
    out, err = runcommand(command)


url = 'https://baseballsavant.mlb.com/statcast_search/csv?type=details&all=true&hfPT=FF&game_date_gt=2024-04-01&game_date_lt=2024-04-01&hfGT=R|PO|S&min_pitches=0&min_results=0&group_by=name&sort_order=desc&min_abs=0&'
url = 'https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfGT=R|PO|S|&type=details&player_type=&game_date_gt=2024-04-01&game_date_lt=2024-04-01&min_pitches=0&min_results=0&group_by=name&sort_order=desc&min_abs=0'
url = 'https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfGT=R|PO|S|&type=details&player_type=&game_date_gt=2024-04-01&game_date_lt=2024-04-01&min_pitches=0&min_results=0&min_abs=0'
url = 'https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfGT=R|PO|S|&type=details&player_type=&game_date_gt=2024-04-01&game_date_lt=2024-04-01'
url = 'https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details&hfGT=R|PO|S|&player_type=&game_date_gt=2024-04-01&game_date_lt=2024-04-01'
url = 'https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details&hfGT=R|PO|S|&game_date_gt=2024-04-01&game_date_lt=2024-04-01'
url = 'https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details&game_date_gt=2024-04-01&game_date_lt=2024-04-01'
url = 'https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details&game_date_gt=2024-04-01&game_date_lt=2024-04-01&player_type=batter|pitcher&rfPT=FF'
url = "https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details&hfPT=FF%7CCH%7C&hfAB=&hfGT=R%7C&hfPR=&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2024%7C&hfSit=&player_type=pitcher&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfMo=&hfTeam=&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=&hfFlag=&metric_1=&group_by=name&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc"
url = "https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details&hfPT=&hfAB=&hfGT=R%7C&hfPR=&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2024%7C&hfSit=&player_type=pitcher&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfMo=&hfTeam=&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=&hfFlag=&metric_1=&group_by=name&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc"
url = "https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details&hfPT=&hfAB=&hfGT=&hfPR=&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2024%7C&hfSit=&player_type=pitcher&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfMo=&hfTeam=&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=&hfFlag=&metric_1=&group_by=name&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc"
url = "https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details&hfSea=2024%7C&player_type=pitcher&group_by=name&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc"
url = "https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details"
values = {
    "hfSea": "2024",
    "player_type": "pitcher",
    "group_by": "name",
    "min_pitches": "0",
    "min_results": "0",
    "min_pas": "0",
    "sort_col": "pitches",
    "player_event_sort": "api_p_release_speed",
    "sort_order": "desc"
}
for key, value in values.items():
    url += f"&{key}={value}"
# results"
parameters = json.load(open('baseballsavant.json'))
for k in values:
    if k in parameters:
        print(k)
        choice = parameters[k]['value']['choice']
        for c in choice:
            print(f"\t{c}")
        pass
    else:
        pass
print(url)
outfile = 'result3.csv'
curl(url, outfile)
pass
