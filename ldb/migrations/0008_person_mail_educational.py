# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ldb', '0007_person_membership_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='mail_educational',
            field=models.BooleanField(default=True, verbose_name='educational mailing'),
        ),
    ]
