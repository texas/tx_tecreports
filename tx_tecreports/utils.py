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
    Parses out first integer from a string


    Only works on integers that stand alone.  Returns ``None`` on
    strings without an integer.
    """
    match = re.match('[^\d]*(\d+).*', s)
    if match:
        return int(match.groups()[0])


def extract_filing_date(s, strict=False):
    """
    Convert a filing list date into a datetime.date object

    This works like ``string_to_date`` and returns ``None`` when it
    can't parse a date from the string unless ``strict`` is set to
    ``True``.
    """
    if s:
        date_string = re.sub(r'(st|nd|rd|th),', ',', s.split(':')[1].strip())
        date_string = date_string.replace('&nbsp;', '').strip()
    else:
        date_string = s
    return string_to_date(date_string, format='%B %d, %Y', strict=strict)
