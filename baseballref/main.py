#!/usr/bin/env python
import sys
import os
import json
from baseballref.getdata import BaseballReference
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
    fileprefix = 'qqqq'
    o = {'fileprefix': fileprefix, 'debug': False}
    o.update(options)
    actions = ['data', 'csv', 'parameters']
    if 'actions' in options:
        actions = options['actions']
        del options['actions']
    bref = BaseballReference(**options)
    logger = bref.logger
    result = {}
    data = None
    for a in actions:
        if a == 'data':
            data = bref.getdata(args)
            logger.info(json.dumps(data,  indent=2))
            result['data'] = data
        if a == 'csv':
            bref.buildtable(data)
        if a == 'parameters':
            parameters = bref.getAllOptions()
            result['parameters'] = parameters
            logger.info(json.dumps(parameters,  indent=2))
    try:
        with open(f"/tmp/{fileprefix}.parameters.json", "w")as f:
            json.dump(parameters, f, indent=2)
        with open(f"/tmp/{fileprefix}.data.json", "w")as f:
            json.dump(data, f, indent=2)
        with open(f"/tmp/{fileprefix}.all.json", "w")as f:
            json.dump({'data': data, 'parameters': parameters}, f, indent=2)
    except:
        pass
    json.dump(result, sys.stdout)
    pass
