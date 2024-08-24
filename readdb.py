# Note: the module name is psycopg, not psycopg3
import sys
from util.runcommand import psql
if __name__ == '__main__':
    sql = psql()
    result = sql.runsql('select count(*) from baseballdata')
    result = sql.runsql(
        "select player_name, batter, pitcher, description from baseballdata where player_name LIKE 'Coleman,%'")
    pass
sys.exit(0)
# Connect to an existing database
with psycopg.connect("dbname=baseball user=djensen") as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        # Execute a command: this creates a new table
        # cur.execute("""
        #     CREATE TABLE test (
        #         id serial PRIMARY KEY,
        #         num integer,
        #         data text)
        #     """)

        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no SQL injections!)
        for i in range(500, 10000, 100):
            result = cur.execute(
                "INSERT INTO test (num, data) VALUES (%s, %s)",
                (i, "abc'def"))
            print(result.statusmessage)
            # Query the database and obtain data as Python objects.
            cur.execute("SELECT * FROM test")
            result = cur.fetchall()
            # will return (1, 100, "abc'def")

            # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
            # of several records, or even iterate on the cursor
            for record in result:
                print(record)

            # Make the changes to the database persistent
            conn.commit()
