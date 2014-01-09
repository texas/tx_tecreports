import datetime
import random
import unittest

import mock

from .. import exceptions
from .. import models

SAMPLE_CVR_LINE = 'CVR,COH-SS,00062095,IND,Davis,Wendy R.,,,,0,20130730,20130805,20140304,P,,,,,,,,,,,,,SEN,,10,SEN,,10,P.O. Box 1039,,Fort Worth,TX,76101,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Wendy R. Davis,,,,,,,,'
SAMPLE_OUT_OF_STATE_PAC_LINE = 'RCPT,A1,414,ENT,PACPlus,,,,,,San Francisco,CA,94104-3503,X,C00516500,20130730,250.00,,,,,,,,,,,,,,,,,,,'
SAMPLE_INDIVIDUAL_RECEIPT_LINE = 'RCPT,A1,98,IND,Champion,Nancy,,,,,Fort Worth,TX,76107-3235,,,20130805,25.00,,Fort Worth ISD,Teacher,,,,,,,,,,,,,,,,'
SAMPLE_TRAVEL_LINE = 'RCPT,A1,634,IND,Patton,Robert,,,,,Fort Worth,TX,76107-4878,,,20130805,8000.00,(See travel info),Self-employed,Investor,,,,,X,Patton,Robert,,,Private airplane,Fort Worth TX,20130805,Washington DC (Dulles),20130805,Attend National Press Club event,'
SAMPLE_TRAVEL_SUB_RECEIPT_LINE = 'RCPT,A1,10,,,,,,,,,,,,,,,,,,,,,,X,Davis,Wendy,,,Private airplane,Washington DC (Dulles),20130805,Austin TX,20130805,Return from National Press Club event,634'


class ElectionTest(unittest.TestCase):
    def test_has_none_for_all_properties_by_default(self):
        e = models.Election()
        self.assertEqual(None, e.date)
        self.assertEqual(None, e.type_of)
        self.assertEqual(None, e.description)

    def test_boolean_flags(self):
        types = ('primary', 'general', 'runoff', 'special', 'other', )
        for t in types:
            attr = 'is_%s' % t

            e = models.Election()
            self.assertFalse(getattr(e, attr), msg='%s is not False' % attr)

            e = models.Election(type_of=t[0].upper())
            self.assertTrue(getattr(e, attr), msg='%s is not True' % attr)


class BaseCoverTest(unittest.TestCase):
    data = SAMPLE_CVR_LINE.split(',')

    def setUp(self):
        self.cover = models.Cover(self.data)


class CoverTest(BaseCoverTest):
    def test_is_original(self):
        self.assertTrue(self.cover.is_original)

    def test_report_number(self):
        self.assertTrue(self.cover.report_number is 0)

    def test_from_date(self):
        self.assertEqual(datetime.date(2013, 7, 30), self.cover.from_date)

    def test_through_date(self):
        self.assertEqual(datetime.date(2013, 8, 5), self.cover.through_date)


class CoverFilerAttrTest(BaseCoverTest):
    def test_filer_is_set(self):
        self.assertEqual(models.Filer, self.cover.filer.__class__)

    def test_filer_id(self):
        self.assertEqual('00062095', self.cover.filer.filer_id)

    def test_filer_type(self):
        self.assertEqual('IND', self.cover.filer.filer_type)

    def test_first_name(self):
        self.assertEqual('Wendy R.', self.cover.filer.first_name)

    def test_last_name(self):
        self.assertEqual('Davis', self.cover.filer.last_name)


class CoverElectionTest(BaseCoverTest):
    def test_election_is_set(self):
        self.assertEqual(models.Election, self.cover.election.__class__)

    def test_date(self):
        self.assertEqual(datetime.date(2014, 3, 4), self.cover.election.date)

    def test_is_primary(self):
        self.assertTrue(self.cover.election.is_primary)

    def test_is_not_general(self):
        self.assertFalse(self.cover.election.is_general)


class ContributorTest(unittest.TestCase):
    def test_is_individual_false(self):
        self.assertFalse(models.Contributor().is_individual)

    def test_is_individual_true(self):
        self.assertTrue(models.Contributor(type_of='IND').is_individual)

    def test_is_entity_false(self):
        self.assertFalse(models.Contributor().is_entity)

    def test_is_entity_true(self):
        self.assertTrue(models.Contributor(type_of='ENT').is_entity)


