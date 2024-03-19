# Generated by Django 4.2.11 on 2024-03-19 02:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('minutes', '0002_auto_20150416_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minutes',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='minutes',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_modified', to=settings.AUTH_USER_MODEL),
        ),
    ]
