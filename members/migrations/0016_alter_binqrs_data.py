# Generated by Django 4.2.5 on 2023-12-09 16:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("members", "0015_binqrs_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="binqrs",
            name="data",
            field=models.CharField(default="noData", max_length=50),
        ),
    ]
