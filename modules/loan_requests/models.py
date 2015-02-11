# coding: utf-8
from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

from rest_framework.fields import ChoiceField

from loan_requests.contents import registry as field_registry
from loan_requests.fields import ContentField


class RequestField(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='Системное имя',
                            blank=False)

    title = models.CharField(max_length=200,
                             verbose_name='Пользовательское имя',
                             blank=False)

    field_type = models.CharField(max_length=50,
                                  verbose_name='Тип поля',
                                  choices=field_registry.get_choices(),
                                  blank=False)

    description = models.TextField(verbose_name='Описание',
                                   blank=True)

    class Meta:
        verbose_name = 'Поле заявки'
        verbose_name_plural = 'Поля заявки'
        ordering = ('title',)

    def __unicode__(self):
        return self.title

    def get_field_type(self):
        return field_registry[self.field_type]()


class RequestFieldChoice(models.Model):
    field = models.ForeignKey(RequestField, related_name='choices')
    text = models.TextField(verbose_name='Текст', blank=False)

    class Meta:
        verbose_name = 'Вариант значения поля'
        verbose_name_plural = 'Варианты значения поля'
        ordering = ('text',)

    def __unicode__(self):
        return self.text

class RequestType(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Название')

    class Meta:
        verbose_name = 'Тип заявки'
        verbose_name_plural = 'Типы заявок'
        ordering = ('title',)

    def __unicode__(self):
        return self.title


class RequestTypeField(models.Model):
    request_type = models.ForeignKey(RequestType, related_name='fields')
    field = models.ForeignKey(RequestField)

    required = models.BooleanField(verbose_name='Обязательное поле',
                                   blank=False,
                                   default=True)

    field_group = models.CharField(verbose_name='Название группы полей',
                                   help_text='Обязательно для заполнения будет хотя бы одно поле из группы',
                                   blank=True,
                                   max_length=100)


    def __unicode__(self):
        return '{}: {}'.format(self.request_type, self.field)

    def get_rest_field(self):
        required = self.required and not self.field_group
        args = {
            'required': required,
            'allow_null': not required,
            }

        choices = self.field.choices.all()
        if choices:
            args['choices'] = [x.text for x in choices]
            return ChoiceField(**args)
        else:
            return self.get_field_type().get_rest_field(**args)

    def get_field_type(self):
        return self.field.get_field_type()

    class Meta:
        verbose_name = 'Поле типа заявки'
        verbose_name_plural = 'Поля типа заявки'


class Request(models.Model):
    user = models.ForeignKey(User, null=False)
    request_type = models.ForeignKey(RequestType, null=False)
    content = ContentField(verbose_name='Поля заявки')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        permissions = (
            ('view_all_requests', 'Просмотр всех заявок'),
            ('edit_all_requests', 'Редактирование всех заявок'),
            ('delete_all_requests', 'Удаление всех заявок'),
        )

    def __unicode__(self):
        return '{}: {}'.format(self.request_type, self.id)