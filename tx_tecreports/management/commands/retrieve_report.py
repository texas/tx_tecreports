from django.core.management.base import BaseCommand

from ...fetcher import get_report


class Command(BaseCommand):
    def handle(self, report_id, **kwargs):
        report = get_report(report_id)
        report.save()
