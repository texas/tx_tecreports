import decimal
# Try to use Python3 here
try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO
import re

from pyquery import PyQuery as pq
from unicsv import UnicodeCSVReader

from . import exceptions
from . import utils
from .helpers import require_initialization, type_of_boolean


class Election(object):
    def __init__(self, date=None, type_of=None, description=None):
        self.date = utils.string_to_date(date)
        self.type_of = type_of
        self.description = description

    is_primary = type_of_boolean('P')
    is_general = type_of_boolean('G')
    is_runoff = type_of_boolean('R')
    is_special = type_of_boolean('S')
    is_other = type_of_boolean('O')


class Filer(object):
    def __init__(self, filer_id=None, filer_type=None, last_name=None,
            first_name=None, name_prefix=None, name_suffix=None,
            nickname=None):
        self.filer_id = filer_id
        self.filer_type = filer_type
        self.last_name = last_name
        self.first_name = first_name
        self.name_prefix = name_prefix
        self.name_suffix = name_suffix
        self.nickname = nickname


class Cover(object):
    def __init__(self, data):
        self.data = data
        self.parse()

    def parse(self):
        self.type_of_filing = self.data[1]
        self.filer = Filer(*self.data[2:9])
        self.report_number = int(self.data[9])
        self.is_original = self.report_number is 0
        self.from_date = utils.string_to_date(self.data[10])
        self.through_date = utils.string_to_date(self.data[11])

        self.election = Election(*self.data[12:15])


class Contributor(object):
    def __init__(self, type_of=None, last_name=None, first_name=None,
            title=None, suffix=None, address_1=None, address_2=None,
            city=None, state=None, zipcode=None):
        self.type_of = type_of
        self.is_individual = self.type_of == 'IND'
        self.is_entity = self.type_of == 'ENT'

        self.last_name = last_name
        self.first_name = first_name
        self.title = title
        self.suffix = suffix
        self.address_1 = address_1
        self.address_2 = address_2
        self.city = city
        self.state = state
        self.zipcode = zipcode

    @property
    def full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name).strip()

    def save(self):
        from .. import models
        type_of, created = models.ContributorType.objects.get_or_create(
                name=self.type_of)
        contributor, created = models.Contributor.objects.get_or_create(
                type_of=type_of,
                is_individual=self.is_individual,
                is_entity=self.is_entity,
                last_name=self.last_name,
                first_name=self.first_name,
                title=self.title,
                suffix=self.suffix,
                address_1=self.address_1,
                address_2=self.address_2,
                city=self.city,
                state=self.state,
                zipcode=self.zipcode)
        return contributor


class Contribution(object):
    def __init__(self, date, amount, description):
        self.date = utils.string_to_date(date)
        self.amount = float(amount) if amount else 0
        self.description = description


class Travel(object):
    def __init__(self, last_name=None, first_name=None, title=None,
            suffix=None, means_of=None, departure_location=None,
            departure_date=None, destination=None, arrival_date=None,
            purpose=None):
        self.last_name = last_name
        self.first_name = first_name
        self.title = title
        self.suffix = suffix
        self.means_of = means_of
        self.departure_location = departure_location
        self.departure_date = utils.string_to_date(departure_date)
        self.destination = destination
        self.arrival_date = utils.string_to_date(arrival_date)
        self.purpose = purpose

    def save(self, receipt):
        from .. import models
        travel, created = models.Travel.objects.get_or_create(
            last_name=self.last_name,
            first_name=self.first_name,
            title=self.title,
            suffix=self.suffix,
            means_of=self.means_of,
            departure_location=self.departure_location,
            departure_date=self.departure_date,
            destination=self.destination,
            arrival_date=self.arrival_date,
            purpose=self.purpose
        )
        return travel


class Receipt(object):
    is_out_of_state_pac = False

    def __init__(self, data, report=None):
        self.data = data
        self.report = report
        self.parse()

    def parse(self):
        self.name_of_schedule = self.data[1]
        self.id = self.data[2]
        self.contributor = Contributor(*self.data[3:13])
        self.is_out_of_state_pac = bool(self.data[13])
        self.fec_id = self.data[14] or None
        self.contribution = Contribution(*self.data[15:18])
        self.employer = self.data[18] or None
        # TODO 19 and 20 are both job title?
        self.job_title = self.data[19] or None

        self.is_travel = bool(self.data[24])
        if self.is_travel:
            self.travel = Travel(*self.data[25:35])

        self.parent_id = self.data[35] or None
        if self.parent_id:
            self.id = '%s-%s' % (self.parent_id, self.id)

    @property
    def is_child(self):
        return self.parent_id

    @property
    def parent(self):
        if not self.parent_id:
            return
        if self.report is None:
            raise Exception('Unable to locate parent (no report present)')
        return self.report.find(id=self.parent_id)

    def save(self, report):
        from .. import models
        if self.employer:
            employer, created = models.Employer.objects.get_or_create(
                    name=self.employer)
        else:
            employer = None
        kwargs = {
            'contributor': self.contributor.save(),
            'report': report,
            'date': self.contribution.date,
            'amount': self.contribution.amount,
            'description': self.contribution.description,
            'employer': employer,
            'job_title': self.job_title,
            'name_of_schedule': self.name_of_schedule,
            'receipt_id': self.id,
            'is_out_of_state_pac': self.is_out_of_state_pac,
            'fec_id': self.fec_id,
        }
        if self.parent_id:
            kwargs['parent_id'] = self.parent_id

        receipt, created = models.Receipt.objects.get_or_create(**kwargs)
        if self.is_travel:
            self.travel.save(receipt=receipt)
        return receipt


