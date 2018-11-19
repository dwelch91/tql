import sys
from math import ceil, floor, trunc
from typing import Dict, List

import pendulum as pendulum

from tql.exceptions import FilterError
from tql.out import print_simple_output
from tql.utils import to_num, to_int, to_float, humanize, dehumanize, ordinal
from tql.replace import apply_char_replacements

FILTERS = {
    # Data type conversion
    'num': (to_num, 0, "<col>|num", "str", "num", "Convert to integer or float."),
    'number': (to_num, 0, "<col>|number", "str", "num", "Convert to integer or float."),
    'int': (to_int, 0, "<col>|int", "str", "int", "Convert to integer."),
    'float': (to_float, 0, "<col>|float", "str", "float", "Convert to float."),
    'str': (str, 0, "<col>|str", "any", "str", "Convert to string."),

    # Human
    'humanize': (lambda s, u: humanize(to_num(s), u, show_value=False), 1, "<col>|humanize:<unit>", "num", "str", "Format number to human string."),
    'dehumanize': (dehumanize, 0, "<col>|dehumanize", "str", "num", "Convert from human string to number."),
    'ordinal': (lambda s: ordinal(to_int(s)), 0, "<col>|ordinal", "num", "str", "Convert number to ordinal string."),

    # String manipulation
    'lower': (lambda s: s.lower(), 0, "<col>|lower", "str", "str", "Convert string to lowercase."),
    'upper': (lambda s: s.upper(), 0, "<col>|upper", "str", "str", "Convert string to uppercase."),
    'capitalize': (lambda s: s.capitalize(), 0, "<col>|capitalize", "str", "str", "Capitalize string."),
    'ljust': (lambda s, w: s.ljust(to_int(w)), 1, "<col>|ljust:<width>", "str", "str", "Left justify string in <width> spaces."),
    'rjust': (lambda s, w: s.rjust(to_int(w)), 1, "<col>|rjust:<width>", "str", "str", "Right justify string in <width> spaces."),
    'center': (lambda s, w: s.center(to_int(w), ' '), 1, "<col>|center:<width>", "str", "str", "Center string in <width> spaces."),
    'swapcase': (lambda s: s.swapcase(s), 0, "<col>|swapcase", "str", "str", "Swap string case."),
    'replace': (lambda s, x, y: s.replace(x, y), 2, "<col>|replace:<from>,<to>", "str", "str", "Replace sub-string <from> with <to>."),
    'title': (lambda s: s.title(), 0, "<col>|title", "str", "str", "Convert string to title case."),
    'zfill': (lambda s, w: s.zfill(to_int(w)), 1, "<col>|zfill:<width>", "str", "str", "Zero fill string to <width> size."),
    'length': (lambda s: len(s), 0, "<col>|length", "str", "str", "Return the length of the string."),
    'reverse': (lambda s: ''.join(reversed(s)), 0, "<col>|reverse", "str", "str", "Reverse the characters in the string."),
    'prefix': (lambda s, p: ''.join([p, s]), 1, "<col>|prefix:<prefix>", "str", "str", "Prefix the string with <prefix>."),
    'suffix': (lambda s, x: ''.join([s, x]), 1, "<col>|suffix:<suffix>", "str", "str", "Suffix the string with <suffix>."),
    'substr': (lambda s, x, y: s[x:y], 2, "<col>|substr:<start>,<end>", "str", "str", "Return a sub-string."),
    'lstrip': (lambda s, c: s.lstrip(c), 1, "<col>|lstrip:<chars>", "str", "str", "Strip <chars> from the left end of the string."),
    'ltrim': (lambda s: s.lstrip(), 0, "<col>|ltrim", "str", "str", "Strip whitespace characters from the left end of the string."),
    'rstrip': (lambda s, c: s.rstrip(c), 1, "<col>|rstrip:<chars>", "str", "str", "Strip <chars> from the right end of the string."),
    'rtrim': (lambda s: s.rstrip(), 0, "<col>|rtrim", "str", "str", "Strip whitespace characters from the right end of the string."),
    'squotes': (lambda s: f"'{s}", 0, '<col>|squote', "str", "str", "Wrap a string in single quotes."),
    'dquotes': (lambda s: f'"{s}"', 0, '<col>|dquote', "str", "str", "Wrap a string in double quotes."),
    'backticks': (lambda s: f'`{s}`', 0, '<col>|backticks', "str", "str", "Wrap a string in backticks."),

    # TODO: regex

    # Data formatting
    'format': (lambda x, fmt: format(to_num(x), fmt), 1, "<col>|format:<format>", "str", "str", "Format data using Python's `format(<format>)` function."),
    # TODO: locale:
    # 'format_currency': (),
    # 'format_number': (),
    'thousands': (lambda n: f"{to_num(n):,}", 0, "<col>|thousands", "num", "str", "Format number with thousands separators."),

    # (Simple) maths (intermediate values are numbers and inputs are auto converted to numbers)
    'add': (lambda s, o: to_num(s) + to_num(o), 1, "<col>|add:<value>", "num", "num", "Add <value> to number."),
    'sub': (lambda s, o: to_num(s) - to_num(o), 1, "<col>|sub:<value>", "num", "num", "Subtract <value> from number."),
    'mult': (lambda s, o: to_num(s) * to_num(o), 1, "<col>|mult:<value>", "num", "num", "Multiply number by <value>."),
    'div': (lambda s, o: to_num(s) / to_num(o), 1, "<col>|div:<value>", "num", "num", "Divide number by <value>."),
    'abs': (lambda x: abs(to_num(x)), 0, "<col>|abs", "num", "num", "Take the absolute value of a number."),
    'round': (lambda x, d: round(to_num(x), to_int(d)), 1, "<col>|round:<digits>", "num", "num", "Round number to <digits> digits."),
    'ceil': (lambda x: ceil(to_num(x)), 0, "<col>|ceil", "num", "num", "Return the ceiling value of a number."),
    'floor': (lambda x: floor(to_num(x)), 0, "<col>|floor", "num", "num", "Return the floor value of a number."),
    'trunc': (lambda x: trunc(to_num(x)), 0, "<col>|trunc", "num", "num", "Return the number truncated."),

    # Datetime filters (intermediate values are pendulum datetimes)
    'datetime': (lambda s: pendulum.parse(s), 0, "<col>|datetime", "str", "datetime", "Parse a datetime string."),
    'datetime_tz': (lambda s, tz: pendulum.parse(s, tz=tz), 1, "<col>|datetime_tz:<tz>", "str", "datetime", "Parse a datetime string with the specified <tz> timezone."),
    'tz': (lambda dt, tz: pendulum.timezone(tz).convert(dt), 1, "<col>|tz:<tz>", "datetime", "datetime", "Convert a datetime to a new <tz> timezone."),
    'iso8601': (lambda dt: dt.to_iso8601_string(), 0, "<col>|iso8601", "datetime", "str", "Convert a datetime to an ISO8601 string representation."),
    'utc': (lambda dt: pendulum.timezone('UTC').convert(dt), 0, "<col>|utc", "datetime", "datetime", "Convert a datetime to UTC."),
    'strftime': (lambda dt, fmt: dt.strftime(fmt), 1, "<col>|strftime:<format>", "datetime", "str", "Format a datetime using `strftime(<format>)`."),
}


