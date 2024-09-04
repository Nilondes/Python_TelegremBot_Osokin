# Generated by Django 5.1 on 2024-08-30 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calender', '0006_alter_appointment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='duration',
            field=models.DurationField(default=0),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('confirmed', 'confirmed'), ('awaiting', 'awaiting'), ('declined', 'declined')], max_length=40),
        ),
    ]
