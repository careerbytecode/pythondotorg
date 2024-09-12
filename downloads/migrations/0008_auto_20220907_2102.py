# Generated by Django 2.2.24 on 2022-09-07 21:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("downloads", "0007_auto_20220809_1655"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="releasefile",
            constraint=models.UniqueConstraint(
                condition=models.Q(download_button=True),
                fields=("os", "release"),
                name="only_one_download_per_os_per_release",
            ),
        ),
    ]
