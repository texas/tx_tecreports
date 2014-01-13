import datetime
import re


def string_to_date(s, format='%Y%m%d', strict=False):
    """
    Convert a string to a datetime.date object

    Returns ``None`` on dates that it can't parse unless you call it
    with the kwarg ``strict`` set to ``True``.
    """
    try:
        return datetime.datetime.strptime(s, format).date()
    except (TypeError, ValueError) as e:
        if strict:
            raise e


def parse_num_from_string(s):
    """
    Parses out first integer from a string, only works on integers that stand alone

    Returns ``None`` on strings without an integer
    """
    match = re.match('[^\d]*(\d+).*', s)
    if match:
        return int(match.groups()[0])
