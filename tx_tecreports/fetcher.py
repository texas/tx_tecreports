import re

from pyquery import PyQuery as pq
import requests

from . import models
from . import utils

BASE_FILER_URL_TEMPLATE = 'http://www.ethics.state.tx.us/php/filer.php?acct={filer_id}'
BASE_URL_TEMPLATE = 'http://204.65.203.5/public/{report_id}noadd.csv'


def fetch_raw_report(report_id):
    return requests.get(BASE_URL_TEMPLATE.format(report_id=report_id))


def get_report(report_id):
    raw_report = fetch_raw_report(report_id)
    return models.Report(raw_report=raw_report)


def compile_filing_data(filing_cell):
    data = [x.strip() for x in filing_cell.html().split('<br />')]

    report_due = re.sub(r'(st|nd|rd|th),', ',', data[3].split(':')[1].strip())
    report_filed = re.sub(r'(st|nd|rd|th),', ',', data[4].split(':')[1].strip())

    return {
        'filer_name': data[0].split(' - ')[0],
        'report_id': utils.parse_num_from_string(data[1]),
        'is_correction': 'Corrected Report' in data[1],
        'report_type': pq(data[2]).find('b').text(),
        'report_due': utils.string_to_date(report_due, format='%B %d, %Y'),
        'report_filed': utils.string_to_date(report_filed, format='%B %d, %Y'),
        'filing_method': data[5].split(':')[1].strip(),
    }


def get_filings_list(filer_id):
    p = pq(BASE_FILER_URL_TEMPLATE.format(filer_id=filer_id))
    rows = p('table[bordercolor="#CCCCCC"] tr')

    filings = []

    for row in rows.items():
        filings.append(compile_filing_data(row('td').eq(0)))

    return filings
