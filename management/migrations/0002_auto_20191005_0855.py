# Generated by Django 2.2.5 on 2019-10-05 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmanagement',
            name='flag',
            field=models.BooleanField(default=False),
        ),
    ]