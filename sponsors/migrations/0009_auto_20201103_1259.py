# Generated by Django 2.0.13 on 2020-11-03 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("sponsors", "0008_auto_20201028_1814"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sponsor",
            name="_content_rendered",
        ),
        migrations.RemoveField(
            model_name="sponsor",
            name="company",
        ),
        migrations.RemoveField(
            model_name="sponsor",
            name="content",
        ),
        migrations.RemoveField(
            model_name="sponsor",
            name="content_markup_type",
        ),
        migrations.RemoveField(
            model_name="sponsor",
            name="featured",
        ),
        migrations.RemoveField(
            model_name="sponsor",
            name="is_published",
        ),
        migrations.AlterField(
            model_name="sponsorcontact",
            name="sponsor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contacts",
                to="sponsors.Sponsor",
            ),
        ),
        migrations.AlterField(
            model_name="sponsorship",
            name="level_name",
            field=models.CharField(default="", max_length=64),
        ),
    ]
