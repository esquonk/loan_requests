# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan_requests', '0002_bank_user_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestFieldChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='\u0422\u0435\u043a\u0441\u0442')),
                ('field', models.ForeignKey(related_name='choices', to='loan_requests.RequestField')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='requesttypefield',
            name='field_group',
            field=models.CharField(help_text='\u041e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u043e \u0442\u043e\u043b\u044c\u043a\u043e \u043e\u0434\u043d\u043e \u043f\u043e\u043b\u0435 \u0438\u0437 \u0433\u0440\u0443\u043f\u043f\u044b', max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0433\u0440\u0443\u043f\u043f\u044b \u043f\u043e\u043b\u0435\u0439', blank=True),
            preserve_default=True,
        ),
    ]
