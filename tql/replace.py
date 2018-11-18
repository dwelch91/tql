# from prettytable import PrettyTable
import sys

from tql.out import print_simple_output

REPLACEMENTS = [
    ('[:space:]', ' ', "Space ( )"),
    ('[:pipe:]', '|', "Pipe (|)"),
    ('[:backslash:]', '\\', "Blackslash (\)"),
    ('[:backtick:]', '`', "Backtick (`)"),
    ('[:squote:]', "'", "Single quote (')"),
    ('[:dquote:]', '"', 'Double quote (")'),
    ('[:tab:]', '\t', 'Tab (\\t)'),
    ('[:cr:]', '\r', 'Carriage return (\\r)'),
    ('[:newline:]', '\n', 'Newline (\\n)'),
    ('[:n:]', '\n', 'Newline (\\n)'),
    ('[:comma:]', ',', 'Comma (,)'),
    ('[:colon:]', ':', 'Colon (:)'),
    ('[:amp:]', '&', 'Ampersand (&)'),
    ('[:ampersand:]', '&', 'Ampersand (&)'),
    ('[:gt:]', '>', 'Greater than (>)'),
    ('[:lt:]', '<', 'Less than (<)'),
]


def apply_char_replacements(s):
    """
    Replace all [:...:] replacements in a string
    :param s:
    :return:
    """
    for seq, replacement, _ in REPLACEMENTS:
        s = s.replace(seq, replacement)
    return s


def print_replacements_table(fmt='table', stream=sys.stdout):
    table_data = []
    for seq, _, desc in REPLACEMENTS:
        if fmt in {'md', 'markdown'}:
            table_data.append([f"`{seq}`", desc])
        else:
            table_data.append([seq, desc])
    print_simple_output(table_data, ('Sequence', 'Description'), fmt, "", stream=stream)