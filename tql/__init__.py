import csv
import sqlite3
import sys

from tql.exceptions import Error
from tql.filter import apply_filters
from tql.out import do_output
from tql.utils import expand_path_and_exists

DEBUG = False


def debug(s, title=None):
    if DEBUG:
        sys.stderr.write(f"{title or ''}{s!r}\n")


def execute(sql: str,
            tables=None,
            headers=None,
            filters=None,
            output='-',
            output_format='csv',
            skip_lines=0,
            output_delimiter=',',
            column_remapping=None,
            auto_filter=False,
            save_db=None,
            load_db=None,
            dialect='unix',
            input_delimiter=',',
            input_quotechar='"',
            debug_=False
            ):
    """
    :param filters:
    :param sql:
    :param tables:
    :param headers:
    :param output:
    :param output_format:
    :param skip_lines:
    :param output_delimiter:
    :param column_remapping:
    :param auto_filter:
    :param save_db:
    :param load_db:
    :param dialect:
    :param input_delimiter:
    :param input_quotechar:
    :param debug_:
    :return:
    """

    global DEBUG
    DEBUG = debug_
    column_remapping = column_remapping or {}
    headers = headers or []
    tables = tables or {}
    filters = filters or {}

    # Open the database
    if save_db:
        path, exists = expand_path_and_exists(save_db)
        if exists:
            raise Error("fDatabase file {path} already exists.")
        con = sqlite3.connect(path)
    elif load_db:
        path, exists = expand_path_and_exists(load_db)
        if not exists:
            raise FileNotFoundError(f"Database file {path} not found.")
        con = sqlite3.connect(path)
    else:
        con = sqlite3.connect(":memory:")

    cur = con.cursor()

    # Read each CSV or TSV file and insert into a SQLite table based on the filename of the file
    for tablename, path in tables.items():
        with open(path) as f:
            if skip_lines:
                [f.readline() for _ in range(skip_lines)]

            reader = csv.reader(f, dialect=dialect, delimiter=input_delimiter, quotechar=input_quotechar)
            first, colnames = True, []

            for row in reader:
                debug(row)
                row = [n.strip() for n in row if n]

                if first:
                    placeholders = ', '.join(['?'] * len(row))
                    col_src = headers if headers else row
                    colnames = [column_remapping.get(n.strip()) or n.strip() for n in col_src]

                    # Apply auto filtering
                    if auto_filter:
                        for col in colnames:
                            if col not in filters:
                                filters[col] = [['num']]
                        debug(filters, 'filters (auto)=')

                    debug(colnames, 'colnames=')
                    colnames_str = ','.join(colnames)

                    # TODO: For -l/--load-db, handle case where db has an existing table with same name as one of the CSV input table(s)
                    s = f"CREATE TABLE {tablename} ({colnames_str});"
                    debug(s, 'table create: ')
                    try:
                        cur.execute(s)
                    except sqlite3.OperationalError as e:
                        raise Error("Failed to create table. Most likely cause is missing headers. "
                                    "Use --headers/-r and/or --skip-lines/-k to setup headers.")

                    first = False
                    continue

                filtered_row = apply_filters(filters, colnames, row)
                debug(row, 'row=')
                s = f"INSERT INTO {tablename} ({colnames_str}) VALUES ({placeholders});"
                cur.execute(s, filtered_row)

    con.commit()

    debug(sql, 'sql=')
    do_output(sql, cur, output, output_format, output_delimiter)
    con.close()
