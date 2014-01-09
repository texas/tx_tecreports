import datetime

import requests

from . import models


def string_to_date(s):
    return datetime.datetime.strptime(s, '%Y%m%d').date()


BASE_URL_TEMPLATE = 'http://204.65.203.5/public/{report_id}noadd.csv'


def fetch_raw_report(report_id):
    return requests.get(BASE_URL_TEMPLATE.format(report_id=report_id))


def get_report(report_id):
    raw_report = fetch_raw_report(report_id)
    return models.Report(raw_report=raw_report)
