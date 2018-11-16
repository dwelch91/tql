from unittest import TestCase

from qq.__main__ import main


HEADERS = 'perms, links, owner, grp, size, date, time, filename'

class TestQ(TestCase):

    def test_select_count(self):
        main(args=["SELECT COUNT(1) FROM './data/exampledatafile';",
                   '-g',
                   #'-r', HEADERS,
                   '-d', ' ',
                   ])


    def test_files_per_date(self):
        main(args=["SELECT date, COUNT(1) FROM './data/exampledatafile' GROUP BY date;",
                   #'-g',
                   '-r', HEADERS,
                   '-d', ' ',
                   ])


    def test_files_per_date_more_than_3(self):
        main(args=["SELECT date, COUNT(1) AS cnt FROM './data/exampledatafile' GROUP BY date HAVING cnt >= 3;",
                   #'-g',
                   '-r', HEADERS,
                   '-d', ' ',
                   ])


    def test_files_total_size_per_date(self):
        main(args=["SELECT date, SUM(size) FROM './data/exampledatafile' GROUP BY date;",
                   #'-g',
                   '-r', HEADERS,
                   '-d', ' ',
                   ])


    def test_files_total_size_per_date_in_kb(self):
        main(args=["SELECT date, SUM(size) / 1024.0 FROM './data/exampledatafile' GROUP BY date ORDER by size DESC LIMIT 5;",
                   #'-g',
                   '-r', HEADERS,
                   '-d', ' ',
                   ])


    def test_files_total_size_per_date_in_kb_formatted(self):
        main(args=["SELECT date, SUM(size) / 1024.0 FROM './data/exampledatafile' GROUP BY date ORDER by size DESC LIMIT 5;",
                   #'-g',
                   '-r', HEADERS,
                   '-d', ' ',
                   ])  # TODO:....


    # def test_time_manip(self):
    #     main(args=["SELECT date, SUM(size) / 1024.0 FROM './data/exampledatafile' GROUP BY date ORDER by size DESC LIMIT 5;",
    #                #'-g',
    #                '-r', HEADERS,
    #                '-d', ' ',
    #                ])


