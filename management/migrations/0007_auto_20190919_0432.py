# Generated by Django 2.1.1 on 2019-09-19 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_middletask'),
    ]

    operations = [
        migrations.RenameField(
            model_name='middletask',
            old_name='end_task',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='projecttask',
            old_name='end_task',
            new_name='end_date',
        ),
    ]
