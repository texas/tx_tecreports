import datetime


from django.test import TestCase


from tx_tecreports import models


class GenericStatsTestCase(TestCase):
    @property
    def generic_report(self):
        from_date = datetime.date(2013, 1, 1)
        through_date = datetime.date(2013, 12, 31)
        return models.Report.objects.create(report_number=0,
                from_date=from_date, through_date=through_date)

    def generate_contributor(self, **kwargs):
        t = models.ContributorType.objects.create(name='IND')
        return models.Contributor.objects.create(type_of=t, **kwargs)

    @property
    def generic_contributor(self):
        return self.generate_contributor(is_individual=True, is_entity=False)


class ContributionsByAmountManagerTestCase(GenericStatsTestCase):
    def test_is_called_on_save(self):
        self.assertEqual(0, models.ContributionsByDate.objects.count(),
                msg='sanity check')

        models.Receipt.objects.create(report=self.generic_report,
                contributor=self.generic_contributor,
                amount=20.00)

        self.assertEqual(1, models.ContributionsByAmount.objects.count())

    def test_adds_to_bucket(self):
        kwargs = {
            'contributor': self.generic_contributor,
            'report': self.generic_report,
        }
        models.Receipt.objects.create(amount=1000, **kwargs)
        models.Receipt.objects.create(amount=500, **kwargs)
        models.Receipt.objects.create(amount=5000, **kwargs)

        self.assertEqual(2, models.ContributionsByAmount.objects.count())
        bucket = models.ContributionsByAmount.objects.get(name='less_5k')
        self.assertEqual(1500, bucket.amount)
        self.assertEqual(2, bucket.total)

        bucket = models.ContributionsByAmount.objects.get(name='5k_10k')
        self.assertEqual(5000, bucket.amount)
        self.assertEqual(1, bucket.total)


class ContributionsByDateManagerTestCase(GenericStatsTestCase):
    @property
    def today(self):
        return datetime.date.today()

    def test_is_called_on_save(self):
        today = self.today
        self.assertEqual(0, models.ContributionsByDate.objects.count(),
                msg='sanity check')

        models.Receipt.objects.create(report=self.generic_report,
                contributor=self.generic_contributor,
                date=today,
                amount=20.00)

        self.assertEqual(1, models.ContributionsByDate.objects.count())

    def test_amount_is_updated(self):
        report = self.generic_report
        today = self.today
        models.Receipt.objects.create(report=report,
                contributor=self.generic_contributor,
                date=today,
                amount=20.00)

        stats = models.ContributionsByDate.objects.get(date=today)
        self.assertEqual(20.00, stats.amount,
                msg='initial amount should be 20.00')

        models.Receipt.objects.create(report=report,
                contributor=self.generic_contributor,
                date=today,
                amount=5.00)

        stats = models.ContributionsByDate.objects.get(date=today)
        self.assertEqual(25.00, stats.amount, msg='now amount should be 25.00')

        models.Receipt.objects.create(report=report,
                contributor=self.generic_contributor,
                date=today - datetime.timedelta(days=1),
                amount=5.00)
        stats = models.ContributionsByDate.objects.get(date=today)
        self.assertEqual(25.00, stats.amount,
                msg='amount is still 25.00 after another state')

    def test_total_is_updated(self):
        today = self.today
        report = self.generic_report
        models.Receipt.objects.create(report=report,
                contributor=self.generic_contributor,
                date=today,
                amount=20.00)

        stats = models.ContributionsByDate.objects.get(date=today)
        self.assertEqual(1, stats.total, msg='total should be 1')

        models.Receipt.objects.create(report=report,
                contributor=self.generic_contributor,
                date=today,
                amount=5.00)

        stats = models.ContributionsByDate.objects.get(date=today)
        self.assertEqual(2, stats.total, msg='now total should be 2')

        models.Receipt.objects.create(report=report,
                contributor=self.generic_contributor,
                date=today - datetime.timedelta(days=1),
                amount=5.00)
        stats = models.ContributionsByDate.objects.get(date=today)
        self.assertEqual(2, stats.total,
                msg='total is still 2 after another state')


