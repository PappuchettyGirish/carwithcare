# Generated by Django 2.1 on 2019-09-14 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_driverdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driversignup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailid', models.CharField(max_length=50)),
                ('otp', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='userrides',
            name='distance',
            field=models.DecimalField(decimal_places=16, max_digits=22),
        ),
    ]
