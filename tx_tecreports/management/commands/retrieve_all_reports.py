import csv
import datetime
import logging
from optparse import make_option

from django.core.management.base import BaseCommand

from ...fetcher import get_filings_list

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--filename', action='store', dest='filename',
                help='File to use parse tecid and tecpacid from'),
        make_option('--report-due', action='store', dest='raw_report_due',
                help='Report due date of filing to parse (format: YYYY/MM/DD)'),
    )

    def get_matching_filing(self, filer_id, **kwargs):
        logger.debug('fetching filings for %s' % filer_id)
        filing_list = get_filings_list(filer_id)

        logger.debug('found %d total filings' % len(filing_list))
        matching_filings = filing_list.find(**kwargs)
        matching_filings_len = len(matching_filings)
        logger.debug('found %d matching filings' % matching_filings_len)

        if matching_filings_len > 1:
            logger.warning('Unable to process %s' % filer_id)
            return
        if matching_filings_len is 0:
            logger.warning('Unable to find any filings for %s' % kwargs)
            return
        return matching_filings[0]

    def fetch_and_save(self, filer_id, **kwargs):
        logger.info('finding filing for %s' % filer_id)
        filing = self.get_matching_filing(filer_id, **kwargs)
        if filing:
            try:
                filing.report.save()
                logger.info('found %s and saved' % filer_id)
            except KeyError:
                logger.warn('KeyError on filing for %s' % filer_id)

    def handle(self, filename, raw_report_due, **kwargs):
        logger.debug('processing %s' % filename)

        reader = csv.DictReader(open(filename, 'rb'))
        report_due = datetime.datetime.strptime(raw_report_due, '%Y/%m/%d').date()

        for record in reader:
            # This report is known to be a malformed CSV
            if record['tecid'] == '00032876':
                logger.warn("Skipping %s because it's not properly formatted" %
                        record['tecid'])
                continue
            self.fetch_and_save(record['tecid'], report_due=report_due)
            if record['tecpacid']:
                self.fetch_and_save(record['tecpacid'], report_due=report_due)
