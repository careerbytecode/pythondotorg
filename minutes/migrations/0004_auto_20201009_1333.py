# Generated by Django 2.0.13 on 2020-10-09 13:33

from django.db import migrations, models
import django.db.models.deletion
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('minutes', '0003_auto_20201009_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgendaItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('title', models.CharField(max_length=500)),
                ('content', markupfield.fields.MarkupField(rendered_field=True)),
                ('content_markup_type', models.CharField(choices=[('', '--'), ('html', 'HTML'), ('plain', 'Plain'), ('markdown', 'Markdown'), ('restructuredtext', 'Restructured Text')], default='restructuredtext', max_length=30)),
                ('_content_rendered', models.TextField(editable=False)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('date', models.DateField(db_index=True)),
                ('minutes', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meeting', to='minutes.Minutes')),
                ('parties', models.ManyToManyField(to='minutes.ConcernedParty')),
            ],
            options={
                'verbose_name': 'meeting',
                'verbose_name_plural': 'meetings',
            },
        ),
        migrations.AddField(
            model_name='agendaitem',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minutes.Meeting'),
        ),
        migrations.AddField(
            model_name='agendaitem',
            name='owners',
            field=models.ManyToManyField(to='minutes.ConcernedParty'),
        ),
    ]
