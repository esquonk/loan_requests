# coding: utf-8
from __future__ import unicode_literals
from collections import defaultdict
from rest_framework.exceptions import ValidationError

from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.relations import StringRelatedField, PrimaryKeyRelatedField

from loan_requests.models import Request, RequestType, RequestField, RequestTypeField


class RequestContentSerializer(Serializer):
    def make_fields(self, request_type):
        for f in request_type.fields.all():
            self.fields[f.field.name] = f.get_rest_field()

    def get_attribute(self, obj):
        return obj

    def get_value(self, dictionary):
        rt_id = dictionary.get('request_type')
        request_type = None
        if rt_id:
            try:
                request_type = RequestType.objects.get(id=rt_id)
            except RequestType.DoesNotExist:
                pass
        else:
            if self.parent.instance:
                request_type = self.parent.instance.request_type

        if request_type:
            self.make_fields(request_type)

        return super(RequestContentSerializer, self).get_value(dictionary)

    def to_representation(self, instance):
        request_type = instance.request_type

        if request_type:
            self.make_fields(request_type)

        return super(RequestContentSerializer, self).to_representation(getattr(instance, self.field_name))

    def to_internal_value(self, data):
        val = super(RequestContentSerializer, self).to_internal_value(data)
        return val

    def validate(self, data):
        rt_id = self.parent.initial_data['request_type']
        request_type = None

        if rt_id:
            try:
                request_type = RequestType.objects.get(id=rt_id)
            except RequestType.DoesNotExist:
                pass
        else:
            if self.parent.instance:
                request_type = self.parent.instance.request_type

        if request_type:
            field_groups = defaultdict(list)
            for f in request_type.fields.all():
                if f.field_group:
                    field_groups[f.field_group].append(f.field.name)

            for field_group, fields in field_groups.iteritems():
                for field in fields:
                    if data.get(field):
                        break
                else:
                    raise ValidationError(
                        'Обязательно для заполнения хотя бы одно из полей: {}'.format(', '.join(fields))
                    )

        return data


class RequestFieldSerializer(ModelSerializer):
    class Meta:
        model = RequestField
        fields = (
            'name',
            'title',
            'field_type',
            'choices',
            'description',
        )

    choices = StringRelatedField(many=True)


class RequestTypeFieldSerializer(ModelSerializer):
    class Meta:
        model = RequestTypeField
        fields = (
            'id',
            'required',
            'field_group',
            'field',
        )

    field = RequestFieldSerializer()


class RequestTypeSerializer(ModelSerializer):
    class Meta:
        model = RequestType
        fields = (
            'id',
            'title',
            'fields',
        )

    fields = RequestTypeFieldSerializer(many=True)


class RequestSerializer(ModelSerializer):
    class Meta:
        model = Request
        fields = (
            'id',
            'user',
            'request_type',
            'content',
        )

    content = RequestContentSerializer()

    request_type = PrimaryKeyRelatedField(queryset=RequestType.objects.all())
    user = StringRelatedField()

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        req = Request.objects.create(**validated_data)
        return req

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance