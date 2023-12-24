# Generated by Django 2.2.24 on 2023-12-24 18:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0098_auto_20231219_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='print_logo',
            field=models.FileField(blank=True, help_text='For printed materials, signage, and projection. SVG or EPS', null=True, upload_to='sponsor_print_logos', validators=[django.core.validators.FileExtensionValidator(['eps', 'epsfepsi', 'svg'])], verbose_name='Print logo'),
        ),
    ]
