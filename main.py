import argparse
import os
import sys
import csv
import sqlite3
import re

FROM_PATTERN = re.compile("""FROM (?=(?:(?<![a-z0-9/.~-])'([a-z0-9/.~-].*?)'(?![a-z0-9/.~-])|\"([a-z0-9/.~-].*?)\"(?![a-z0-9/~-])))""", re.I)


def to_num(n):
    try:
        return int(n)
    except ValueError:
        try:
            return float(n)
        except ValueError:
            return n


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('sql', nargs=1)
    args = parser.parse_args()

    tables, rewrite, i = {}, [], 0
    for sql in args.sql:
        for m in FROM_PATTERN.finditer(sql):
            path = m.group(1)
            path = os.path.expanduser(path) if '~' in path else path
            if not os.path.exists(path):
                print(f"File not found: {path}")
                return 2
            rewrite.append(sql[i:m.start(1)-1])
            i = m.end(1) + 1
            filename = os.path.basename(path)
            tablename = os.path.splitext(filename)[0]
            rewrite.append(tablename)
            tables[tablename] = path

        rewrite.append(sql[i:])

    new_sql = ''.join(rewrite)
    con = sqlite3.connect(":memory:")
    cur = con.cursor()

    for tablename, path in tables.items():
        with open(path) as f:
            reader = csv.reader(f)
            first, colnames = True, ''

            for row in reader:
                if first:
                    placeholders = ', '.join(['?'] * len(row))
                    colnames = ', '.join(row)
                    s = f"CREATE TABLE {tablename} ({colnames})"
                    cur.execute(s)
                    first = False
                    continue

                row = [to_num(n) for n in row]
                s = f"INSERT INTO {tablename} ({colnames}) VALUES ({placeholders});"
                cur.execute(s, row)

    con.commit()

    for row in cur.execute(new_sql):
        print(row)

    con.close()


if __name__ == '__main__':
    sys.exit(main())