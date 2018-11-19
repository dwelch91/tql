import unittest

from tql.exceptions import FilterError
from tql.__main__ import main
from tql.filter import preprocess_filters, apply_filters


class TestFilters(unittest.TestCase):

    def test_filters_list(self):
        main(args=['--filters-list'])

    def test_preprocess_filters_simple(self):
        args = ["foo|num", "fake|add:1", "first|num|add:1"]
        expected = {
            "foo": [["num"]],
            "fake": [["add", "1"]],
            "first": [["num"], ["add", "1"]]
        }

        t = preprocess_filters(args)
        self.assertEqual(expected, t)

    def test_preprocess_filters_replace(self):
        args = ["foo|num", "fake|add:1", "first|format:08[:comma:].1f"]
        expected = {
            "foo": [["num"]],
            "fake": [["add", "1"]],
            "first": [["format", "08,.1f"]]
        }

        t = preprocess_filters(args)
        self.assertEqual(expected, t)

    def test_preprocess_filters_more_args(self):
        args = ["foo|num", "fake|add:1", "first|replace:a,b"]
        expected = {
            "foo": [["num"]],
            "fake": [["add", "1"]],
            "first": [["replace", "a", "b"]]
        }

        t = preprocess_filters(args)
        self.assertEqual(expected, t)

    def test_preprocess_filters_bad_filter(self):
        args = ["foo|num", "fake|add:1", "firstbadfilter:a,b"]
        with self.assertRaises(FilterError):
            t = preprocess_filters(args)

    def test_preprocess_filters_too_many_filters_for_col(self):
        # two filter args for col `first`
        args = ["foo|num", "fake|add:1", "first|replace:a,b", "first|num|trunc"]
        with self.assertRaises(FilterError):
            t = preprocess_filters(args)

    def test_apply_filters_simple(self):
        filters, columns, row = {"foo": [["num"]], "bar": [["lower"]]}, ["foo", "bar"], ["123", "ABC"]
        expected = [123, "abc"]

        new_row = apply_filters(filters, columns, row)
        self.assertEqual(expected, new_row)

        new_row = apply_filters({}, columns, row)
        self.assertEqual(row, new_row)

    def test_apply_filters_complex(self):
        # TODO more complex cases?
        filters = {"foo": [["num"]], "bar": [["lower"]], "links": [["mult", 10000], ["add", 1], ["humanize", "U"]]}
        columns, row = ["foo", "bar", "links"], ["123", "ABC", "100"]
        expected = [123, "abc", "1MU"]

        new_row = apply_filters(filters, columns, row)
        self.assertEqual(expected, new_row)

    def test_apply_filters_bad_filter(self):
        filters, columns, row = {"foo": [["num"]], "bar": [["fake"]]}, ["foo", "bar"], ["123", "ABC"]

        with self.assertRaises(FilterError):
            new_row = apply_filters(filters, columns, row)

    def test_apply_filters_bad_num_params(self):
        filters, columns, row = {"foo": [["num"]], "bar": [["lower", "1", "2"]]}, ["foo", "bar"], ["123", "ABC"]

        with self.assertRaises(FilterError):
            new_row = apply_filters(filters, columns, row)

    def test_data_csv(self):
        main(args=["""SELECT * FROM @'./data/filters.csv';""",
                   # '-g',
                   '-e', 'abs|abs',
                   '-e', 'add|add:1',
                   '-e', 'backticks|backticks',
                   '-e', 'capitalize|capitalize',
                   '-e', 'ceil|ceil',
                   '-e', 'center|center:10',
                   '-e', 'datetime|datetime|iso8601',
                   '-e', 'datetime_tz|datetime_tz: America/New_York|iso8601',
                   '-e', 'dehumanize|dehumanize',
                   '-f', 'csv',
                   '-F', 'table',
                   # '-s', 'output.db'
                   ])
