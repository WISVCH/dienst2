# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20160319_2101'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'contact', 'verbose_name_plural': 'contacts'},
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(related_name='items', verbose_name='category', to='post.Category'),
        ),
        migrations.AlterField(
            model_name='item',
            name='recipient',
            field=models.ForeignKey(related_name='received_items', verbose_name='recipient', to='post.Contact'),
        ),
        migrations.AlterField(
            model_name='item',
            name='sender',
            field=models.ForeignKey(related_name='sent_items', verbose_name='sender', to='post.Contact'),
        ),
    ]
