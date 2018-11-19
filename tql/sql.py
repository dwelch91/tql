import os
import re
import sys

from urllib.parse import urlparse

from tql.exceptions import Error
from tql.replace import apply_char_replacements
from tql.utils import expand_path_and_exists


RESERVED_WORDS = {
    'ABORT', 'ACTION', 'ADD', 'AFTER', 'ALL', 'ALTER', 'ANALYZE', 'AND', 'AS', 'ASC', 'ATTACH', 'AUTOINCREMENT',
    'BEFORE', 'BEGIN', 'BETWEEN', 'BY', 'CASCADE', 'CASE', 'CAST', 'CHECK', 'COLLATE', 'COLUMN', 'COMMIT', 'CONFLICT', 'CONSTRAINT',
    'CREATE', 'CROSS', 'CURRENT', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP',
    'DATABASE', 'DEFAULT', 'DEFERRABLE', 'DEFERRED', 'DELETE', 'DESC', 'DETACH', 'DISTINCT', 'DO', 'DROP',
    'EACH', 'ELSE', 'END', 'ESCAPE', 'EXCEPT', 'EXCLUSIVE', 'EXISTS', 'EXPLAIN',
    'FAIL', 'FILTER', 'FOLLOWING', 'FOR', 'FOREIGN', 'FROM', 'FULL', 'GLOB', 'GROUP', 'HAVING',
    'IF', 'IGNORE', 'IMMEDIATE', 'IN', 'INDEX', 'INDEXED', 'INITIALLY', 'INNER', 'INSERT', 'INSTEAD', 'INTERSECT', 'INTO', 'IS', 'ISNULL',
    'JOIN', 'KEY', 'LEFT', 'LIKE', 'LIMIT', 'MATCH', 'NATURAL', 'NO', 'NOT', 'NOTHING', 'NOTNULL', 'NULL',
    'OF', 'OFFSET', 'ON', 'OR', 'ORDER', 'OUTER', 'OVER', 'PARTITION', 'PLAN', 'PRAGMA', 'PRECEDING', 'PRIMARY', 'QUERY',
    'RAISE', 'RANGE', 'RECURSIVE', 'REFERENCES', 'REGEXP', 'REINDEX', 'RELEASE', 'RENAME', 'REPLACE', 'RESTRICT', 'RIGHT', 'ROLLBACK', 'ROW', 'ROWS',
    'SAVEPOINT', 'SELECT', 'SET', 'TABLE', 'TEMP', 'TEMPORARY', 'THEN', 'TO', 'TRANSACTION', 'TRIGGER',
    'UNBOUNDED', 'UNION', 'UNIQUE', 'UPDATE', 'USING', 'VACUUM', 'VALUES', 'VIEW', 'VIRTUAL',
    'WHEN', 'WHERE', 'WINDOW', 'WITH', 'WITHOUT',
}


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
        # print(s)
        s = apply_char_replacements(s)
        for m in FROM_PATTERN.finditer(s):
            # print(m, m.groups())
            if m.group(2):
                grp, path = 2, m.group(2)
            elif m.group(3):
                grp, path = 3, m.group(3)
            elif m.group(4):
                grp, path = 4, m.group(4)
            else:
                raise Error("Path parsing error.")

            # print(path)
            if path != '-':
                parse_result = urlparse(path)
                scheme = parse_result.scheme
                # print(repr(scheme))
                if scheme in {'http', 'https'}:
                    pass
                elif scheme == 's3':
                    pass
                elif scheme == 'gs':
                    pass
                elif scheme in {'file', ''}:
                    path = parse_result.path
                    path, exists = expand_path_and_exists(path)
                    if not exists:
                        raise FileNotFoundError(f"File not found: {path}")
                else:
                    raise Error("Invalid URL scheme: {scheme}")

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

            if tablename.upper() in RESERVED_WORDS:
                sys.stderr.write(f"Warning: Table name {tablename} is a SQLite reserved word.")

            rewrite.append(f'"{tablename}"')
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