class ContributionsByStateManagerTestCase(GenericStatsTestCase):
    @property
    def generic_oklahoma_contributor(self):
        return self.generate_contributor(is_individual=True, is_entity=False,
                state='OK')

    @property
    def generic_texas_contributor(self):
        return self.generate_contributor(is_individual=True, is_entity=False,
                state='TX')

    def test_is_called_on_save(self):
        self.assertEqual(0, models.ContributionsByState.objects.count(),
                msg='sanity check')

        models.Receipt.objects.create(report=self.generic_report,
                contributor=self.generic_texas_contributor,
                amount=20.00)

        self.assertEqual(1, models.ContributionsByState.objects.count())

    def test_amount_is_updated(self):
        report = self.generic_report
        models.Receipt.objects.create(report=report,
                contributor=self.generic_texas_contributor,
                amount=20.00)

        contribution = models.ContributionsByState.objects.get(state='TX')
        self.assertEqual(20.00, contribution.amount,
                msg='initial amount should be 20.00')

        models.Receipt.objects.create(report=report,
                contributor=self.generic_texas_contributor,
                amount=5.00)

        contribution = models.ContributionsByState.objects.get(state='TX')
        self.assertEqual(25.00, contribution.amount,
                msg='now amount should be 25.00')

        models.Receipt.objects.create(report=report,
                contributor=self.generic_oklahoma_contributor,
                amount=5.00)
        contribution = models.ContributionsByState.objects.get(state='TX')
        self.assertEqual(25.00, contribution.amount,
                msg='amount is still 25.00 after another state')

    def test_total_is_updated(self):
        report = self.generic_report
        models.Receipt.objects.create(report=report,
                contributor=self.generic_texas_contributor,
                amount=20.00)

        contribution = models.ContributionsByState.objects.get(state='TX')
        self.assertEqual(1, contribution.total,
                msg='total should be 1')

        models.Receipt.objects.create(report=report,
                contributor=self.generic_texas_contributor,
                amount=5.00)

        contribution = models.ContributionsByState.objects.get(state='TX')
        self.assertEqual(2, contribution.total,
                msg='now total should be 2')

        models.Receipt.objects.create(report=report,
                contributor=self.generic_oklahoma_contributor,
                amount=5.00)
        contribution = models.ContributionsByState.objects.get(state='TX')
        self.assertEqual(2, contribution.total,
                msg='total is still 2 after another state')


class ContributionsByZipcodeManagerTestCase(GenericStatsTestCase):
    @property
    def generic_south_austin_contributor(self):
        return self.generate_contributor(is_individual=True, is_entity=False,
                zipcode=78704)

    @property
    def generic_east_austin_contributor(self):
        return self.generate_contributor(is_individual=True, is_entity=False,
                zipcode=78702)

    def test_is_called_on_save(self):
        self.assertEqual(0, models.ContributionsByZipcode.objects.count(),
                msg='sanity check')

        models.Receipt.objects.create(report=self.generic_report,
                contributor=self.generic_east_austin_contributor,
                amount=20.00)

        self.assertEqual(1, models.ContributionsByZipcode.objects.count())

    def test_amount_is_updated(self):
        report = self.generic_report
        models.Receipt.objects.create(report=report,
                contributor=self.generic_east_austin_contributor,
                amount=20.00)

        stats = models.ContributionsByZipcode.objects.get(zipcode='78702')
        self.assertEqual(20.00, stats.amount,
                msg='initial amount should be 20.00')

        models.Receipt.objects.create(report=report,
                contributor=self.generic_east_austin_contributor,
                amount=5.00)

        stats = models.ContributionsByZipcode.objects.get(zipcode='78702')
        self.assertEqual(25.00, stats.amount, msg='now amount should be 25.00')

        models.Receipt.objects.create(report=report,
                contributor=self.generic_south_austin_contributor,
                amount=5.00)
        stats = models.ContributionsByZipcode.objects.get(zipcode='78702')
        self.assertEqual(25.00, stats.amount,
                msg='amount is still 25.00 after another state')

    def test_total_is_updated(self):
        report = self.generic_report
        models.Receipt.objects.create(report=report,
                contributor=self.generic_east_austin_contributor,
                amount=20.00)

        stats = models.ContributionsByZipcode.objects.get(zipcode='78702')
        self.assertEqual(1, stats.total, msg='total should be 1')

        models.Receipt.objects.create(report=report,
                contributor=self.generic_east_austin_contributor,
                amount=5.00)

        stats = models.ContributionsByZipcode.objects.get(zipcode='78702')
        self.assertEqual(2, stats.total, msg='now total should be 2')

        models.Receipt.objects.create(report=report,
                contributor=self.generic_south_austin_contributor,
                amount=5.00)
        stats = models.ContributionsByZipcode.objects.get(zipcode='78702')
        self.assertEqual(2, stats.total,
                msg='total is still 2 after another state')
