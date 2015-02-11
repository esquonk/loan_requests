# coding: utf-8
from __future__ import unicode_literals

from .common import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'loan_requests',
        'USER': 'loan_requests',
        'PASSWORD': 'loan_requests',
    }
}