# coding: utf-8
from __future__ import unicode_literals

from django.contrib import admin

from loan_requests.models import RequestType, RequestField, RequestTypeField, Request, RequestFieldChoice


class RequestFieldChoiceInline(admin.TabularInline):
    model = RequestFieldChoice
    extra = 5


class RequestTypeFieldInline(admin.TabularInline):
    model = RequestTypeField
    extra = 10


class RequestFieldAdmin(admin.ModelAdmin):
    inlines = (RequestFieldChoiceInline, )


class RequestTypeAdmin(admin.ModelAdmin):
    inlines = (RequestTypeFieldInline, )


class RequestAdmin(admin.ModelAdmin):
    pass

admin.site.register(RequestType, RequestTypeAdmin)
admin.site.register(RequestField, RequestFieldAdmin)
admin.site.register(Request, RequestAdmin)