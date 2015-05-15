# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Closure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=32, verbose_name='user')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='date')),
                ('num_e500', models.IntegerField(default=0, verbose_name='500 euro')),
                ('num_e200', models.IntegerField(default=0, verbose_name='200 euro')),
                ('num_e100', models.IntegerField(default=0, verbose_name='100 euro')),
                ('num_e50', models.IntegerField(default=0, verbose_name='50 euro')),
                ('num_e20', models.IntegerField(default=0, verbose_name='20 euro')),
                ('num_e10', models.IntegerField(default=0, verbose_name='10 euro')),
                ('num_e5', models.IntegerField(default=0, verbose_name='5 euro')),
                ('num_e2', models.IntegerField(default=0, verbose_name='2 euro')),
                ('num_e1', models.IntegerField(default=0, verbose_name='1 euro')),
                ('num_e050', models.IntegerField(default=0, verbose_name='50 eurocent')),
                ('num_e020', models.IntegerField(default=0, verbose_name='20 eurocent')),
                ('num_e010', models.IntegerField(default=0, verbose_name='10 eurocent')),
                ('num_e005', models.IntegerField(default=0, verbose_name='5 eurocent')),
                ('total',
                 models.FloatField(default=0, verbose_name='total register content', editable=False, blank=True)),
                ('pin', models.FloatField(default=0, verbose_name='pin receipt')),
                ('transactions_pin',
                 models.FloatField(default=0, verbose_name='pin transactions', editable=False, blank=True)),
                ('transactions_cash',
                 models.FloatField(default=0, verbose_name='cash transactions', editable=False, blank=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('finished', models.BooleanField(default=False, verbose_name='finished')),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'closure',
                'verbose_name_plural': 'closures',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=32, verbose_name='user')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('amount', models.FloatField(verbose_name='amount')),
                ('description', models.TextField(verbose_name='description')),
                ('valid', models.BooleanField(default=True, verbose_name='valid')),
                ('method', models.CharField(default=b'C', max_length=1, verbose_name='method',
                                            choices=[(b'P', 'PIN'), (b'C', 'Cash')])),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'transaction',
                'verbose_name_plural': 'transactions',
            },
        ),
    ]
