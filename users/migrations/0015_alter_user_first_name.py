# Generated by Django 4.2.11 on 2024-09-05 17:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0014_auto_20210801_2332"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(blank=True, max_length=150, verbose_name="first name"),
        ),
    ]
