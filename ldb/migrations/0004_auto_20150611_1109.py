# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ldb', '0003_uniqueness'),
    ]

    operations = [
        migrations.AlterField(
            model_name='committeemembership',
            name='person',
            field=models.ForeignKey(related_name='committee_memberships', to='ldb.Person'),
        ),
    ]
