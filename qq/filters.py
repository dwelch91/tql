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
    'num': (to_num, 0),
    'number': (to_num, 0),
    'int': (to_int, 0),
    'integer': (to_int, 0),
    'float': (to_float, 0),
    'str': (lambda s: str(s), 0),

    # Human
    'humanize': (lambda s, u: humanize(to_num(s), u, show_value=False), 1),  # param: unit
    'dehumanize': (dehumanize, 0),
    'ordinal': (lambda s: ordinal(to_int(s)), 0),

    # String manipulation
    'lower': (lambda s: s.lower(), 0),
    'upper': (lambda s: s.upper(), 0),
    'capitalize': (lambda s: s.capitalize(), 0),
    'ljust': (lambda s, w: s.ljust(to_int(w)), 1),  # param: width
    'rjust': (lambda s, w: s.rjust(to_int(w)), 1),  # param: width
    'swapcase': (lambda s: s.swapcase(s), 0),
    'replace': (lambda s, x, y: s.replace(x, y), 2),  # params: from, to char(s)
    'title': (lambda s: s.title(), 0),
    'zfill': (lambda s, w: s.zfill(to_int(w)), 1),  # param: width
    'len': (lambda s: len(s), 0),
    'length': (lambda s: len(s), 0),
    'reverse': (lambda s: ''.join(reversed(s)), 0),
    'prefix': (lambda s, p: ''.join([p, s]), 1),  # param: prefix
    'suffix': (lambda s, x: ''.join([s, x]), 1),  # param: suffix
    'substr': (lambda s, x, y: s[x:y], 2),  # params: start, end

    # Data formatting
    'format': (lambda x, fmt: format(x, fmt), 1),  # param: format

    # (Simple) maths (intermediate values are numbers and inputs are auto converted to numbers)
    'add': (lambda s, o: to_num(s) + to_num(o), 1),  # param: value to add
    'sub': (lambda s, o: to_num(s) - to_num(o), 1),  # param: value to sub
    'mult': (lambda s, o: to_num(s) * to_num(o), 1),  # param: value to multiply
    'div': (lambda s, o: to_num(s) / to_num(o), 1),  # param: value to divide
    'abs': (lambda x: abs(to_num(x)), 1),
    'round': (lambda x, d: round(to_num(x), to_int(d)), 1),  # param: num digits
    'ceil': (lambda x: ceil(to_num(x)), 0),
    'floor': (lambda x: floor(to_num(x)), 0),
    'trunc': (lambda x: trunc(to_num(x)), 0),

    # Datetime filters (intermediate values are pendulum datetimes)
    'datetime': (lambda s: pendulum.parse(s), 0),
    'datetime_tz': (lambda s, tz: pendulum.parse(s, tz=tz), 1),  # param: TZ identifier
    'tz': (lambda dt, tz: pendulum.timezone(tz).convert(dt), 1),  # param: TZ identifier
    'timezone': (lambda dt, tz: pendulum.timezone(tz).convert(dt), 1),  # param: TZ identifier
    'iso8601': (lambda dt: dt.to_iso8601_string(), 0),
    'utc': (lambda dt: pendulum.timezone('UTC').convert(dt), 0),
    'date_format': (lambda dt, fmt: dt.strftime(fmt), 1),  # param: Datetime format for strftime
}