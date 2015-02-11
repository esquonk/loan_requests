# coding: utf-8
from __future__ import unicode_literals
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.routers import SimpleRouter
from loan_requests.api.permissions import RequestPermission

from loan_requests.models import Request, RequestType

from .serializers import RequestSerializer, RequestTypeSerializer


class RequestTypeViewSet(ReadOnlyModelViewSet):
    model = RequestType
    queryset = RequestType.objects.all()
    serializer_class = RequestTypeSerializer


class RequestViewSet(ModelViewSet):
    model = Request
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    permission_classes = (
        IsAuthenticated,
        RequestPermission,
    )

    def get_queryset(self):
        queryset = Request.objects.all()
        user = self.request.user

        if not user.has_perm('loan_requests.view_all_requests'):
            queryset = queryset.filter(user=user)

        return queryset