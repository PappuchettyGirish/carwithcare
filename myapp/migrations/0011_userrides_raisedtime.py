# Generated by Django 2.1 on 2019-09-18 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_auto_20190918_0529'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrides',
            name='raisedtime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
