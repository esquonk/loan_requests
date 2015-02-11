# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

permissions = (
    ('view_all_requests', 'Просмотр всех заявок'),
    ('edit_all_requests', 'Редактирование всех заявок'),
    ('delete_all_requests', 'Удаление всех заявок'),
)

def add_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model("auth","Permission")
    ContentType = apps.get_model('contenttypes', 'ContentType')

    ct = ContentType.objects.get_or_create(app_label='loan_requests',
                                           model='request',
                                           name='Заявка',
                                           )[0]


    group = Group(name='Сотрудники банка')
    group.save()
    for codename, name in permissions:
        group.permissions.add(
            Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=ct
            )[0]
        )

class Migration(migrations.Migration):

    dependencies = [
        ('loan_requests', '0001_initial'),
        ('auth', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_group)
    ]
