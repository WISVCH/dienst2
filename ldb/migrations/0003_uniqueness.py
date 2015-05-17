# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from dienst2.extras import CharNullField

class Migration(migrations.Migration):

    dependencies = [
        ('ldb', '0001_initial'),
        ('ldb', '0002_nulls'),
    ]

    # Set uniqueness
    operations = [
        migrations.AlterField(
            model_name='person',
            name='facebook_id',
            field=CharNullField(max_length=64, unique=True, null=True, verbose_name='Facebook ID', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='ldap_username',
            field=CharNullField(max_length=64, unique=True, null=True, verbose_name='LDAP username', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='linkedin_id',
            field=CharNullField(max_length=64, unique=True, null=True, verbose_name='LinkedIn ID', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='netid',
            field=CharNullField(max_length=64, unique=True, null=True, verbose_name='NetID', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_number',
            field=CharNullField(max_length=7, unique=True, null=True, verbose_name='student number', blank=True),
        ),
    ]
