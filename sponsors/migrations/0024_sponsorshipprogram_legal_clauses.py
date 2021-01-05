# Generated by Django 2.0.13 on 2021-01-05 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sponsors", "0023_auto_20210105_1206"),
    ]

    operations = [
        migrations.AddField(
            model_name="sponsorshipprogram",
            name="legal_clauses",
            field=models.ManyToManyField(
                blank=True,
                help_text="Legal clauses to be displayed in the contract",
                related_name="programs",
                to="sponsors.LegalClause",
                verbose_name="Legal Clauses",
            ),
        ),
    ]
