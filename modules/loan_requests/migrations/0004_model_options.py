# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan_requests', '0003_request_field_changes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='requestfieldchoice',
            options={'ordering': ('text',), 'verbose_name': '\u0412\u0430\u0440\u0438\u0430\u043d\u0442 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f \u043f\u043e\u043b\u044f', 'verbose_name_plural': '\u0412\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f \u043f\u043e\u043b\u044f'},
        ),
        migrations.AlterModelOptions(
            name='requesttypefield',
            options={'verbose_name': '\u041f\u043e\u043b\u0435 \u0442\u0438\u043f\u0430 \u0437\u0430\u044f\u0432\u043a\u0438', 'verbose_name_plural': '\u041f\u043e\u043b\u044f \u0442\u0438\u043f\u0430 \u0437\u0430\u044f\u0432\u043a\u0438'},
        ),
        migrations.AlterField(
            model_name='requesttypefield',
            name='field_group',
            field=models.CharField(help_text='\u041e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u043e \u0434\u043b\u044f \u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f \u0431\u0443\u0434\u0435\u0442 \u0445\u043e\u0442\u044f \u0431\u044b \u043e\u0434\u043d\u043e \u043f\u043e\u043b\u0435 \u0438\u0437 \u0433\u0440\u0443\u043f\u043f\u044b', max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0433\u0440\u0443\u043f\u043f\u044b \u043f\u043e\u043b\u0435\u0439', blank=True),
            preserve_default=True,
        ),
    ]
