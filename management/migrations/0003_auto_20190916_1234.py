# Generated by Django 2.1.1 on 2019-09-16 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20190916_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttask',
            name='big_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.ProjectManagement'),
        ),
    ]
