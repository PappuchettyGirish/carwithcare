# Generated by Django 2.1 on 2019-09-18 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20190914_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrides',
            name='endtime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='userrides',
            name='starttime',
            field=models.DateTimeField(null=True),
        ),
    ]
