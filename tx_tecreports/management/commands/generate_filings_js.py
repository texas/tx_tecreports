import csv
import datetime
import json
import logging
from optparse import make_option

from django.core.management.base import BaseCommand

from ...fetcher import get_filings_list

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--filename', action='store', dest='filename',
                default='./data/curated-statewide-candidates-2014.csv',
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

    def generate_object(self, record, order, filer_id_key='tecid',
            filer_type='', **kwargs):
        filing = self.get_matching_filing(record[filer_id_key], **kwargs)
        if filing is None:
            return

        return {
            'display_name': record['name'],
            'type': filer_type,
            'race': record['race'],
            'party': record['party'],
            'filer_id': record[filer_id_key],
            'order': order,
            'report_id': filing.report_id,
        }

    def handle(self, filename, raw_report_due, **kwargs):
        report_due = (datetime.datetime.strptime(raw_report_due, '%Y/%m/%d')
                .date())

        reader = csv.DictReader(open(filename, 'rb'))
        data = []
        for record in reader:
            logger.info('Fetching for %s' % record['name'])
            if record['tecid'] == '00032876':
                logger.warn("Skipping %s because it's not properly formatted" %
                        record['tecid'])
                continue

            obj = self.generate_object(record, record['new_order'],
                    report_due=report_due)
            if obj:
                data.append(obj)

            if record['tecpacid']:
                logger.info('Fetching SPAC for %s' % record['name'])
                obj = self.generate_object(record, int(record['new_order']) + 1,
                        'tecpacid', filer_type='(SPAC)', report_due=report_due)
                if obj:
                    data.append(obj)
        print json.dumps(data)
