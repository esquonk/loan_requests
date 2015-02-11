# coding: utf-8
from __future__ import unicode_literals

from rest_framework.permissions import BasePermission, SAFE_METHODS


class RequestPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True

        if request.method in SAFE_METHODS and request.user.has_perm('loan_requests.view_all_requests'):
            return True

        if request.method in ('PUT', 'PATCH') and request.user.has_perm('loan_requests.edit_all_requests'):
            return True

        if request.method == 'DELETE' and request.user.has_perm('loan_requests.delete_all_requests'):
            return True

        return False
