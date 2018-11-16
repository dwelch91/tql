import os
import re

from tql.exceptions import Error
from tql.replacements import apply_char_replacements
from tql.utils import expand_path_and_exists

FROM_PATTERN = re.compile(r"""FROM\s+@([\'\"])(?!\1)(.+?)\1|FROM\s+@([^\'\"\s]+)|FROM\s+(-)\s+""", re.I)


def rewrite_sql(sql, table_remap=None):
    """
    Re-write the SQL, replacing @filenames with table names.
    Leave non-@ prefixed table names as-is.
    Handle stdin - and @-
    :param sql:
    :param table_remap:
    :return:
    """
    table_remap = table_remap or {}
    tables, rewrite, i = {}, [], 0
    for s in sql:
        s = apply_char_replacements(s)
        for m in FROM_PATTERN.finditer(s):
            if m.group(2):
                grp, path = 2, m.group(2)
            elif m.group(3):
                grp, path = 3, m.group(3)
            elif m.group(4):
                grp, path = 4, m.group(4)
            else:
                raise Error("Path parsing error.")

            if path != '-':
                path, exists = expand_path_and_exists(path)
                if not exists:
                    raise FileNotFoundError(f"File not found: {path}")

            rewrite.append(s[i:m.start(grp) - (2 if grp == 2 else 1 if grp == 3 else 0)])
            i = m.end(grp) + (1 if grp == 2 else 0)

            if path != '-':
                filename = os.path.basename(path)
                tablename = os.path.splitext(filename)[0]
            else:
                filename = '-'
                tablename = 'stdin'

            if path in table_remap:
                tablename = table_remap[path]
            elif filename in table_remap:
                tablename = table_remap[filename]
            elif tablename in table_remap:
                tablename = table_remap[tablename]

            rewrite.append(tablename)
            tables[tablename] = path

        rewrite.append(s[i:])

    return ''.join(rewrite), tables


def process_table_remapping(remap_table):
    """

    :param remap_table:
    :return:
    """
    table_remapping = {}
    remap_table = remap_table or []
    for remap in remap_table:
        src, trg = remap.split('=', 1)  # TODO: Error handling
        table_remapping[apply_char_replacements(src)] = apply_char_replacements(trg)
    return table_remapping


def process_column_remapping(remap_column):
    """

    :param remap_column:
    :return:
    """
    column_remapping = {}
    remap_column = remap_column or []
    for remap in remap_column:
        src, trg = remap.split('=', 1)
        column_remapping[apply_char_replacements(src)] = apply_char_replacements(trg)
    return column_remapping


# TODO: DRY these 2 funcs ^^^

