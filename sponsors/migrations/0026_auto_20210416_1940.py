# Generated by Django 2.0.13 on 2021-04-16 19:40

from django.db import migrations, models
import markupfield.fields


class Migration(migrations.Migration):
    dependencies = [
        ("sponsors", "0025_auto_20210416_1939"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contract",
            name="_legal_clauses_rendered",
            field=models.TextField(default="", editable=False),
        ),
        migrations.AlterField(
            model_name="contract",
            name="legal_clauses",
            field=markupfield.fields.MarkupField(blank=True, default="", rendered_field=True),
        ),
    ]
