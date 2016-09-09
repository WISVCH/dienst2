# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('grouping', models.BooleanField(default=False, verbose_name='grouping')),
                ('counting', models.BooleanField(default=False, verbose_name='counting')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('description', models.CharField(max_length=128, verbose_name='description')),
                ('category', models.ForeignKey(to='post.Category')),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('location', models.CharField(max_length=1, verbose_name='location',
                                              choices=[('I', 'internal'), ('E', 'external')])),
            ],
            options={
                'verbose_name': 'source',
                'verbose_name_plural': 'sources',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='receiver',
            field=models.ForeignKey(related_name='receiver', to='post.Source'),
        ),
        migrations.AddField(
            model_name='item',
            name='sender',
            field=models.ForeignKey(related_name='sender', to='post.Source'),
        ),
    ]
