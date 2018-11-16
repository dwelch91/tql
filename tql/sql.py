import os
import re

from tql.replacements import apply_char_replacements

FROM_PATTERN = re.compile("""FROM (?=(?:(?<![a-z0-9/.~-])'([a-z0-9/.~-].*?)'(?![a-z0-9/.~-])|\"([a-z0-9/.~-].*?)\"(?![a-z0-9/~-])))""", re.I)


def rewrite_sql(sql, table_remap):
    """
    Re-write the SQL, replacing filenames with table names
    :param sql:
    :param table_remap:
    :return:
    """
    table_remap = table_remap or {}
    tables, rewrite, i = {}, [], 0
    for s in sql:
        s = apply_char_replacements(s)
        for m in FROM_PATTERN.finditer(s):
            path = m.group(1)
            # TODO: Handle stdin ('-')
            path = os.path.expanduser(path) if '~' in path else path
            if not os.path.exists(path):
                raise FileNotFoundError(f"File not found: {path}")
            rewrite.append(s[i:m.start(1) - 1])  # TODO: REVISIT - maybe use re.sub?
            i = m.end(1) + 1
            filename = os.path.basename(path)
            tablename = os.path.splitext(filename)[0]
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

