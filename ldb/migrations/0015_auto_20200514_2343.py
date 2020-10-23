# Generated by Django 2.2.12 on 2020-05-14 21:43

import dienst2.extras
from django.db import migrations
import ldb.validators


class Migration(migrations.Migration):

    dependencies = [("ldb", "0014_auto_20190426_1628")]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="ldap_username",
            field=dienst2.extras.CharNullField(
                blank=True,
                max_length=64,
                null=True,
                unique=True,
                validators=[ldb.validators.validate_ldap_username],
                verbose_name="LDAP username",
            ),
        )
    ]
