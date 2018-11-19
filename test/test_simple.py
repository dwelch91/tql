from unittest import TestCase, skip

from tql.__main__ import main
from tql.exceptions import FilterError, DatabaseError, Error


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
                   '-f', 'csv',
                   '-d', '[:space:]',
                   '-F', 'table',
                   ])

    def test_data_csv(self):
        main(args=["""SELECT * FROM @'./data/data.csv' WHERE "a_volts_min" < 220;""",
                   # '-g',
                   '-e', 'mac_address|lower',
                   '-e', 'count|int',
                   '-e', 'a_volts_min|float|trunc',
                   '-e', 'start_timestamp|datetime|tz:America/Los_Angeles|iso8601',
                   '-e', 'a_volts_avg|float|format:0>15f',
                   '-f', 'csv',
                   '-F', 'table',
                   # '-s', 'output.db'
                   ])

    def test_formatting(self):
        main(args=["SELECT * FROM @'./data/test1.csv';",
                   '-e', 'foo|thousands',
                   '-e', 'yyy|num|format:08[:comma:].1f',
                   '-e', 'bar|num|format:08[:comma:]d',
                   ])

    def test_invalid_filter_col(self):
        with self.assertRaises(FilterError):
            main(args=["SELECT * FROM @'./data/test1.csv';",
                       '-e', 'zzz|thousands',
                       ])

    def test_invalid_filter_name(self):
        with self.assertRaises(FilterError):
            main(args=["SELECT * FROM @'./data/test1.csv';",
                       '-e', 'foo|bar',
                       ])

    def test_duplicate_headers(self):
        with self.assertRaises(Error):
            main(args=["SELECT * FROM @'./data/dups.csv';",
                       ])

    def test_no_sql(self):
        with self.assertRaises(Error):
            main(args=[])


    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            main(args=["SELECT * FROM @'foo' WHERE size > 500 GROUP BY perms;",
                       ])


    def test_invalid_sql(self):
        with self.assertRaises(DatabaseError):
            main(args=["SELECT * XXX @'foo' WHERE size > 500 GROUP BY perms;",
                       ])

    def test_remap_col(self):
        main(args=["SELECT * FROM @'./data/remap.csv' WHERE frm = 'y';",
                   # '-g',
                   '-m', 'group=grp',  # re-map column name
                   '-m', 'from=frm',  # re-map column name
                   '-m', 'to=too',  # re-map column name
                   ])

    def test_remap_col_2(self):
        main(args=["""SELECT * FROM @'./data/remap.csv' WHERE "from" = 'y';""",
                   #'-g',
                   # '-m', 'group=grp',  # re-map column name
                   # '-m', 'from=frm',  # re-map column name
                   # '-m', 'to=too',  # re-map column name
                   ])

    def test_remap_col_double_quotes(self):
        main(args=["""SELECT * FROM @"./data/remap.csv" WHERE frm = 'y';""",
                   # '-g',
                   '-m', 'group=grp',  # re-map column name
                   '-m', 'from=frm',  # re-map column name
                   '-m', 'to=too',  # re-map column name
                   '-F', 'table'
                   ])

    @skip
    def test_help(self):
        main(args=['--help'])

    def test_replacements_list(self):
        main(args=['--replacements-list', '-F', 'md'])

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

    @skip
    def test_http_xlsx(self):
        # main(args=["SELECT * FROM @'https://raw.githubusercontent.com/okfn/tabulator-py/master/data/table.xlsx';"])
        # main(args=["SELECT * FROM @'http://www.nature.com/authorguide/sdata/Data-Descriptor-tables-template-for-authors.xlsx';"])
        main(args=["SELECT * FROM @'http://reference1.mapinfo.com/software/anysite/english_AU/tutorials/Sample-Sales-Data.xlsx';",
        # main(args=["SELECT * FROM @'http://mtskheta.gov.ge/public/img/1530793528.xlsx';",
                   '-f', 'xlsx'
                   ])

    def test_http_json(self):
        # main(args=["SELECT * FROM @'https://raw.githubusercontent.com/okfn/tabulator-py/master/data/table.xlsx';"])
        # main(args=["SELECT * FROM @'http://www.nature.com/authorguide/sdata/Data-Descriptor-tables-template-for-authors.xlsx';"])
        main(args=["SELECT * FROM @'https://raw.githubusercontent.com/okfn/tabulator-py/master/data/table-dicts.json' WHERE name = 'english';",
        # main(args=["SELECT * FROM @'http://mtskheta.gov.ge/public/img/1530793528.xlsx';",
                   '-f', 'json',
                   #'-g'
                   ])