# Generated by Django 2.1.1 on 2019-09-16 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_auto_20190916_1234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectmanagement',
            name='id',
        ),
        migrations.AlterField(
            model_name='projectmanagement',
            name='project_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
