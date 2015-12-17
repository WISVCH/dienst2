# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ldb', '0008_person_mail_educational'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='name_prefix',
            field=models.CharField(max_length=100, verbose_name='name prefix', blank=True),
        ),
    ]
