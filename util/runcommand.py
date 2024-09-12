import subprocess
import psycopg2
from html.parser import HTMLParser
import xml.etree.ElementTree as ET


def canonicalize(text):
    lines = text.split('\n')
    return ' '.join(list(map(lambda l: l.strip(), lines))).strip()


def runcommand(command):
    p = subprocess.Popen(["bash", "-c", command],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = p.communicate()
    # return f"""\{"command": {command}, "stdout": {output}, "stderr": {errors}\}"""
    output = output.split('\n')
    errors = errors.split('\n')
    return {"rc": p.exitValue(), "stdout": output, "stderr": errors}


class psql:
    def __init__(self):
        self.conn = psycopg2.connect("dbname=baseball user=djensen")
        self.cur = self.conn.cursor()

    def runsql(self, sqlcommand):
        print(sqlcommand)
        result = self.cur.execute(sqlcommand)
        self.conn.commit()
        if result is not None:
            print(result.statusmessage)
            try:
                result = self.cur.fetchall()
                for r in result:
                    print(r)
            except Exception as e:
                print(e.args[0])
                pass


class HTML2XMLParser(HTMLParser):
    def __init__(self, root):
        super().__init__()
        self.currentelement = root
        self.parents = {}
        self.parents[root] = None

    def handle_starttag(self, tag, attrs):
        if tag in ['input', 'br', 'hr', 'img', 'link', 'col', 'meta', 'style']:
            pass
        else:
            element = ET.SubElement(self.currentelement, tag)
            for a in attrs:
                if a[1] is None:
                    continue
                if a[0].find(':') != -1:
                    continue
                element.attrib[a[0]] = a[1]
            self.parents[element] = self.currentelement
            self.currentelement = element

    def handle_endtag(self, tag):
        if tag in ['input', 'br', 'hr', 'img', 'link', 'col', 'meta', 'style']:
            pass
        else:
            self.currentelement = self.parents[self.currentelement]

    def handle_data(self, data):
        if data.strip() != '':
            self.currentelement.attrib['data'] = data.strip()
