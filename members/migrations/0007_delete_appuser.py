# Generated by Django 4.2.5 on 2023-12-07 06:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("members", "0006_alter_appuser_first_name"),
    ]

    operations = [
        migrations.DeleteModel(
            name="AppUser",
        ),
    ]
