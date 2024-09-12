# Generated by Django 2.0.13 on 2021-07-15 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("sponsors", "0028_auto_20210707_1426"),
    ]

    operations = [
        migrations.CreateModel(
            name="BenefitFeatureConfiguration",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ],
            options={
                "verbose_name": "Benefit Feature Configuration",
                "verbose_name_plural": "Benefit Feature Configurations",
            },
        ),
        migrations.CreateModel(
            name="LogoPlacementConfiguration",
            fields=[
                (
                    "benefitfeatureconfiguration_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="sponsors.BenefitFeatureConfiguration",
                    ),
                ),
                (
                    "publisher",
                    models.CharField(
                        choices=[("psf", "Foundation"), ("pycon", "Pycon"), ("pypi", "Pypi"), ("core", "Core Dev")],
                        help_text="On which site should the logo be displayed?",
                        max_length=30,
                        verbose_name="Publisher",
                    ),
                ),
                (
                    "logo_place",
                    models.CharField(
                        choices=[
                            ("sidebar", "Sidebar"),
                            ("sponsors", "Sponsors Page"),
                            ("jobs", "Jobs"),
                            ("blogpost", "Blog"),
                            ("footer", "Footer"),
                            ("docs", "Docs"),
                            ("download", "Download Page"),
                            ("devguide", "Dev Guide"),
                        ],
                        help_text="Where the logo should be placed?",
                        max_length=30,
                        verbose_name="Logo Placement",
                    ),
                ),
            ],
            options={
                "verbose_name": "Logo Placement Configuration",
                "verbose_name_plural": "Logo Placement Configurations",
            },
            bases=("sponsors.benefitfeatureconfiguration",),
        ),
        migrations.AddField(
            model_name="benefitfeatureconfiguration",
            name="benefit",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="sponsors.SponsorshipBenefit"),
        ),
        migrations.AddField(
            model_name="benefitfeatureconfiguration",
            name="polymorphic_ctype",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="polymorphic_sponsors.benefitfeatureconfiguration_set+",
                to="contenttypes.ContentType",
            ),
        ),
    ]
