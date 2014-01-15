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
            return o.strftime('%Y/%m/%d')
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
                'filer_id': 'TODO',
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
