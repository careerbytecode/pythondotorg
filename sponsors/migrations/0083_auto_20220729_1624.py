# Generated by Django 2.2.24 on 2022-07-29 16:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sponsors", "0082_auto_20220729_1613"),
    ]

    operations = [
        migrations.AddField(
            model_name="sponsorshipbenefit",
            name="year",
            field=models.PositiveIntegerField(
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(limit_value=2022, message="The min year value is 2022."),
                    django.core.validators.MaxValueValidator(limit_value=2050, message="The max year value is 2050."),
                ],
            ),
        ),
        migrations.AddField(
            model_name="sponsorshippackage",
            name="year",
            field=models.PositiveIntegerField(
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(limit_value=2022, message="The min year value is 2022."),
                    django.core.validators.MaxValueValidator(limit_value=2050, message="The max year value is 2050."),
                ],
            ),
        ),
    ]
