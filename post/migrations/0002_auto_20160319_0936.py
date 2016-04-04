# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(related_name='items', to='post.Category'),
        ),
        migrations.AlterField(
            model_name='item',
            name='receiver',
            field=models.ForeignKey(related_name='received_items', to='post.Source'),
        ),
        migrations.AlterField(
            model_name='item',
            name='sender',
            field=models.ForeignKey(related_name='sent_items', to='post.Source'),
        ),
    ]
