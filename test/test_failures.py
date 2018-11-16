from unittest import TestCase

from tql.__main__ import main
from tql.exceptions import DatabaseError, Error


class TestFailures(TestCase):

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


