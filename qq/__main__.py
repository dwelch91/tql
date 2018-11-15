import argparse
import os
import sys
import csv
import sqlite3
import re

from qq.filters import FILTERS
from qq.utils import error

try:
    import prettytable

    HAVE_PRETTY_TABLE = True
except ImportError:
    HAVE_PRETTY_TABLE = False

FROM_PATTERN = re.compile("""FROM (?=(?:(?<![a-z0-9/.~-])'([a-z0-9/.~-].*?)'(?![a-z0-9/.~-])|\"([a-z0-9/.~-].*?)\"(?![a-z0-9/~-])))""", re.I)
DEBUG = False


def debug(s):
    if DEBUG:
        sys.stderr.write(f"{s}\n")

# TODO: Refactor!


def main(args=None):
    global DEBUG
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('sql', nargs='*')
    parser.add_argument('--dialect', '-t', choices=csv.list_dialects(), default='unix',
                        help=f"Specify the CSV dialect. Valid values are {', '.join(csv.list_dialects())}.")
    parser.add_argument('--delimiter', '-d', default=',', help="Specify the CSV delimiter to use. Default is a comma (,).")
    parser.add_argument('--quotechar', '--quote-char', '-q', default='"', help='Specify the CSV quote charactor. Default is double quote (").')
    parser.add_argument('--output', '-o', default='-', help="Output file. Default is stdout (-).")
    parser.add_argument('--output-format', '--out-format', '--out-fmt', '-f', default='table', choices=['table', 'csv'],
                        help="Output format. Valid value are 'table' and 'csv'. Default is table.")
    parser.add_argument('--save-db', '-s', help="Specify a SQLite database to use (instead of using an in-memory database. The database will remain after qq exits.")
    #parser.add_argument('--load-db', '-l', help="Load an existing database instead of creating a new one.")
    parser.add_argument('--skip-lines', '--skip', '-k', type=int, default=0, help="Skip `SKIP_LINES` lines at the beginning of the file. Default is 0.")
    parser.add_argument('--headers', '-r',
                        help="Don't use the first non-skipped line for header/column names, use these header/column names instead. "
                             "Format is a comma separated list of column names. "
                             "Column names must not be SQLite reserved words.")
    parser.add_argument('--debug', '-g', action='store_true', help="Turn on debug output.")
    parser.add_argument('--filter', '-e', action='append',
                        help="Specify a column filter. Use one filter per switch/param. "
                             "Format is <column_name>|filter|<0 or more params or additional filters>.  "
                             "Filters have a variable number of parameters. Filters may be chained.")
    parser.add_argument('--filter-list', action='store_true')

    # TODO: Subparsers? qq select ... qq insert ... qq delete ... qq filter-list ... etc.
    # TODO: Handle more CSV parser params
    # TODO: Handle column names (either spec'd with -r or auto-gen'd) that are SQL reserved words... prefix or suffix them? or, have user re-map them?
    # TODO: Handle filenames that don't translate into valid table names
    # TODO: Handle duplicate column names
    # TODO: Allow for column name re-mapping (when doing auto-headers, not -r)
    # TODO: Allow for table name re-mapping (override default table name using basename of CSV/TSV file)
    # TODO: Modification queries? (read CSV, apply filters, save to db, apply SQL modification(s), output new CSV)
    # TODO: Show available filters command

    args = parser.parse_args(args=args)
    DEBUG = args.debug
    debug(args)

    if args.filter_list:
        for f, n, doc in FILTERS.values():
            print(doc)
        return 0

    tables, rewrite, i = {}, [], 0
    for sql in args.sql:
        for m in FROM_PATTERN.finditer(sql):
            path = m.group(1)
            # TODO: Handle stdin ('-')
            path = os.path.expanduser(path) if '~' in path else path
            if not os.path.exists(path):
                error(f"File not found: {path}")
                return 2
            rewrite.append(sql[i:m.start(1) - 1])
            i = m.end(1) + 1
            filename = os.path.basename(path)
            tablename = os.path.splitext(filename)[0]
            rewrite.append(tablename)
            tables[tablename] = path

        rewrite.append(sql[i:])

    new_sql = ''.join(rewrite)

    # TODO: Allow for database "re-use" - open an existing database file and use other tables in it for JOINs, etc along with the CSV input table(s)
    # TODO: --load-db <database name>
    # TODO: Have to handle case where db has an existing table with same name as one of the CSV input table(s)
    if args.save_db:
        con = sqlite3.connect(args.save_db)
    else:
        con = sqlite3.connect(":memory:")

    cur = con.cursor()

    # Pre-process the filters
    filters = {}
    if args.filter:
        debug(args.filter)
        for filter_combo in args.filter:
            parts = filter_combo.split('|')
            if len(parts) < 2:
                error(f"Invalid filter combo: {filter_combo}")
                return 1
            col = parts[0]
            params = parts[1:]
            if col in filters:
                error(f"Multiple filters for column: {col}")
                return 1
            filters[col] = params

    debug(filters)

    # Read each CSV or TSV file and insert into a SQLite table based on the filename of the file
    for tablename, path in tables.items():
        with open(path) as f:
            if args.skip_lines:
                for _ in range(args.skip_lines):
                    f.readline()

            reader = csv.reader(f, dialect=args.dialect, delimiter=args.delimiter, quotechar=args.quotechar)
            first, colnames = True, []

            for row in reader:
                row = [n.strip() for n in row if n]

                if first:
                    placeholders = ', '.join(['?'] * len(row))
                    if args.headers:
                        colnames = [n.strip() for n in args.headers.split(',')]
                        colnames_str = ','.join(colnames)
                    else:
                        colnames = [n.strip() for n in row]
                        colnames_str = ', '.join(colnames)

                    s = f"CREATE TABLE {tablename} ({colnames_str});"
                    debug(s)
                    cur.execute(s)
                    first = False
                    continue

                # Process the filters
                new_row = []
                if filters:
                    for col, data in zip(colnames, row):
                        if col in filters:
                            params = filters[col][:]
                            while params:
                                filter_name = params.pop(0)
                                if filter_name not in FILTERS:
                                    print(f"Error: Invalid filter name: {filter_name}")
                                    return 1

                                func, num_params, _ = FILTERS[filter_name]
                                func_args = [params.pop(0) for _ in range(num_params)]
                                data = func(data, *func_args)

                        new_row.append(data)

                    debug(new_row)
                    s = f"INSERT INTO {tablename} ({colnames_str}) VALUES ({placeholders});"
                    cur.execute(s, new_row)

                else:
                    debug(row)
                    s = f"INSERT INTO {tablename} ({colnames_str}) VALUES ({placeholders});"
                    cur.execute(s, row)

    con.commit()

    debug(new_sql)
    result = cur.execute(new_sql)
    column_names = [x[0] for x in cur.description]

    if args.output == '-':
        if args.output_format == 'table':
            if HAVE_PRETTY_TABLE:
                table = prettytable.PrettyTable(column_names)
                table.align = 'l'
                for row in result:
                    table.add_row(row)
                print(table)
            else:
                error("Install prettytable for table output support.")
                return 1

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
