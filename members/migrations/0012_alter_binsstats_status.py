# Generated by Django 4.2.5 on 2023-12-09 10:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("members", "0011_binsstats_city_alter_binsstats_lat_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="binsstats",
            name="status",
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
