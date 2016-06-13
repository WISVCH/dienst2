# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20160319_2323'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('date',), 'verbose_name': 'item', 'verbose_name_plural': 'items'},
        ),
    ]
