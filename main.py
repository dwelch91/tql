import argparse
import os
import sys
import csv
import sqlite3
import re

try:
    import prettytable
    HAVE_PRETTY_TABLE = True
except ImportError:
    HAVE_PRETTY_TABLE = False

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
    parser.add_argument('--dialect', '-t', choices=csv.list_dialects(), default='unix')
    parser.add_argument('--delimiter', '-d', default=',')
    #parser.add_argument('--doublequote', '-q', action='store_true')
    #parser.add_argument('--escapechar', '-e', )
    parser.add_argument('--quotechar', '--quote-char', '-q', default='"')
    parser.add_argument('--output', '-o', default='-')
    parser.add_argument('--output-format', '--out-format', '--out-fmt', '-f', default='table', choices=['table', 'csv'])
    parser.add_argument('--save-db', '-s')

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

    if args.save_db:
        con = sqlite3.connect(args.save_db)
    else:
        con = sqlite3.connect(":memory:")

    cur = con.cursor()

    for tablename, path in tables.items():
        with open(path) as f:
            reader = csv.reader(f, dialect=args.dialect, delimiter=args.delimiter, quotechar=args.quotechar)
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

    result = cur.execute(new_sql)
    column_names = [x[0] for x in cur.description]

    if args.output == '-':
        if args.output_format == 'table':
            table = prettytable.PrettyTable(column_names)
            for row in result:
                table.add_row(row)
            print(table)

        elif args.output_format == 'csv':
            writer = csv.writer(sys.stdout, delimiter=args.delimiter)
            writer.writerow(column_names)
            for row in result:
                writer.writerow(row)
    else:
        with open(args.output, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=args.delimiter)
            for row in result:
                writer.writerow(row)

    con.close()


if __name__ == '__main__':
    sys.exit(main())