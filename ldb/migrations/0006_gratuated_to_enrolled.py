# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('ldb', '0005_index_upper'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='graduated',
            new_name='enrolled',
        ),
        migrations.AlterField(
            model_name='student',
            name='enrolled',
            field=models.BooleanField(default=True, verbose_name='enrolled'),
        ),
        migrations.RunSQL("UPDATE ldb_student SET enrolled = NOT enrolled;"),
    ]
