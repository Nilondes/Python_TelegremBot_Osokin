# Generated by Django 5.1 on 2024-08-29 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calender', '0004_rename_chat_id_event_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='duration',
            field=models.TimeField(default='00:00:00'),
        ),
    ]
