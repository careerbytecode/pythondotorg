# Generated by Django 2.2.24 on 2021-11-08 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0059_auto_20211029_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='requiredimgasset',
            name='help_text',
            field=models.CharField(blank=True, default='', help_text='Any helper comment on how the input should be populated', max_length=256),
        ),
        migrations.AddField(
            model_name='requiredimgasset',
            name='label',
            field=models.CharField(default='label', help_text="What's the title used to display the input to the sponsor?", max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requiredimgassetconfiguration',
            name='help_text',
            field=models.CharField(blank=True, default='', help_text='Any helper comment on how the input should be populated', max_length=256),
        ),
        migrations.AddField(
            model_name='requiredimgassetconfiguration',
            name='label',
            field=models.CharField(default='label', help_text="What's the title used to display the input to the sponsor?", max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='requiredtextasset',
            name='label',
            field=models.CharField(help_text="What's the title used to display the input to the sponsor?", max_length=256),
        ),
        migrations.AlterField(
            model_name='requiredtextassetconfiguration',
            name='label',
            field=models.CharField(help_text="What's the title used to display the input to the sponsor?", max_length=256),
        ),
    ]
