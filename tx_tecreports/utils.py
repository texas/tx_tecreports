import datetime


def string_to_date(s, strict=False):
    """
    Convert a string to a datetime.date object

    Returns ``None`` on dates that it can't parse unless you call it
    with the kwarg ``strict`` set to ``True``.
    """
    try:
        return datetime.datetime.strptime(s, '%Y%m%d').date()
    except (TypeError, ValueError) as e:
        if strict:
            raise e
