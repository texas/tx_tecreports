import requests

from . import models

BASE_FILER_URL_TEMPLATE = 'http://www.ethics.state.tx.us/php/filer.php?acct={filer_id}'
BASE_URL_TEMPLATE = 'http://204.65.203.5/public/{report_id}noadd.csv'


def fetch_raw_report(report_id):
    return requests.get(BASE_URL_TEMPLATE.format(report_id=report_id))


def get_report(report_id):
    raw_report = fetch_raw_report(report_id)
    return models.Report(report_id=report_id, raw_report=raw_report)


def fetch_filing_list(filer_id):
    return requests.get(BASE_FILER_URL_TEMPLATE.format(filer_id=filer_id))


def get_filings_list(filer_id):
    raw_filing_list = fetch_filing_list(filer_id)
    return models.FilingList(raw_filing_list=raw_filing_list)
