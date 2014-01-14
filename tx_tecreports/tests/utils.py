import datetime
import random
import unittest

from .. import utils


class string_to_date_TestCase(unittest.TestCase):
    def test_turns_string_to_date(self):
        d = datetime.date(year=2000, month=1, day=1)
        self.assertEqual(d, utils.string_to_date('20000101'))

    def test_returns_none_on_bad_date(self):
        self.assertEqual(None, utils.string_to_date('202020'))

    def test_raises_ValueError_with_strict(self):
        with self.assertRaises(ValueError):
            utils.string_to_date('202020', strict=True)

    def test_returns_none_when_passed_none(self):
        self.assertEqual(None, utils.string_to_date(None))

    def test_raises_TypeError_with_strict(self):
        with self.assertRaises(TypeError):
            utils.string_to_date(None, strict=True)


class parse_num_from_string_TestCase(unittest.TestCase):
    def test_returns_none_if_no_string_is_present(self):
        example = "Report #: Foobar"
        self.assertEqual(None, utils.parse_num_from_string(example))

    def test_returns_number_when_present(self):
        report_number = 584598
        example = "Report #: %d" % report_number
        self.assertEqual(report_number, utils.parse_num_from_string(example))

    def test_returns_number_when_present_with_trailing_space(self):
        report_number = 584598
        example = "Report #: %d " % report_number
        self.assertEqual(report_number, utils.parse_num_from_string(example))

    def test_returns_number_for_corrected_report(self):
        example = "Report #: 449380 - Corrected Report"
        actual = utils.parse_num_from_string(example)
        self.assertEqual(449380, actual)


class extract_filing_date_TestCase(unittest.TestCase):
    def generate_random_date_pair(self):
        random_year = random.randint(2000, 2010)
        random_month = random.randint(1, 12)
        random_day = random.randint(1, 28)
        date = datetime.date(random_year, random_month, random_day)
        formatted_date = date.strftime("%B %d{suffix}, %Y")

        # The code parses for suffix without paying attention to its
        # validity, so just tack a random suffix on.
        r = random.randint(0, 2)
        formatted_date = formatted_date.format(suffix=["th", "st", "nd"][r])

        return ("Report Due: %s" % formatted_date, date)

    def test_extracts_date_minus_suffix(self):
        dates = (
            ("Report Due: January 15th, 2008",
                datetime.date(2008, 1, 15)),
        )

        for raw, expected in dates:
            self.assertEqual(expected, utils.extract_filing_date(raw),
                "Unable to extract %s from \"%s\"" % (expected, raw))

    def test_extracts_random_date(self):
        raw, expected = self.generate_random_date_pair()
        self.assertEqual(expected, utils.extract_filing_date(raw))

    def test_extracts_date_with_nbsp(self):
        raw = "Report Due: &nbsp; January 15th, 2008"
        expected = datetime.date(2008, 1, 15)
        self.assertEqual(expected, utils.extract_filing_date(raw))

    def test_raises_ValueError_exception_with_strict_and_invalid_date(self):
        with self.assertRaises(ValueError):
            utils.extract_filing_date('Report Due: February 30th, 2008',
                    strict=True)

    def test_raises_TypeError_wth_strict_and_no_value(self):
        with self.assertRaises(TypeError):
            utils.extract_filing_date(None, strict=True)

    def test_raises_ValueError_wth_strict_and_empty_string(self):
        with self.assertRaises(ValueError):
            utils.extract_filing_date('', strict=True)
