# Generated by Django 2.1.1 on 2019-09-21 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_auto_20190921_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='middletask',
            name='middle_task_flag',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projectmanagement',
            name='project_flag',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projecttask',
            name='big_task_flag',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='smalltask',
            name='small_task_flag',
            field=models.IntegerField(default=0),
        ),
    ]