def summary_property(key1, key2):
    def inner(self):
        if not 'SMRY' in self.buckets:
            return 0
        for row in self.buckets['SMRY']:
            row = row.split(',')
            if not row[1] in key1:
                continue
            if row[2] == key2:
                return decimal.Decimal(row[3])
        return 0
    return property(inner)


def simple_summary_property(key2):
    return summary_property(['COH', 'SCCOH'], key2)


class Report(object):
    def __init__(self, report_id=None, raw_report=None):
        self.report_id = report_id
        self.raw_report = raw_report
        self._initialized = False
        if self.raw_report is not None:
            self.parse()

    def parse(self):
        self.buckets = {}
        self._receipts = None
        self._cover = None
        for line in self.raw_report.iter_lines(decode_unicode=True):
            line_type = line.split(',', 1)[0]
            if line_type not in self.buckets:
                self.buckets[line_type] = []
            self.buckets[line_type].append(line)
        self._initialized = True

    unitemized_contributions = simple_summary_property('1')
    total_contributions = simple_summary_property('2')
    unitemized_expenditures = simple_summary_property('3')
    total_expenditures = simple_summary_property('4')
    outstanding_loans = simple_summary_property('5')
    cash_on_hand = simple_summary_property('6')
    unitemized_pledges = summary_property(['B1', ], '4')
    unitemized_loans = summary_property(['E', ], '4')

    @require_initialization
    def cover(self):
        data = self.buckets['CVR'][0].split(',')
        return Cover(data)

    @require_initialization
    def receipts(self):
        if self._receipts is None:
            self._receipts = []
            data = StringIO(u"\n".join(self.buckets.get('RCPT', [])))
            for row in UnicodeCSVReader(data):
                self._receipts.append(Receipt(row, self))
        return self._receipts

    def search(self, **kwargs):
        for r in self.receipts:
            for attr, value in kwargs.items():
                if getattr(r, attr) == value:
                    yield r

    def find(self, **kwargs):
        return list(self.search(**kwargs))

    def get(self, **kwargs):
        result_set = self.search(**kwargs)
        try:
            result = result_set.next()
            try:
                result_set.next()
                raise exceptions.MultipleFound
            except StopIteration:
                return result
        except StopIteration:
            raise exceptions.UnableToGet

    @property
    def total_receipts(self):
        return sum([a.contribution.amount for a in self.receipts])

    def save(self):
        from .. import models

        # TODO: Save Race data
        kwargs = {
            'report_id': self.report_id,
            'filer_id': self.cover.filer.filer_id,
            'filer_type': self.cover.filer.filer_type,
            'report_number': self.cover.report_number,
            'is_original': self.cover.is_original,
            'from_date': self.cover.from_date,
            'through_date': self.cover.through_date,
            'unitemized_contributions': self.unitemized_contributions,
            'total_contributions': self.total_contributions,
            'unitemized_expenditures': self.unitemized_expenditures,
            'total_expenditures': self.total_expenditures,
            'outstanding_loans': self.outstanding_loans,
            'cash_on_hand': self.cash_on_hand,
            'unitemized_pledges': self.unitemized_pledges,
            'unitemized_loans': self.unitemized_loans,
        }
        report, created = models.Report.objects.get_or_create(**kwargs)
        for receipt in self.receipts:
            receipt.save(report=report)
        return report


class FilingList(list):
    def __init__(self, raw_filing_list=None):
        self.raw_filing_list = raw_filing_list
        self.parse()

    def parse(self):
        if self.raw_filing_list is None:
            return

        p = pq(self.raw_filing_list.text)
        rows = p('table[bordercolor="#CCCCCC"] tr')

        for row in rows.items():
            self.append(Filing(row('td:first').html()))

    def search(self, **kwargs):
        for f in self:
            for attr, value in kwargs.items():
                if getattr(f, attr) == value:
                    yield f

    def find(self, **kwargs):
        return list(self.search(**kwargs))

    def get(self, **kwargs):
        try:
            result_set = self.search(**kwargs)
            result = result_set.next()
            try:
                result_set.next()
                raise exceptions.MultipleFound
            except StopIteration:
                return result
        except StopIteration:
            raise exceptions.UnableToGet


class Filing(object):
    def __init__(self, raw_filing_data=None):
        self.raw_filing_data = raw_filing_data
        self._report = None
        self.filing_method = None
        self.parse()

    def parse(self):
        if not self.raw_filing_data:
            return

        doc = pq(self.raw_filing_data.strip()).html()
        data = [x.strip() for x in doc.split('<br/>')]

        self.filer_name = data[0].split(' - ')[0]
        self.report_id = utils.parse_num_from_string(data[1])
        self.is_correction = 'Corrected Report' in data[1]
        self.report_type = pq(data[2]).find('b').text()
        self.report_due = utils.extract_filing_date(data[3])
        self.report_filed = utils.extract_filing_date(data[4])
        self.filing_method = data[5].split(':')[1].strip()

    @property
    def is_downloadable(self):
        return self.filing_method == 'Electronic'

    @property
    def report(self):
        if not self._report and self.raw_filing_data:
            from .base import get_report
            self._report = get_report(self.report_id)
        return self._report
