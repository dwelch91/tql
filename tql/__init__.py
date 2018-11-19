import sqlite3
import sys

from tabulator import Stream

from tql.exceptions import Error
from tql.filter import apply_filters, check_filters_against_columns
from tql.custom import S3Loader, GSLoader
from tql.out import do_output
from tql.sql import rewrite_sql
from tql.utils import expand_path_and_exists

DEBUG = False


def debug(s, title=None):
    if DEBUG:
        sys.stderr.write(f"{title or ''}{s!r}\n")


def execute(sql: str,
            headers=None,
            filters=None,
            output='-',
            output_format='table',
            skip_lines=0,
            output_delimiter=',',
            column_remapping=None,
            table_remapping=None,
            auto_filter=False,
            save_db=None,
            load_db=None,
            # dialect='unix',
            input_format='csv',
            input_delimiter=',',
            input_encoding='utf-8',
            input_compression=None,
            #input_quotechar='"',
            debug_=False
            ):
    """
    :param input_format:
    :param filters:  {"col": [["filter", ...args...], ...]
    :param sql:
    :param headers:
    :param output:
    :param output_format:
    :param skip_lines:
    :param output_delimiter:
    :param column_remapping: {"col": "map_to_col", ...}
    :param table_remapping:  {"table": "map_to_col", ...}
    :param auto_filter:
    :param save_db:
    :param load_db:
    # :param dialect:
    :param input_delimiter:
    # :param input_quotechar:
    :param debug_:
    :return:
    """

    global DEBUG
    DEBUG = debug_
    column_remapping = column_remapping or {}
    headers = headers or []
    if headers and isinstance(headers, str):
        headers = [h.strip() for h in headers.split(',')]
        # debug(headers, "headers=")
    filters = filters or {}

    # Re-write the SQL, replacing filenames with table names and apply table re-mapping(s)
    sql, tables = rewrite_sql(sql, table_remapping)
    debug(sql, 'sql=')
    debug(tables, 'tables=')

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

    # if load_db:
    #     # Check for table conflicts
    #     s = f"""SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"""
    #     result = cur.execute(s)
    #     for tables in result.fetchall():
    #         pass

    # Read each CSV or TSV file and insert into a SQLite table based on the filename of the file
    for tablename, path in tables.items():
        print(path)
        with Stream(path,
                    format=input_format,
                    delimiter=input_delimiter,
                    skip_rows=range(1, skip_lines + 1),
                    custom_parsers={},
                    custom_loaders={'s3': S3Loader,
                                    'gs': GSLoader},
                    custom_writers={},
                    ignore_blank_headers=True,
                    encoding=input_encoding,
                    compression=input_compression,
                    headers=headers if headers else 1,
                    # fill_merged_cells=True,
                ) as stream:

            debug(stream.headers, "headers=")
            debug(stream.encoding, "encoding=")
            # print(stream.sample)

            first, colnames = True, []
            for row in stream:
                # print(row)
                debug(row, "row=")
                row = [n.strip() if isinstance(n, str) else n for n in row if not isinstance(n, str) or (isinstance(n, str) and n)]
                # debug(row, "row=")
                if first:
                    #print(row)
                    placeholders = ','.join(['?'] * len(row))
                    debug(placeholders, "placeholders=")
                    colnames = [column_remapping.get(n.strip()) or n.strip() for n in stream.headers]

                    # Check for duplicate column names
                    dups = set(x for x in colnames if colnames.count(x) > 1)
                    if dups:
                        raise Error(f"Invalid duplicate column name(s): {', '.join(dups)}")

                    # Apply auto filtering
                    if auto_filter:
                        for col in colnames:
                            if col not in filters:
                                filters[col] = [['num']]
                        debug(filters, 'filters (auto)=')

                    debug(colnames, 'colnames=')
                    colnames_str = ','.join(f'"{c}"' for c in colnames)

                    check_filters_against_columns(filters, colnames)

                    s = f"""CREATE TABLE "{tablename}" ({colnames_str});"""
                    debug(s)
                    try:
                        cur.execute(s)
                    except sqlite3.OperationalError as e:
                        raise Error("Failed to create table. Most likely cause is missing headers. "
                                    "Use --headers/-r and/or --skip-lines/-k to setup headers.")

                    first = False
                    # continue

                filtered_row = apply_filters(filters, colnames, row)

                s = f"""INSERT INTO "{tablename}" ({colnames_str}) VALUES ({placeholders});"""
                debug(f"{s}, {filtered_row}")
                cur.execute(s, filtered_row)

    con.commit()

    debug(sql, 'sql=')
    do_output(sql, cur, output, output_format, output_delimiter)
    con.close()
