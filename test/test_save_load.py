import os
from unittest import TestCase, skip

from tql.__main__ import main


class TestSaveLoad(TestCase):

    def test_save_and_load(self):
        if os.path.exists('./test.db'):
            os.unlink('./test.db')
        main(args=["SELECT * FROM @'./data/ls.txt' WHERE size > 500 GROUP BY perms;",
                   '-k', '1',  # skip 1 line
                   '-r', 'perms, links, owner, grp, size, month, day, time, filename',  # column names
                   '-d', ' ',  # space delimited
                   #'-g',  # debug
                   '-T', 'ls=dirlist',  # re-map table name
                   '-m', 'owner=RENWO',  # re-map column
                   '-e', 'size|dehumanize',  # filter
                   '-e', 'links|mult|10000|add|1|humanize|U',  # filter
                   '-e', 'RENWO|upper|ljust|20|reverse',  # filter
                   '-e', 'day|ordinal',  # filter
                   '-e', 'perms|replace|-|[:pipe:]',  # filter
                   '-e', 'grp|suffix|!',  # filter
                   '-e', 'filename|prefix|~/[:space:]foo[:pipe:]/[:backslash:]|suffix|[:pipe:]',  # filter
                   '-s', './test.db'
                   ])

        main(args=["SELECT * FROM dirlist WHERE perms LIKE '|%' AND size < 300;",
                   '-l', './test.db'
                   ])

        main(args=["SELECT * FROM dirlist WHERE perms LIKE 'd%' AND size > 300;",
                   '-l', './test.db',
                   '-f', 'csv'
                   ])

        if os.path.exists('./test.db'):
            os.unlink('./test.db')
