# coding: utf-8
from __future__ import unicode_literals
import re
from rest_framework.exceptions import ValidationError

from rest_framework.fields import CharField, DateField, IntegerField, DecimalField, BooleanField, DateTimeField, \
    FloatField, NullBooleanField


class FieldTypeRegistry(object):
    def __init__(self):
        self.fields = {}

    def register(self, cls):
        self.fields[cls.name] = cls

    def get_choices(self):
        return [(key, f.title) for key, f in self.fields.iteritems()]

    def __getitem__(self, item):
        return self.fields[item]

registry = FieldTypeRegistry()


class FieldTypeMeta(type):
    def __new__(cls, names, bases, attrs):
        if names != 'FieldType' and not attrs.get('name'):
            attrs['name'] = unicode(names.lower())

        return super(FieldTypeMeta, cls).__new__(cls, names, bases, attrs)

    def __init__(cls, names, bases, attrs):
        super(FieldTypeMeta, cls).__init__(names, bases, attrs)
        if names != 'FieldType':
            registry.register(cls)


class FieldType(object):
    __metaclass__ = FieldTypeMeta
    name = None
    rest_class = None

    def get_rest_field(self, *args, **kw):
        if 'required' in kw and issubclass(self.rest_class, CharField):
            kw['allow_blank'] = not kw['required']
        return self.rest_class(*args, **kw)


class String(FieldType):
    title = 'Строка'
    rest_class = CharField


class Text(FieldType):
    title = 'Текст'
    rest_class = CharField


class Date(FieldType):
    title = 'Дата'
    rest_class = DateField


class DateTime(FieldType):
    title = 'Дата/время'
    rest_class = DateTimeField


class INN(String):
    title = 'ИНН'

    class INNField(CharField):
        class INNValidator(object):
            inn_regex = re.compile(r'^\d{10}$|^\d{12}$')

            def __call__(self, value):
                if self.inn_regex.match(value) is None:
                    raise ValidationError('Неправильный формат ИНН, должно быть 10 или 12 цифр')

                return value

        validators = (
            INNValidator(),
        )

    rest_class = INNField


class Passport(String):
    title = 'Паспорт'

    class PassportField(CharField):
        pass

    rest_class = PassportField


class Phone(String):
    title = 'Телефон'

    class PhoneField(CharField):
        pass

    rest_class = PhoneField


class Integer(FieldType):
    title = 'Целое число'
    rest_class = IntegerField


class Float(FieldType):
    title = 'Вещественное число'
    rest_class = FloatField


class Boolean(FieldType):
    title = 'Да/нет'

    def get_rest_field(self, *args, **kw):
        allow_null = kw.pop('allow_null', False)
        if allow_null:
            klass = NullBooleanField
        else:
            klass = BooleanField
        return klass(*args, **kw)

