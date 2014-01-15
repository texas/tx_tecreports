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


class ContributionsByAmountManager(AsSimpleDictMixin, models.Manager):
    use_for_related_fields = True

    def denormalize(self, sender, instance=None, **kwargs):
        if instance is None or not instance.amount:
            return
        found = False

        for bucket in AMOUNT_BUCKETS:
            if (instance.amount >= bucket['low']
                    and instance.amount <= bucket['high']):
                found = True
                break
        if not found:
            raise Exception("WTF?")
        # import ipdb; ipdb.set_trace()
        stats, created = self.model.objects.get_or_create(
                report=instance.report, **bucket)
        stats.refresh_stats(report=instance.report)
        stats.save()


class ContributionsByDateManager(AsSimpleDictMixin, models.Manager):
    use_for_related_fields = True

    def denormalize(self, sender, instance=None, **kwargs):
        if instance is None or not instance.date:
            return
        stats, created = self.model.objects.get_or_create(date=instance.date,
                report=instance.report)
        stats.refresh_stats(report=instance.report)
        stats.save()


class ContributionByZipcodeManager(AsSimpleDictMixin, models.Manager):
    use_for_related_fields = True

    def denormalize(self, sender, instance=None, **kwargs):
        if instance is None or not instance.contributor.zipcode:
            return
        stats, created = self.model.objects.get_or_create(
                report=instance.report, zipcode=instance.contributor.zipcode)
        stats.refresh_stats(report=instance.report)
        stats.save()


class ContributionByStateManager(AsSimpleDictMixin, models.Manager):
    use_for_related_fields = True

    def denormalize(self, sender, instance=None, **kwargs):
        if instance is None or not instance.contributor.state:
            return
        stats, created = self.model.objects.get_or_create(
                state=instance.contributor.state, report=instance.report)
        stats.refresh_stats(report=instance.report)
        stats.save()