class ContributionTest(unittest.TestCase):
    def test_date_is_real_date(self):
        c = models.Contribution('20000101', '20.00', '')
        self.assertEqual(datetime.date(2000, 1, 1), c.date)

    def test_amount_is_a_float(self):
        # This is gonna be a problem
        c = models.Contribution('20000101', '20.00', '')
        self.assertEqual(20.00, c.amount)


class BaseReceiptTest(unittest.TestCase):
    def setUp(self):
        if hasattr(self, 'data'):
            self.receipt = models.Receipt(self.data)

    def test_contribution_date(self):
        if hasattr(self, 'date'):
            self.assertEqual(self.date, self.receipt.contribution.date)

    def test_contribution_amount(self):
        if not hasattr(self, 'amount'):
            return
        self.assertEqual(self.amount, self.receipt.contribution.amount)


class OutOfStatePacReceiptTest(BaseReceiptTest):
    data = SAMPLE_OUT_OF_STATE_PAC_LINE.split(',')
    date = datetime.date(2013, 7, 30)
    amount = 250.00

    def test_is_out_of_state_pac(self):
        self.assertTrue(self.receipt.is_out_of_state_pac)

    def test_fec_id(self):
        self.assertEqual('C00516500', self.receipt.fec_id)

    def test_employer_is_none(self):
        self.assertEqual(None, self.receipt.employer)

    def test_job_title_is_none(self):
        self.assertEqual(None, self.receipt.job_title)

    def test_is_travel_is_false(self):
        self.assertFalse(self.receipt.is_travel)

    def test_parent_id_is_none(self):
        self.assertEqual(None, self.receipt.parent_id)


class IndividualReceiptTestCase(BaseReceiptTest):
    data = SAMPLE_INDIVIDUAL_RECEIPT_LINE.split(',')
    date = datetime.date(2013, 8, 5)
    amount = 25.00

    def test_has_contributor(self):
        self.assertEqual(models.Contributor, self.receipt.contributor.__class__)

    def test_is_travel_is_false(self):
        self.assertFalse(self.receipt.is_travel)

    def test_is_individual(self):
        self.assertTrue(self.receipt.contributor.is_individual)

    def test_is_not_entity(self):
        self.assertFalse(self.receipt.contributor.is_entity)

    def test_is_not_out_of_state_pac(self):
        self.assertFalse(self.receipt.is_out_of_state_pac)

    def test_fec_id_is_none(self):
        self.assertEqual(None, self.receipt.fec_id)

    def test_employer(self):
        self.assertEqual('Fort Worth ISD', self.receipt.employer)

    def test_job_title(self):
        self.assertEqual('Teacher', self.receipt.job_title)

    def test_parent_id_is_none(self):
        self.assertEqual(None, self.receipt.parent_id)


class TravelReceiptTestCase(BaseReceiptTest):
    data = SAMPLE_TRAVEL_LINE.split(',')

    def test_is_travel(self):
        self.assertTrue(self.receipt.is_travel)

    def test_has_real_travel(self):
        self.assertEqual(models.Travel, self.receipt.travel.__class__)

    def test_expected_travel_values(self):
        expected = (
            ('last_name', 'Patton'),
            ('first_name', 'Robert'),
            ('title', ''),
            ('suffix', ''),
            ('means_of', 'Private airplane'),
            ('departure_location', 'Fort Worth TX'),
            ('departure_date', datetime.date(2013, 8, 5)),
            ('destination', 'Washington DC (Dulles)'),
            ('arrival_date', datetime.date(2013, 8, 5)),
            ('purpose', 'Attend National Press Club event'),
        )
        for attr, value in expected:
            self.assertEqual(value, getattr(self.receipt.travel, attr))

    def test_parent_is_none(self):
        self.assertEqual(None, self.receipt.parent)


class TravelSubReceiptTestCase(BaseReceiptTest):
    data = SAMPLE_TRAVEL_SUB_RECEIPT_LINE.split(',')

    def test_parent_id_is_set(self):
        self.assertEqual('634', self.receipt.parent_id)

    def test_id_is_a_composite(self):
        self.assertEqual('634-10', self.receipt.id)

    def test_raises_on_parent_if_no_report_is_provided(self):
        with self.assertRaises(Exception):
            self.receipt.parent

    def test_returns_parent_from_report(self):
        r = random.randint(1000, 2000)
        finder = mock.Mock(callable=True, return_value=r)
        report = mock.Mock(find=finder)
        receipt = models.Receipt(self.data, report=report)
        self.assertEqual(r, receipt.parent)
        finder.assert_called_with(id=receipt.parent_id)


