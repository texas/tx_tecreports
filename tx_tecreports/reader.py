import datetime
from StringIO import StringIO

from csvkit.unicsv import UnicodeCSVReader
import requests

from . import models


def string_to_date(s):
    return datetime.datetime.strptime(s, '%Y%m%d').date()


BASE_URL_TEMPLATE = 'http://204.65.203.5/public/{report_id}noadd.csv'


def fetch_raw_report(report_id):
    return requests.get(BASE_URL_TEMPLATE.format(report_id=report_id))


class Report(object):
    def __init__(self, report_id):
        self.raw = fetch_raw_report(report_id)
        self.buckets = {}
        self._receipts = None
        self._cover = None
        for line in self.raw.iter_lines(decode_unicode=True):
            line_type = line.split(',', 1)[0]
            if line_type not in self.buckets:
                self.buckets[line_type] = []
            self.buckets[line_type].append(line)

    @property
    def cover(self):
        data = self.buckets['CVR'][0].split(',')
        return models.Cover(data)

    @property
    def receipts(self):
        if self._receipts is None:
            self._receipts = []
            data = StringIO("\n".join(self.buckets['RCPT']))
            for row in UnicodeCSVReader(data):
                self._receipts.append(models.Receipt(row, self))
        return self._receipts

    def find(self, some_id):
        for r in self.receipts:
            if r.id == some_id:
                return r

    @property
    def total_receipts(self):
        return sum([a.contribution.amount for a in self.receipts if a.contribution.amount])
