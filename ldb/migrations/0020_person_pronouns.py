# Generated by Django 2.2.28 on 2022-12-03 11:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ldb", "0019_auto_20221202_1710"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="pronouns",
            field=models.CharField(blank=True, max_length=100, verbose_name="pronouns"),
        ),
    ]
