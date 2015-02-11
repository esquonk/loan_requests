# coding: utf-8
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from loan_requests.api.views import RequestViewSet, RequestTypeViewSet

router = DefaultRouter()
router.register('request_type', RequestTypeViewSet)
router.register('request', RequestViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]