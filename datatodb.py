#!/usr/bin/env python
import os
import re
import pandas
import sys
#
# Using the data downloaded, this file creates two files - create.sql and data.sql
# which can be used to create the baseball database and load it.
#
indir = "/Volumes/Swap/data"

if len(sys.argv) > 1:
    indir = sys.argv[1]
files = list(filter(lambda f: not re.match(
    'data.*csv', f) is None, os.listdir(indir)))
for f in files:
    print(f)
    df = pandas.read_csv(os.path.join(indir, f))
    if df.shape[0] == 0:
        continue
    sql = 'CREATE TABLE baseballdata ( '
    prefix = ''
    for c, t in zip(df.columns, df.dtypes):
        if c in ['pitch_type', 'sv_id', 'pitch_name', 'if_fielding_alignment', 'of_fielding_alignment']:
            tt = 'VARCHAR'
        elif t == 'float64':
            tt = "DOUBLE PRECISION"
        elif t == 'int64':
            tt = 'INT'
        elif t == 'object':
            tt = 'VARCHAR'
        else:
            tt = t
        sql += f"{prefix} \"{c}\" {tt}"
        prefix = ',\n'
        # print(f"{c} {t}")
    sql += ')'
    print(sql)
    with open("create.sql", "w") as f:
        f.write(sql)
    break
    pass
with open("data.sql", "w") as f:
    for file in files:
        # sql = f"""COPY baseballdata FROM '{os.path.join("/Volumes/Swap/data",file)}' WITH (FORMAT csv);"""
        if os.path.getsize(os.path.join(indir, file)) < 2000:
            continue  # NO DATA
        sql = f"""\copy baseballdata from '{os.path.join(indir,file)}' WITH DELIMITER ',' CSV HEADER;"""
        f.write(sql+"\n")
pass
