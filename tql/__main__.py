import sys
import argparse
import csv

# from pytablewriter import TableWriterFactory

from tql import execute
from tql.exceptions import Error
from tql.filter import print_filter_list_table, preprocess_filters
from tql.replace import print_replacements_table, apply_char_replacements
from tql.sql import rewrite_sql, process_table_remapping, process_column_remapping
from tql.utils import error

DEBUG = False


def debug(s, title=None):
    if DEBUG:
        sys.stderr.write(f"{title or ''}{s!r}\n")


def build_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('sql', nargs='*', help="The SQL to execute. "
                                               "Use filenames surrounded by single or double quotes to specify CSV sources instead of existing tables in the FROM clause(s). "
                                               "You can use [:...:] replacements for special characters (see --help-filters for more information.")
    # Input
    # input_formats = TableWriterFactory.get_format_name_list()
    input_formats = ['csv', 'json']
    parser.add_argument('--input-format', '--in-format', '--in-fmt', '-f', default='csv', choices=input_formats, # + ['table', 'ptable', 'pt'],
                        help=f"Input format. Valid value are {', '.join(input_formats)}. Default is `csv`.")
    parser.add_argument('--skip-lines', '--skip', '-k', type=int, default=0, help="Skip `SKIP_LINES` lines at the beginning of the file. Default is 0.")
    # parser.add_argument('--input-dialect', '-t', choices=csv.list_dialects(), default='unix',
    #                     help=f"Specify the CSV dialect. Valid values are {', '.join(csv.list_dialects())}. Default is `unix`.")
    parser.add_argument('--input-delimiter', '-d', default=',', help="Specify the CSV delimiter to use. Default is a comma (,).")
    # parser.add_argument('--input-quotechar', '--quote-char', '-q', default='"', help='Specify the CSV quote charactor. Default is double quote (").')
    parser.add_argument('--input-encoding', default='utf8', help="Specify the input file encoding. Defaults to 'utf8'.")

    parser.add_argument('--headers', '-r',
                        help="Don't use the first non-skipped line for header/column names, use these header/column names instead. "
                             "Format is a comma separated list of column names. "
                             "Column names must not be SQLite reserved words.")

    # Filtering
    parser.add_argument('--filter', '-e', action='append',
                        help="Specify a column filter. Use one filter per switch/param. "
                             "Format is <column_name>|filter|<0 or more params or additional filters in filter chain>.  "
                             "Filters have a variable number of parameters (0+). Filters may be chained.")
    parser.add_argument('--auto-filter', '-a', action='store_true', help="Automatically apply the `num` filter to all column data.")

    # Split and merge columns
    #parser.add_argument('--merge-columns', '--merge', '-M')  # -M "one,two,three=foo"
    #parser.add_argument('--split-column', '--split', '-S')  # -S "foo=one,two,three"

    # Re-mapping
    parser.add_argument('--remap-column', '--remap-header', '-m', action='append',
                        help="A single column re-map in the form <col_name>=<new_col_name>. Use one switch for each column re-mapping. "
                             "This overrides any column/header names that are auto-discovered or passed in via --headers/-r. "
                             "You can use [:...:] replacements for special characters (see --help-filters for more information.")
    #parser.add_argument('--auto-remap-columns')
    parser.add_argument('--remap-table', '--remap-file', '-T', action='append',
                        help="A single table re-map in the form <table_name>=<new_table_name>. Use one switch for each table re-mapping. "
                             "This overrides any table names that are auto-generated from filenames passed in via the SQL statement. "
                             "You can use [:...:] replacements for special characters (see --help-filters for more information.")
    #parser.add_argument('--auto-remap-tables')

    # Save/load database
    db_group = parser.add_mutually_exclusive_group()
    db_group.add_argument('--save-db', '-s', help="Specify a SQLite database to use (instead of using an in-memory database. The database will remain after tql exits.")
    db_group.add_argument('--load-db', '-l', help="Load an existing database instead of creating a new one.")

    # Output
    parser.add_argument('--output', '-o', default='-', help="Output file. Default is stdout (-).")
    output_formats = ['csv', 'table', 'md', 'markdown']
    # output_formats = TableWriterFactory.get_format_name_list() + ['table', 'ptable', 'pt']
    parser.add_argument('--output-format', '--out-format', '--out-fmt', '-F', default='table', choices=output_formats,
                        help=f"Output format. Valid value are {', '.join(output_formats)}. Default is table.")
    parser.add_argument('--output-delimiter', '-D', default=',', help="Specify the CSV delimiter to use for output. Default is a comma (,).")
    parser.add_argument('--output-quotechar', '-Q', '--output-quote-char', default='"', help='Specify the CSV quote character for output. Default is double quote (").')

    # S3 I/O
    parser.add_argument('--aws-profile')

    # GS I/O
    parser.add_argument('--gcp-profile')

    # Debug
    parser.add_argument('--debug', '-g', action='store_true', help="Turn on debug output.")

    # Help
    parser.add_argument('--filters-list', '--filter-list', '--help-filters', action='store_true')
    parser.add_argument('--replacements-list', '--replacement-list', '--help-replacements', action='store_true')

    return parser


def main(args=None):
    global DEBUG
    if args is None:
        args = sys.argv[1:]

    parser = build_args_parser()
    args = parser.parse_args(args=args)
    DEBUG = args.debug
    debug(args, 'args=')

    if args.filters_list:
        print_filter_list_table(args.output_format)
        return 0

    if args.replacements_list:
        print_replacements_table(args.output_format)
        return 0

    if not args.sql:
        raise Error("You must specify the SQL to execute.")

    # Process table re-mappings, if any
    table_remapping = process_table_remapping(args.remap_table)
    debug(table_remapping, 'table_remapping=')

    # Pre-process the filters
    filters = preprocess_filters(args.filter)
    debug(filters, 'filters=')

    # Process the column re-mappings, if any
    column_remapping = process_column_remapping(args.remap_column)
    debug(column_remapping, 'column_remapping=')

    # Process delimiters
    input_delimiter = apply_char_replacements(args.input_delimiter)

    execute(args.sql,
            headers=args.headers,
            filters=filters,
            output=args.output,
            output_format=args.output_format,
            skip_lines=args.skip_lines,
            output_delimiter=',',
            column_remapping=column_remapping,
            table_remapping=table_remapping,
            auto_filter=args.auto_filter,
            save_db=args.save_db,
            load_db=args.load_db,
            input_format=args.input_format,
            input_delimiter=input_delimiter,
            input_encoding=args.input_encoding,
            debug_=args.debug)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Error as e:
        error(e.msg)
        sys.exit(1)  # TODO: correct result code