def preprocess_filters(filter_args):
    """
    Check and organize filters
    :param filter_args:
    :return:
    """
    filters = {}
    if filter_args:
        for filter_combo in filter_args:
            parts = filter_combo.split('|')
            if len(parts) < 2:
                raise FilterError(f"Invalid filter combo: {filter_combo}")
            col = parts[0]
            if col in filters:
                raise FilterError(f"Multiple filters for column: {col}")
            filters[col] = []
            for f in parts[1:]:
                filter_parts = f.split(":", 1)
                if len(filter_parts) > 1:
                    args = filter_parts.pop(-1)
                    filter_parts.extend(args.split(","))
                filter_name = filter_parts[0]
                if filter_name not in FILTERS:
                    raise FilterError(f"Invalid filter name: {filter_name}")
                filter_parts = [apply_char_replacements(p) for p in filter_parts]
                filters[col].append(filter_parts)
    return filters


def print_filter_list_table(fmt='table', stream=sys.stdout):
    """
    Print out a nice table of filters w/docs
    :return:
    """
    table_data = []
    sorted_keys = sorted(FILTERS.keys())
    for func_name in sorted_keys:
        _, num_params, syntax, from_type, to_type, desc = FILTERS[func_name]
        if fmt in {'md', 'markdown'}:
            table_data.append([f"`{func_name}`", num_params, f"`{syntax}`", f"`{from_type}`", f"`{to_type}`", desc.replace('<', '`<').replace('>', '>`')])
        else:
            table_data.append([func_name, num_params, syntax, from_type, to_type, desc])

    print_simple_output(table_data, ('Filter', 'Num. Params', 'Syntax**', 'In type*', 'Out type', 'Description'), fmt,
                        "", stream=stream)

    print(
        "* Most filters that take numeric inputs will automatically apply the `num` filter to the column data prior to filtering.\n"
        "  Filters can be chained together using the pipe (|) character. For example, `c1|num|add|1|human`\n"
        "  The type of the data after the last filter has run will be the type that is added to the database.\n", file=stream)


def apply_filters(filters: Dict, colnames: List, row: List) -> List:
    """
    Process data based on filter chains
    :param filters:
    :param colnames:
    :param row:
    :return:
    """
    if filters:
        new_row = []
        for col, data in zip(colnames, row):
            if col in filters:
                params = filters[col][:]
                for f in params:
                    current_filter = f[:]  # copy so that pop does not break next iteration
                    filter_name = current_filter.pop(0)
                    if filter_name not in FILTERS:
                        raise FilterError(f"Error: Invalid filter name: {filter_name}")
                    func, num_params = FILTERS[filter_name][:2]
                    if len(current_filter) != num_params:
                        raise FilterError(
                            f"Error: Incorrect number of params for {filter_name}. Expected {num_params}, got {len(current_filter)})")
                    data = func(data, *current_filter)
            new_row.append(data)
        return new_row
    return row


def check_filters_against_columns(filters: Dict, colnames: List):
    """
    Raise a FilterError if a filter does not refer to a valid column.
    :param filters:
    :param colnames:
    :return:
    """
    for col in filters.keys():
        if col not in colnames:
            raise FilterError(f"Unknown column name in filter: {col}")
