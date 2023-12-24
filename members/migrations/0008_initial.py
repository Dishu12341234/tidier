# Generated by Django 4.2.5 on 2023-12-07 06:48

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("members", "0007_delete_appuser"),
    ]

    operations = [
        migrations.CreateModel(
            name="BinsStats",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("BinID", models.CharField(max_length=6, unique=True)),
                ("status", models.CharField(blank=True, max_length=4)),
                ("refreshStats", models.CharField(blank=True, max_length=4)),
                ("lastRefresh", models.DateField(blank=True)),
                ("fillUp", models.IntegerField(blank=True, max_length=100)),
                ("Lat", models.IntegerField(blank=True, max_length=100)),
                ("Lon", models.IntegerField(blank=True, max_length=100)),
                ("Area", models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]
