import decimal

from django.db import models


AMOUNT_BUCKETS = [
    {'name': 'less_5k', 'low': decimal.Decimal('0'), 'high': decimal.Decimal('4999.99')},
    {'name': '5k_10k', 'low': decimal.Decimal('5000'), 'high': decimal.Decimal('9999.99')},
    {'name': '10k_20k', 'low': decimal.Decimal('10000'), 'high': decimal.Decimal('19999.99')},
    {'name': '20k_50k', 'low': decimal.Decimal('20000'), 'high': decimal.Decimal('49999.99')},
    {'name': '50k_100k', 'low': decimal.Decimal('50000'), 'high': decimal.Decimal('99999.99')},
    {'name': 'more_100k', 'low': decimal.Decimal('100000'), 'high': decimal.Decimal('1000000000')},
]


class AsSimpleDictMixin(object):
    def as_simple_dict(self):
        return [a.as_simple_dict() for a in self]


class StatsManager(object):
    def update_stats(self, **kwargs):
        report = kwargs['report']
        if report.is_being_processed:
            return
        stats, created = self.model.objects.get_or_create(**kwargs)
        stats.refresh_stats(report=report)
        stats.save()
        return stats


class ContributionsByAmountManager(AsSimpleDictMixin, StatsManager,
        models.Manager):
    use_for_related_fields = True

    def full_denormalize(self, report):
        for bucket in AMOUNT_BUCKETS:
            self.update_stats(report=report, **bucket)

    def denormalize(self, sender, instance=None, **kwargs):
        if (instance is None or not instance.amount
                or instance.report.is_being_processed):
            return
        found = False

        for bucket in AMOUNT_BUCKETS:
            if (instance.amount >= bucket['low']
                    and instance.amount <= bucket['high']):
                found = True
                break
        if not found:
            raise Exception("WTF?")
        self.update_stats(report=instance.report, **bucket)


class ContributionsByDateManager(AsSimpleDictMixin, StatsManager,
        models.Manager):
    use_for_related_fields = True

    def full_denormalize(self, report):
        dates = (report.receipts
                .exclude(date=None)
                .values('date')
                .annotate(total=models.Count('id')))
        for record in dates:
            self.update_stats(report=report, date=record['date'])

    def denormalize(self, sender, instance=None, **kwargs):
        if instance is None or not instance.date:
            return
        self.update_stats(report=instance.report, date=instance.date)


class ContributionByZipcodeManager(AsSimpleDictMixin, StatsManager,
        models.Manager):
    use_for_related_fields = True

    def _full_denormalize(self, report):
        zipcodes = (report.receipts
                .exclude(contributor__zipcode_short=None)
                .values('contributor__zipcode_short')
                .annotate(total=models.Count('id')))
        for record in zipcodes:
            self.update_stats(report=report,
                    zipcode=record['contributor__zipcode_short'])

    def denormalize(self, sender, instance=None, **kwargs):
        if instance is None or not instance.contributor.zipcode_short:
            return
        self.update_stats(report=instance.report,
                zipcode=instance.contributor.zipcode_short)


class ContributionByStateManager(AsSimpleDictMixin, StatsManager,
        models.Manager):
    use_for_related_fields = True

    def full_denormalize(self, report):
        states = (report.receipts
                .exclude(contributor__state=None)
                .values('contributor__state')
                .annotate(total=models.Count('id')))
        for record in states:
            self.update_stats(report=report, state=record['contributor__state'])

    def denormalize(self, sender, instance=None, **kwargs):
        if (instance is None or not instance.contributor.state
                or instance.report.is_being_processed):
            return
        self.update_stats(state=instance.contributor.state,
                report=instance.report)
