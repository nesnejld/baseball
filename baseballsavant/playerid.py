import psycopg2
import os
from util.runcommand import psql, runcommand
import pandas as pd
columns = ["IDPLAYER", "PLAYERNAME", "BIRTHDATE", "FIRSTNAME", "LASTNAME", "TEAM", "LG", "POS", "IDFANGRAPHS", "FANGRAPHSNAME", "MLBID", "MLBNAME", "CBSID", "CBSNAME", "RETROID", "BREFID", "NFBCID", "NFBCNAME", "ESPNID", "ESPNNAME", "KFFLNAME", "DAVENPORTID", "BPID", "YAHOOID",
           "YAHOONAME", "MSTRBLLNAME", "BATS", "THROWS", "FANTPROSNAME", "LASTCOMMAFIRST", "ROTOWIREID", "FANDUELNAME", "FANDUELID", "DRAFTKINGSNAME", "OTTONEUID", "HQID", "RAZZBALLNAME", "FANTRAXID", "FANTRAXNAME", "ROTOWIRENAME", "ALLPOS", "NFBCLASTFIRST", "ACTIVE", "UNDERDOG", "RAZZBALLID"]


p = psql()
if False:
    try:
        sql = 'DROP TABLE playerid;'
        p.runsql(sql)
    except:
        p.conn.close()
        p = psql()
        pass
    prefix = ''
    sql = 'CREATE TABLE playerid ('
    for c in columns:
        t = 'VARCHAR'
        if c in ['MLBID']:
            t = 'INT'
        sql += prefix+c+' ' + t
        prefix = ',\n'
    sql += ');'
    print(sql)
    result = p.runsql(sql)
    sql = f"""\copy playerid from '{os.path.abspath(os.path.join("data","SFBB Player ID Map - PLAYERIDMAP.csv"))}' WITH DELIMITER ',' CSV HEADER;"""
    result = runcommand(f"""psql -d baseball -c "{sql}" """)
if True:
    engine = psycopg2.connect(
        "dbname='baseball' user='djensen' host='127.0.0.1' port='5432' password='passw0rd'")
    df = pd.read_sql('select * from playerid', con=engine)
    pass
pass
