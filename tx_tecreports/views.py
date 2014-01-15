import datetime
import decimal
import json

from django.http import HttpResponse
from django.views.generic import View

from . import models


# TODO: move this into a common HTTP/view library
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, datetime.date):
            return o.strftime('%m/%d/%Y')
        return super(DecimalEncoder, self).default(o)


class JSONPResponse(HttpResponse):
    def __init__(self, data, request, *args, **kwargs):
        callback = request.GET.get('callback', None)
        data = json.dumps(data, cls=DecimalEncoder)
        if callback:
            data = '%s(%s)' % (callback, data)
        kwargs['content_type'] = 'application/javascript'
        super(JSONPResponse, self).__init__(data, *args, **kwargs)


class ReportAPIView(View):
    def get(self, request, report_id, **kwargs):
        # TODO 404
        report = models.Report.objects.get(report_id=report_id)
        qs_to_dict = lambda qs: [a.as_simple_dict() for a in qs]
        data = {
            '_meta': {
                'report_id': report.report_id,
                'filer_id': report.filer_id,
                'filer_type': report.filer_type,
                'unitemized_contributions': report.unitemized_contributions,
                'total_contributions': report.total_contributions,
                'unitemized_expenditures': report.unitemized_expenditures,
                'total_expenditures': report.total_expenditures,
                'outstanding_loans': report.outstanding_loans,
                'cash_on_hand': report.cash_on_hand,
                'unitemized_pledges': report.unitemized_pledges,
                'unitemized_loans': report.unitemized_loans,
            },
            'contribs_by_state': qs_to_dict(report.stats_by_state.all()),
            'top_contribs_by_zip': qs_to_dict(
                    report.stats_by_zipcode.all()[:10]),
            'buckets': qs_to_dict(report.stats_by_amount.all()),
            'top_ten_donations': qs_to_dict(
                    report.receipts.all().order_by('-amount')[:10]),
            'contribs_by_date': qs_to_dict(report.stats_by_date.all()),
        }
        return JSONPResponse(data, request)
