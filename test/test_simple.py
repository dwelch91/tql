from unittest import TestCase

from qq.__main__ import main


class TestSimple(TestCase):

    def test_load_1(self):
        main()


    def test_skip_lines(self):
        main(args=["SELECT perms, SUM(size) FROM './ls.txt' WHERE size > 500 GROUP BY perms;",
                   '-k', '1',  # skip 1 line
                   '-r', 'perms, links, owner, grp, size, month, day, time, filename',
                   '-d', ' ',  # space delimited
                   #'-g',
                   '-e', 'size|dehumanize',
                   '-e', 'links|mult|10000|add|1|humanize|U',
                   '-e', 'owner|upper|ljust|20|reverse',
                   '-e', 'day|ordinal',
                   '-e', 'perms|replace|-|_',
                   '-e', 'grp|suffix|!',
                   '-e', 'filename|prefix|~/foo/',
                   ])


    def test_data_csv(self):
        main(args=["SELECT * FROM './data.csv' WHERE count != 15;",
                   #'-g',
                   '-e', 'mac_address|lower',
                   '-e', 'count|int',
                   '-e', 'a_volts_min|float|trunc',
                   '-e', 'start_timestamp|datetime|tz|America/Los_Angeles|iso8601',
                   '-e', 'a_volts_avg|float|format|0>15f'
                   ])

    def test_help(self):
        main(args=['--help'])


    def test_filter_list(self):
        main(args=['--filter-list'])
