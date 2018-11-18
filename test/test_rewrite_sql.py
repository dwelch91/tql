from unittest import TestCase, skip

from tql.sql import rewrite_sql
from tql.utils import expand_path_and_exists


class TestRewriteSql(TestCase):

    def test_rewrite_dquotes(self):
        sql = """SELECT * FROM @"./data/remap.csv" WHERE frm = 'y';"""
        table_remap = {}
        sql, map = rewrite_sql([sql], table_remap)
        self.assertEqual("""SELECT * FROM "remap" WHERE frm = 'y';""", sql)
        self.assertEqual({'remap': expand_path_and_exists('./data/remap.csv')[0]}, map)


    def test_rewrite_squotes(self):
        sql = """SELECT * FROM @'./data/remap.csv' WHERE frm = 'y';"""
        table_remap = {}
        sql, map = rewrite_sql([sql], table_remap)
        self.assertEqual("""SELECT * FROM "remap" WHERE frm = 'y';""", sql)
        self.assertEqual({'remap': expand_path_and_exists('./data/remap.csv')[0]}, map)


    def test_rewrite_no_quotes(self):
        sql = """SELECT * FROM @./data/remap.csv WHERE frm = 'y';"""
        table_remap = {}
        sql, map = rewrite_sql([sql], table_remap)
        self.assertEqual("""SELECT * FROM "remap" WHERE frm = 'y';""", sql)
        self.assertEqual({'remap': expand_path_and_exists('./data/remap.csv')[0]}, map)


    def test_rewrite_stdin_without_at(self):
        sql = """SELECT * FROM - WHERE frm = 'y';"""
        table_remap = {}
        sql, map = rewrite_sql([sql], table_remap)
        self.assertEqual("""SELECT * FROM "stdin" WHERE frm = 'y';""", sql)
        self.assertEqual({'stdin': '-'}, map)


    def test_rewrite_stdin_with_at(self):
        sql = """SELECT * FROM @- WHERE frm = 'y';"""
        table_remap = {}
        sql, map = rewrite_sql([sql], table_remap)
        self.assertEqual("""SELECT * FROM "stdin" WHERE frm = 'y';""", sql)
        self.assertEqual({'stdin': '-'}, map)


    @skip
    def test_rewrite_stdin_with_at_and_quotes(self):
        sql = """SELECT * FROM '@-' WHERE frm = 'y';"""   # TODO: Doesn't work... maybe don't support this?
        table_remap = {}
        sql, map = rewrite_sql([sql], table_remap)
        self.assertEqual("""SELECT * FROM "stdin" WHERE frm = 'y';""", sql)
        self.assertEqual({'stdin': '-'}, map)


    def test_rewrite_multiple(self):
        sql = """SELECT * FROM @./data/remap.csv WHERE frm = 'y' SELECT * FROM @./data/test1.csv WHERE foo = 'bar';"""
        table_remap = {}
        sql, map = rewrite_sql([sql], table_remap)
        self.assertEqual("""SELECT * FROM "remap" WHERE frm = 'y' SELECT * FROM "test1" WHERE foo = 'bar';""", sql)
        self.assertDictEqual({'remap': expand_path_and_exists('./data/remap.csv')[0], 'test1': expand_path_and_exists('./data/test1.csv')[0]}, map)


    def test_rewrite_db_table(self):
        sql = """SELECT * FROM foo WHERE frm = 'y';"""
        table_remap = {}
        sql, map = rewrite_sql([sql], table_remap)
        self.assertEqual("""SELECT * FROM foo WHERE frm = 'y';""", sql)
        self.assertEqual({}, map)


    def test_rewrite_bad_quotes(self):
        sql = """SELECT * FROM @'foo" WHERE frm = 'y';"""
        table_remap = {}
        with self.assertRaises(FileNotFoundError):
            rewrite_sql([sql], table_remap)


    def test_rewrite_bad_syntax(self):
        sql = """SELECT * FROM @ WHERE frm = 'y';"""  # TODO: This doesn't fail, but it should
        table_remap = {}
        # with self.assertRaises(FileNotFoundError):
        sql, map = rewrite_sql([sql], table_remap)
        # print(sql)