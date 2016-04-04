# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20160319_0936'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='receiver',
            new_name='recipient',
        ),
        migrations.RenameModel(
            old_name='Source',
            new_name='Contact',
        ),
    ]
