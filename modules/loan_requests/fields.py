# coding: utf-8
from __future__ import unicode_literals
from collections import defaultdict

import dateutil.parser

from jsonfield import JSONField


class JSONBField(JSONField):
    def db_type(self, connection):
        return 'jsonb'


class ContentField(JSONBField):
    def to_python(self, value):
        value = super(ContentField, self).to_python(value)

        if not value:
            return value

        res = defaultdict(lambda: None)
        for k, item in value.iteritems():
            if isinstance(item, dict):
                val = item['value']
                t = item['type']
                if t == 'datetime':
                    val = dateutil.parser.parse(val)
                elif t == 'date':
                    val = dateutil.parser.parse(val).date()
            else:
                val = item

            res[k] = val

        return res

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def get_prep_value(self, value):
        res = {}

        if not value is None:
            for key, val in value.iteritems():
                res[key] = {
                    'type': type(val).__name__,
                    'value': val
                }

        return super(ContentField, self).get_prep_value(res)
