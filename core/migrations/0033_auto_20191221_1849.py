# Generated by Django 3.0 on 2019-12-21 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20191221_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pickup_address',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='product',
            name='zip',
            field=models.CharField(max_length=100),
        ),
    ]