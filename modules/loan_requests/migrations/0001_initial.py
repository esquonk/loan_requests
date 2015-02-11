# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import loan_requests.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', loan_requests.fields.ContentField(default=dict, verbose_name='\u041f\u043e\u043b\u044f \u0437\u0430\u044f\u0432\u043a\u0438')),
            ],
            options={
                'verbose_name': '\u0417\u0430\u044f\u0432\u043a\u0430',
                'verbose_name_plural': '\u0417\u0430\u044f\u0432\u043a\u0438',
                'permissions': (('view_all_requests', '\u041f\u0440\u043e\u0441\u043c\u043e\u0442\u0440 \u0432\u0441\u0435\u0445 \u0437\u0430\u044f\u0432\u043e\u043a'), ('edit_all_requests', '\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u0432\u0441\u0435\u0445 \u0437\u0430\u044f\u0432\u043e\u043a'), ('delete_all_requests', '\u0423\u0434\u0430\u043b\u0435\u043d\u0438\u0435 \u0432\u0441\u0435\u0445 \u0437\u0430\u044f\u0432\u043e\u043a')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequestField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u0421\u0438\u0441\u0442\u0435\u043c\u043d\u043e\u0435 \u0438\u043c\u044f')),
                ('title', models.CharField(max_length=200, verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u0441\u043a\u043e\u0435 \u0438\u043c\u044f')),
                ('field_type', models.CharField(max_length=50, verbose_name='\u0422\u0438\u043f \u043f\u043e\u043b\u044f', choices=[('string', '\u0421\u0442\u0440\u043e\u043a\u0430'), ('text', '\u0422\u0435\u043a\u0441\u0442'), ('float', '\u0412\u0435\u0449\u0435\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0435 \u0447\u0438\u0441\u043b\u043e'), ('datetime', '\u0414\u0430\u0442\u0430/\u0432\u0440\u0435\u043c\u044f'), ('phone', '\u0422\u0435\u043b\u0435\u0444\u043e\u043d'), ('inn', '\u0418\u041d\u041d'), ('boolean', '\u0414\u0430/\u043d\u0435\u0442'), ('passport', '\u041f\u0430\u0441\u043f\u043e\u0440\u0442'), ('date', '\u0414\u0430\u0442\u0430'), ('integer', '\u0426\u0435\u043b\u043e\u0435 \u0447\u0438\u0441\u043b\u043e')])),
                ('description', models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': '\u041f\u043e\u043b\u0435 \u0437\u0430\u044f\u0432\u043a\u0438',
                'verbose_name_plural': '\u041f\u043e\u043b\u044f \u0437\u0430\u044f\u0432\u043a\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequestType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': '\u0422\u0438\u043f \u0437\u0430\u044f\u0432\u043a\u0438',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0437\u0430\u044f\u0432\u043e\u043a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequestTypeField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('required', models.BooleanField(default=True, verbose_name='\u041e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0435 \u043f\u043e\u043b\u0435')),
                ('field', models.ForeignKey(to='loan_requests.RequestField')),
                ('request_type', models.ForeignKey(related_name='fields', to='loan_requests.RequestType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='request',
            name='request_type',
            field=models.ForeignKey(to='loan_requests.RequestType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
