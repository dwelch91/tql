import csv
import sqlite3

from prettytable import PrettyTable
from pytablewriter import TableWriterFactory

from tql.exceptions import DatabaseError


def do_output(sql, cur, output, output_format, delimiter):
    try:
        result = cur.execute(sql)
    except sqlite3.OperationalError as e:
        raise DatabaseError("Database error: {e}")

    column_names = [x[0] for x in cur.description]

    if output == '-':  # output_format
        print_simple_output(result.fetchall(), column_names, output_format, "Output")  # TODO: Set name to table name

    else:
        with open(output, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=delimiter)
            for row in result:
                writer.writerow(row)


def print_simple_output(data, col_names, fmt, name):
    if fmt in {'table', 'ptable', 'pt'}:
        table = PrettyTable(col_names)
        table.align = 'l'
        for row in data:
            table.add_row(row)
        print(table)

    else:
        writer = TableWriterFactory.create_from_format_name(fmt)
        writer.table_name = name
        writer.header_list = col_names
        writer.value_matrix = data
        writer.write_table()

