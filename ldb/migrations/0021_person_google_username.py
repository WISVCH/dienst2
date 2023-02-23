# Generated by Django 2.2.28 on 2023-02-19 18:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ldb", "0020_person_pronouns"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="google_username",
            field=models.CharField(
                blank=True,
                max_length=64,
                null=True,
                unique=True,
                verbose_name="Google username",
            ),
        ),
    ]
