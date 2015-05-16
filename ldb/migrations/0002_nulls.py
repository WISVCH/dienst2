# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from dienst2.extras import CharNullField


class Migration(migrations.Migration):
    dependencies = [
        ('ldb', '0001_initial'),
    ]

    # To make columns unique, we need to allow nulls. Split into two migrations because migrations are executed within
    # a single transaction, and we cannot alter structure after altering data within a single transaction.
    #
    # https://code.djangoproject.com/ticket/4136
    operations = [
        migrations.AlterField(
            model_name='person',
            name='facebook_id',
            field=CharNullField(max_length=64, null=True, verbose_name='Facebook ID', blank=True),
        ),

        migrations.AlterField(
            model_name='person',
            name='ldap_username',
            field=CharNullField(max_length=64, null=True, verbose_name='LDAP username', blank=True),
        ),

        migrations.AlterField(
            model_name='person',
            name='linkedin_id',
            field=CharNullField(max_length=64, null=True, verbose_name='LinkedIn ID', blank=True),
        ),

        migrations.AlterField(
            model_name='person',
            name='netid',
            field=CharNullField(max_length=64, null=True, verbose_name='NetID', blank=True),
        ),

        migrations.AlterField(
            model_name='student',
            name='student_number',
            field=CharNullField(max_length=7, null=True, verbose_name='student number', blank=True),
        ),
        migrations.RunSQL("UPDATE ldb_person SET ldap_username = NULL WHERE ldap_username = '';"),
        migrations.RunSQL("UPDATE ldb_person SET linkedin_id = NULL WHERE linkedin_id = '';"),
        migrations.RunSQL("UPDATE ldb_person SET netid = NULL WHERE netid = '';"),
        migrations.RunSQL("UPDATE ldb_person SET facebook_id = NULL WHERE facebook_id = '';"),
        migrations.RunSQL(
            "UPDATE ldb_student SET student_number = NULL WHERE student_number = '' OR student_number = '0';"),
    ]
