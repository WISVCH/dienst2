# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ldb', '0006_gratuated_to_enrolled'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='_membership_status',
            field=models.IntegerField(default=0, db_column='membership_status'),
        ),
    ]
