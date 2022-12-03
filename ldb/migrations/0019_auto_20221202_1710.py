# Generated by Django 2.2.28 on 2022-12-02 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ldb", "0018_auto_20200528_1344"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[
                    ("M", "Male"),
                    ("F", "Female"),
                    ("NB", "Non-binary"),
                    ("O", "Other"),
                ],
                max_length=2,
                verbose_name="gender",
            ),
        ),
    ]
