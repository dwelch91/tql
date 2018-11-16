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

    if output == '-':  # stdout
        if output_format in {'table', 'ptable', 'pt'}:
            table = PrettyTable(column_names)
            table.align = 'l'
            for row in result:
                table.add_row(row)
            print(table)

        else:
            writer = TableWriterFactory.create_from_format_name(output_format)
            writer.table_name = 'foo'  # TODO
            writer.header_list = column_names
            writer.value_matrix = result.fetchall()
            writer.write_table()

    else:
        with open(output, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=delimiter)
            for row in result:
                writer.writerow(row)
