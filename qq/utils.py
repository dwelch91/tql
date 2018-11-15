import re
import sys

POWERS_10 = {0: "", 3: "K", 6: "M", 9: "G", 12: "T", 15: "P", 18: "E"}
POWERS_2 = {0: "", 10: "K", 20: "M", 30: "G", 40: "T", 50: "P", 60: "E"}
INV_POWERS_10 = {"": 0, "K": 3, "M": 6, "G": 9, "T": 12, "P": 15, "E": 18}
INV_POWERS_2 = {"": 0, "K": 10, "M": 20, "G": 30, "T": 40, "P": 50, "E": 60}


def humanize(value, unit='B', use_commas=True, show_value=True, SI=True, sig_digits=3):
    """
    Format a str_value scaling it to the nearest scaling factor (K, G, B, etc.)
    If SI, use powers of 10 and report megabytes (MB), gigabytes (GB), etc.
    If not SI, use powers of 2 and report mebibytes (MiB), gibibytes (GiB), etc.
    """
    str_value = '{:,}'.format(value) if use_commas else str(value)
    i_value, power, base, multiplier = ("", POWERS_10, 10, 1000) if SI else ("i", POWERS_2, 2, 1024)

    if value < multiplier:
        return '{}{}'.format(str_value, unit)

    for exponent in reversed(sorted(power.keys())):
        if exponent == 0:
            i_value = ""

        multiplier = base ** exponent
        if value >= multiplier:
            temp = "{:.{}g}{}{}{}".format(value / multiplier, sig_digits, power[exponent], i_value, unit)
            return temp if not show_value else "{} [{} {}]".format(temp, str_value, unit)


dehuman_re = re.compile(r"""^(?P<value>[-+]?[0-9]*\.?[0-9]+)\s*(?:(?P<units>[kKmMgGtT])(?P<si>i*))*""")


def dehumanize(v, SI=True, force_int=True):
    """
    Convert a string like "10MB", "1KiB", or "0.5mbit/s" into an equivalent scalar value
    (10000000, 1024, and 500000 respectively, in this example).
    If SI is True, use base 10 rather than base 2 multipliers.
    """
    m = dehuman_re.match(v)
    if m is None:
        raise ValueError

    si = m.group('si') != 'i' or SI
    try:
        units = m.group('units').upper()
    except AttributeError:
        units = ""

    value = float(m.group('value'))
    temp = value * (10 ** INV_POWERS_10[units]) if si else value * (2 ** INV_POWERS_2[units])
    return int(temp) if force_int else temp


ORDINAL_SUFFIXES = ['th', 'st', 'nd', 'rd']


def ordinal(n):
    """
    Return an ordinal string "1st", "2nd", "3rd", ... etc for a positive or zero integer input
    :param n: The number
    :return: Ordinal string
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Must be a positive or zero integer.")
    if n < 20:
        return str(n) + (ORDINAL_SUFFIXES[n] if n < 4 else 'th')
    else:
        unit = int(str(n)[-1])
        return str(n) + ('th' if int(str(n)[-2]) == 1 else ORDINAL_SUFFIXES[unit] if unit < 4 else 'th')


def to_num(n):
    if isinstance(n, str):
        try:
            return int(n)
        except ValueError:
            try:
                return float(n)
            except ValueError:
                pass
    return n


def to_int(n):
    try:
        return int(n)
    except ValueError:
        return n


def to_float(n):
    try:
        return float(n)
    except ValueError:
        return n


def error(s):
    sys.stderr.write(f"Error: {s}\n")


