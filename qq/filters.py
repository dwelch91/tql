from math import ceil, floor, trunc

import pendulum as pendulum

from qq.utils import to_num, to_int, to_float, humanize, dehumanize, ordinal


# TODO: Escape chars in filters
# TODO: Combine columns
# TODO: Split columns
# TODO: Date/time/datetime filters?
# TODO: Regex filter?
# TODO: Locale formatting


FILTERS = {
    # Data conversion
    'num': (to_num, 0, "num : Convert to integer or float."),
    'number': (to_num, 0, "number : Convert to integer or float."),
    'int': (to_int, 0, "int : Convert to integer."),
    'integer': (to_int, 0, "integer : Convert to integer. "),
    'float': (to_float, 0, "float: Convert to float."),
    'str': (lambda s: str(s), 0, "str: Convert to string."),

    # Human
    'humanize': (lambda s, u: humanize(to_num(s), u, show_value=False), 1, "humanize|<unit> : Format number to human string."),  # param: unit
    'dehumanize': (dehumanize, 0, "dehumanize : Convert from human string to number."),
    'ordinal': (lambda s: ordinal(to_int(s)), 0, "ordinal : Convert number to ordinal string."),

    # String manipulation
    'lower': (lambda s: s.lower(), 0, "lower : "),
    'upper': (lambda s: s.upper(), 0, "upper : "),
    'capitalize': (lambda s: s.capitalize(), 0, "capitalize : "),
    'ljust': (lambda s, w: s.ljust(to_int(w)), 1, "ljust|<width> : "),  # param: width
    'rjust': (lambda s, w: s.rjust(to_int(w)), 1, "rjust|<width> : "),  # param: width
    'swapcase': (lambda s: s.swapcase(s), 0, "swapcase : "),
    'replace': (lambda s, x, y: s.replace(x, y), 2, "replace|<from>|<to> : "),  # params: from, to char(s)
    'title': (lambda s: s.title(), 0, "title : "),
    'zfill': (lambda s, w: s.zfill(to_int(w)), 1, "zfill|<width> : "),  # param: width
    'len': (lambda s: len(s), 0, "len : "),
    'length': (lambda s: len(s), 0, "length : "),
    'reverse': (lambda s: ''.join(reversed(s)), 0, "reverse | "),
    'prefix': (lambda s, p: ''.join([p, s]), 1, "prefix|<prefix> : "),  # param: prefix
    'suffix': (lambda s, x: ''.join([s, x]), 1, "suffix|<suffix> : "),  # param: suffix
    'substr': (lambda s, x, y: s[x:y], 2, "substr|<start>|<end> : "),  # params: start, end

    # Data formatting
    'format': (lambda x, fmt: format(x, fmt), 1, "format|<format> : "),  # param: format

    # (Simple) maths (intermediate values are numbers and inputs are auto converted to numbers)
    'add': (lambda s, o: to_num(s) + to_num(o), 1, "add|<value> : "),  # param: value to add
    'sub': (lambda s, o: to_num(s) - to_num(o), 1, "sub|<value> : "),  # param: value to sub
    'mult': (lambda s, o: to_num(s) * to_num(o), 1, "mult|<value> : "),  # param: value to multiply
    'div': (lambda s, o: to_num(s) / to_num(o), 1, "div|<value> : "),  # param: value to divide
    'abs': (lambda x: abs(to_num(x)), 0, "abs : "),
    'round': (lambda x, d: round(to_num(x), to_int(d)), 1, "round|<digits> : "),  # param: num digits
    'ceil': (lambda x: ceil(to_num(x)), 0, "ceil : "),
    'floor': (lambda x: floor(to_num(x)), 0, "floor : "),
    'trunc': (lambda x: trunc(to_num(x)), 0, "trunc : "),

    # Datetime filters (intermediate values are pendulum datetimes)
    'datetime': (lambda s: pendulum.parse(s), 0, "datetime : "),
    'datetime_tz': (lambda s, tz: pendulum.parse(s, tz=tz), 1, "datetime_tz|<tz> : "),  # param: TZ identifier
    'tz': (lambda dt, tz: pendulum.timezone(tz).convert(dt), 1, "tz|<tz> : "),  # param: TZ identifier
    'timezone': (lambda dt, tz: pendulum.timezone(tz).convert(dt), 1, "timezone|<tz> : "),  # param: TZ identifier
    'iso8601': (lambda dt: dt.to_iso8601_string(), 0, "iso8601 : "),
    'utc': (lambda dt: pendulum.timezone('UTC').convert(dt), 0, "utc : "),
    'date_format': (lambda dt, fmt: dt.strftime(fmt), 1, "date_format|<format> : "),  # param: Datetime format for strftime
}