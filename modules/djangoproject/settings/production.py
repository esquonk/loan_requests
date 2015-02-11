# coding: utf-8
from __future__ import unicode_literals

from .common import *

SITE_ROOT = '/srv/loan_requests'

DEBUG = False
TEMPLATE_DEBUG = False

STATIC_ROOT = SITE_ROOT + '/static'

ALLOWED_HOSTS = (
    'localhost',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '127.0.0.1',
        'NAME': 'loan_requests',
        'USER': 'loan_requests',
        'PASSWORD': 'loan_requests',
    }
}