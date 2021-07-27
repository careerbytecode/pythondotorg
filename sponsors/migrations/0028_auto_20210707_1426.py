# Generated by Django 2.0.13 on 2021-07-07 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0027_sponsorbenefit_program_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsorshipbenefit',
            name='program',
            field=models.ForeignKey(help_text='Which sponsorship program the benefit is associated with.', on_delete=django.db.models.deletion.CASCADE, to='sponsors.SponsorshipProgram', verbose_name='Sponsorship Program'),
        ),
    ]
