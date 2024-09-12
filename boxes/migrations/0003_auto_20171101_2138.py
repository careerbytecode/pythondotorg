# Generated by Django 1.11.5 on 2017-11-01 21:38

from django.db import migrations


def migrate_old_content(apps, schema_editor):
    Box = apps.get_model("boxes", "Box")
    Box.objects.filter(label="events-subscriptions").update(
        content='<h2 class="widget-title">Python Events Calendars</h2>\r\n\r\n<br/>\r\n\r\n'
        '<p>For Python events near you, please have a look at the <a href="http://lmorillas.github.io/python_events/">'
        "<b>Python events map</b></a>.</p>\r\n\r\n"
        '<p>The Python events calendars are maintained by the <a href="https://wiki.python.org/moin/PythonEventsCalendar#Python_Calendar_Team">events calendar team</a>.</p>\r\n\r\n'
        '<p>Please see the <a href="https://wiki.python.org/moin/PythonEventsCalendar">'
        'events calendar project page</a> for details on how to <a href="/events/submit/">submit events</a>,'
        '<a href="https://wiki.python.org/moin/PythonEventsCalendar#Available_Calendars">subscribe to the calendars</a>,'
        'get <a href="https://twitter.com/PythonEvents">Twitter feeds</a> or embed them.</p>\r\n\r\n<p>Thank you.</p>\r\n'
    )


class Migration(migrations.Migration):
    dependencies = [
        ("boxes", "0002_auto_20150416_1853"),
    ]

    operations = [
        migrations.RunPython(migrate_old_content),
    ]
