import subprocess
import psycopg2


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
