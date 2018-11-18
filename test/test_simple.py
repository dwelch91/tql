from unittest import TestCase, skip

from tql.__main__ import main


class TestSimple(TestCase):

    def test_skip_lines(self):
        main(args=["SELECT * FROM @'./data/ls.txt' WHERE size > 500 GROUP BY perms;",
                   '-k', '1',  # skip 1 line
                   '-r', 'perms, links, owner, grp, size, month, day, time, filename',  # column names
                   '-d', ' ',  # space delimited
                   # '-g',  # debug
                   '-T', 'ls=dirlist',  # re-map table name
                   '-m', 'owner=RENWO',  # re-map column
                   '-e', 'size|dehumanize',  # filter
                   '-e', 'links|mult:10000|add:1|humanize:U',  # filter
                   '-e', 'RENWO|upper|ljust:20|reverse',  # filter
                   '-e', 'day|ordinal',  # filter
                   '-e', 'perms|replace:-,[:pipe:]',  # filter
                   '-e', 'grp|suffix:!',  # filter
                   '-e', 'filename|prefix:~/[:space:]foo[:pipe:]/[:backslash:]|suffix:[:pipe:]',  # filter
                   '-f', 'table',
                   ])

    def test_data_csv(self):
        main(args=["SELECT * FROM @'./data/data.csv' WHERE a_volts_min < 220;",
                   # '-g',
                   '-e', 'mac_address|lower',
                   '-e', 'count|int',
                   '-e', 'a_volts_min|float|trunc',
                   '-e', 'start_timestamp|datetime|tz:America/Los_Angeles|iso8601',
                   '-e', 'a_volts_avg|float|format:0>15f',
                   # '-f', 'csv',
                   '-f', 'table',
                   # '-s', 'output.db'
                   ])

    def test_formatting(self):
        main(args=["SELECT * FROM @'./data/test1.csv';",
                   '-e', 'foo|thousands',
                   '-e', 'yyy|num|format:08[:comma:].1f',
                   '-e', 'bar|num|format:08[:comma:]d',
                   ])

    def test_remap_col(self):
        main(args=["SELECT * FROM @'./data/remap.csv' WHERE frm = 'y';",
                   # '-g',
                   '-m', 'group=grp',  # re-map column name
                   '-m', 'from=frm',  # re-map column name
                   '-m', 'to=too',  # re-map column name
                   ])

    def test_remap_col_double_quotes(self):
        main(args=["""SELECT * FROM @"./data/remap.csv" WHERE frm = 'y';""",
                   # '-g',
                   '-m', 'group=grp',  # re-map column name
                   '-m', 'from=frm',  # re-map column name
                   '-m', 'to=too',  # re-map column name
                   '-f', 'pandas'
                   ])

    @skip
    def test_help(self):
        main(args=['--help'])

    def test_replacements_list(self):
        main(args=['--replacements-list', '-f', 'md'])

    def test_auto_filters(self):
        main(args=["SELECT * FROM @'./data/ls.txt' WHERE links > 1;",
                   '-k', '1',  # skip 1 line
                   '-r', 'perms, links, owner, grp, size, month, day, time, filename',  # column names
                   '-d', ' ',  # space delimited
                   # '-g',  # debug
                   '-e', 'size|dehumanize',
                   '-T', 'ls=dirlist',  # re-map table name
                   '-a'  # auto filtering
                   ])
