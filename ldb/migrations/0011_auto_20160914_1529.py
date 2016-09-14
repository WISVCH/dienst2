# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ldb', '0010_auto_20160612_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumnus',
            name='contact_method',
            field=models.CharField(choices=[('m', 'Mail'), ('e', 'Email')], max_length=1, default='e', verbose_name='contact method'),
        ),
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, verbose_name='gender'),
        ),
    ]
