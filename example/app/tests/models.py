from django.test import TestCase


from tx_tecreports import models


class ContributionsByStateTestCase(TestCase):
    def test_unicode_method(self):
        obj = models.ContributionsByState(state='TX', amount=20.00, total=1)
        self.assertEqual("TX $20.00 via 1 contribution(s)", str(obj))
