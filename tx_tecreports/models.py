# Try to use Python3 here
try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

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
    def parent(self):
        if not self.parent_id:
            return
        if self.report is None:
            raise Exception('Unable to locate parent (no report present)')
        return self.report.find(id=self.parent_id)


class Report(object):
    def __init__(self, raw_report=None):
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

    @require_initialization
    def cover(self):
        data = self.buckets['CVR'][0].split(',')
        return Cover(data)

    @require_initialization
    def receipts(self):
        if self._receipts is None:
            self._receipts = []
            data = StringIO(u"\n".join(self.buckets['RCPT']))
            for row in UnicodeCSVReader(data):
                self._receipts.append(Receipt(row, self))
        return self._receipts

    def search(self, **kwargs):
        for r in self.receipts:
            for attr, value in kwargs.items():
                if getattr(r, attr) == value:
                    yield r

    def find(self, **kwargs):
        return [a for a in self.search(**kwargs)]

    def get(self, **kwargs):
        result_set = self.search(**kwargs)
        result = result_set.next()
        try:
            result_set.next()
            raise exceptions.MultipleFound
        except StopIteration:
            return result

    @property
    def total_receipts(self):
        return sum([a.contribution.amount for a in self.receipts])
