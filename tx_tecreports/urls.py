from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^api/v1/report/(?P<report_id>[^/]+)/$',
            views.ReportAPIView.as_view(), name='report_api'),
)