class TravelTestCase(unittest.TestCase):
    def test_departure_date(self):
        t = models.Travel(departure_date='20000101')
        self.assertEqual(datetime.date(2000, 1, 1), t.departure_date)

    def test_arrival_date(self):
        t = models.Travel(arrival_date='20000101')
        self.assertEqual(datetime.date(2000, 1, 1), t.arrival_date)


def generate_mock_report():
    simple_report = [
        SAMPLE_CVR_LINE,
        SAMPLE_INDIVIDUAL_RECEIPT_LINE,
        SAMPLE_OUT_OF_STATE_PAC_LINE,
        SAMPLE_TRAVEL_LINE,
        SAMPLE_TRAVEL_SUB_RECEIPT_LINE,
    ]
    iter_lines = mock.Mock(callable=True, return_value=simple_report)
    raw_report = mock.Mock(iter_lines=iter_lines)
    return raw_report


class ReportTestCase(unittest.TestCase):
    def test_parse_is_not_called_by_default(self):
        with mock.patch.object(models.Report, 'parse') as parse:
            models.Report()
        self.assertFalse(parse.called)

    def test_parse_called_when_report_is_provided(self):
        with mock.patch.object(models.Report, 'parse') as parse:
            models.Report(raw_report='anything')
        parse.assert_any_call()


class ParsingReportTestCase(unittest.TestCase):
    def setUp(self):
        raw_report = generate_mock_report()
        self.report = models.Report(raw_report=raw_report)

    def test_buckets_are_created(self):
        self.assertEqual(1, len(self.report.buckets['CVR']))
        self.assertEqual(4, len(self.report.buckets['RCPT']))

    def test_cover_returned_as_expected(self):
        cover = self.report.cover
        self.assertEqual(models.Filer, cover.filer.__class__)
        self.assertEqual('00062095', cover.filer.filer_id)
        self.assertEqual('IND', cover.filer.filer_type)
        self.assertEqual('Wendy R.', cover.filer.first_name)
        self.assertEqual('Davis', cover.filer.last_name)

    def test_receipts_are_present(self):
        self.assertEqual(4, len(self.report.receipts))

    def test_total_receipts(self):
        self.assertEqual(8275.00, self.report.total_receipts)

        # smoke test to ensure there's an empty contribution
        receipt = self.report.get(id='634-10')
        self.assertEqual(0, receipt.contribution.amount)


class FindingReceiptsInReportTestCase(unittest.TestCase):
    def setUp(self):
        raw_report = generate_mock_report()
        self.report = models.Report(raw_report=raw_report)

    def test_returns_an_empty_list_when_unable_to_find_match(self):
        self.assertEqual([], self.report.find(id='unknown and unknowable'))

    def test_can_find_receipt_by_id(self):
        receipt = self.report.find(id='98')[0]
        self.assertEqual(25.00, receipt.contribution.amount)

    def test_returns_multiples_if_found(self):
        receipts = self.report.find(name_of_schedule='A1')
        self.assertEqual(4, len(receipts))

    def test_get_returns_one_item(self):
        receipt = self.report.get(id='98')
        self.assertEqual(25.00, receipt.contribution.amount)

    def test_raises_exception_on_multiple_find(self):
        with self.assertRaises(exceptions.MultipleFound):
            self.report.get(name_of_schedule='A1')


class UninitializedReportTestCase(unittest.TestCase):
    def setUp(self):
        self.report = models.Report()

    def test_cover_fails_when_not_parsed(self):
        with self.assertRaises(exceptions.NotYetInitialized):
            self.report.cover

    def test_receipts_fails_when_not_parsed(self):
        with self.assertRaises(exceptions.NotYetInitialized):
            self.report.receipts

    def test_find_fails_when_not_parsed(self):
        with self.assertRaises(exceptions.NotYetInitialized):
            self.report.find(id='123')

    def test_total_receipts_fails_when_not_parsed(self):
        with self.assertRaises(exceptions.NotYetInitialized):
            self.report.total_receipts
