import datetime

from django.test import TestCase


from tx_tecreports import models


class ContributionsByAmountTestCase(TestCase):
    def test_unicode_method(self):
        obj = models.ContributionsByAmount(name='less_5k', amount=20.00,
                total=1)
        self.assertEqual('less_5k $20.00 via 1 contribution(s)', str(obj))


class ContributionsByDateTestCase(TestCase):
    def test_unicode_method(self):
        today = datetime.date.today()
        obj = models.ContributionsByDate(date=today, amount=20.00,
                total=1)
        self.assertEqual('{date} $20.00 via 1 contribution(s)'.format(
                date=today), str(obj))


class ContributionsByStateTestCase(TestCase):
    def test_unicode_method(self):
        obj = models.ContributionsByState(state='TX', amount=20.00, total=1)
        self.assertEqual("TX $20.00 via 1 contribution(s)", str(obj))


class ContributionsByZipcodeTestCase(TestCase):
    def test_unicode_method(self):
        obj = models.ContributionsByZipcode(zipcode='78702', amount=20.00, total=1)
        self.assertEqual("78702 $20.00 via 1 contribution(s)", str(obj))
