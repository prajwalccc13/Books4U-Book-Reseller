# Generated by Django 3.0 on 2019-12-21 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20191221_1856'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='zip',
            new_name='google_maps_coordinates',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='zip_code',
            new_name='google_maps_coordinates',
        ),
    ]