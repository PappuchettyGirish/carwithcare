# Generated by Django 2.1 on 2019-09-14 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20190914_0222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrides',
            name='distance',
            field=models.FloatField(),
        ),
    ]
