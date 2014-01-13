import datetime
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
