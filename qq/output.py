import csv
import sqlite3
import sys

from prettytable import PrettyTable

from qq.exceptions import DatabaseError


def do_output(sql, cur, output, output_format, delimiter):
    try:
        result = cur.execute(sql)
    except sqlite3.OperationalError as e:
        raise DatabaseError("Database error: {e}")

    column_names = [x[0] for x in cur.description]

    if output == '-':  # stdout
        if output_format == 'table':
            table = PrettyTable(column_names)
            table.align = 'l'
            for row in result:
                table.add_row(row)
            print(table)

        elif output_format == 'csv':
            writer = csv.writer(sys.stdout, delimiter=delimiter)
            writer.writerow(column_names)
            for row in result:
                writer.writerow(row)
    else:
        with open(output, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=delimiter)
            for row in result:
                writer.writerow(row)
