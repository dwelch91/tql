from prettytable import PrettyTable


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


def print_replacements_table():
    table = PrettyTable(('Sequence', 'Description'))
    table.align = 'l'
    for seq, _, desc in REPLACEMENTS:
        table.add_row((seq, desc))
    print(table)