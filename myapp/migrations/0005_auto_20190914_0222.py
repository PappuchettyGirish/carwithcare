# Generated by Django 2.1 on 2019-09-14 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_userrides'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrides',
            name='distance',
            field=models.DecimalField(decimal_places=16, max_digits=22),
        ),
        migrations.AlterField(
            model_name='userrides',
            name='fromlat',
            field=models.DecimalField(decimal_places=16, max_digits=22),
        ),
        migrations.AlterField(
            model_name='userrides',
            name='fromlong',
            field=models.DecimalField(decimal_places=16, max_digits=22),
        ),
        migrations.AlterField(
            model_name='userrides',
            name='tolat',
            field=models.DecimalField(decimal_places=16, max_digits=22),
        ),
        migrations.AlterField(
            model_name='userrides',
            name='tolong',
            field=models.DecimalField(decimal_places=16, max_digits=22),
        ),
    ]