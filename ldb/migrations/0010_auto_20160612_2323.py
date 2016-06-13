# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ldb', '0009_organization_blank_name_prefix'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='committee',
            options={'ordering': ['name'], 'verbose_name': 'committee', 'verbose_name_plural': 'committees'},
        ),
        migrations.AlterModelOptions(
            name='committeemembership',
            options={'ordering': ['board', 'committee__name'], 'verbose_name': 'committee membership', 'verbose_name_plural': 'committee memberships'},
        ),
    ]
