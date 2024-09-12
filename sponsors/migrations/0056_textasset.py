# Generated by Django 2.2.24 on 2021-10-26 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("sponsors", "0055_auto_20211026_1512"),
    ]

    operations = [
        migrations.CreateModel(
            name="TextAsset",
            fields=[
                (
                    "genericasset_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="sponsors.GenericAsset",
                    ),
                ),
                ("text", models.TextField(default="")),
            ],
            options={
                "verbose_name": "Image Asset",
                "verbose_name_plural": "Image Assets",
            },
            bases=("sponsors.genericasset",),
        ),
    ]
