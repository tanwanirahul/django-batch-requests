from django.conf.urls import url
from tests.test_views import (EchoHeaderView, ExceptionView, SimpleView,
                              SleepingView)

from batch_requests.views import handle_batch_requests

urlpatterns = [
               url(r'^views/', SimpleView.as_view(), name="simpleview"),
               url(r'^echo/', EchoHeaderView.as_view(), name="echoheader"),
               url(r'^exception/', ExceptionView.as_view(), name="exceptionview"),
               url(r'^sleep/', SleepingView.as_view(), name="sleepingview"),
               url(r'^api/v1/batch/', handle_batch_requests, name="batch"),
]
