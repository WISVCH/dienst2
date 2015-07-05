# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('ldb', '0004_auto_20150611_1109'),
    ]

    operations = [
        migrations.RunSQL("CREATE INDEX ldb_person_ldap_username_upper ON ldb_person (UPPER(ldap_username));"),
        migrations.RunSQL("CREATE INDEX ldb_person_netid_upper ON ldb_person (UPPER(netid));"),
    ]
