# Generated by Django 3.0 on 2019-12-11 12:17

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20191211_0741'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='image',
            new_name='display_image',
        ),
        migrations.AddField(
            model_name='images',
            name='dec_image1',
            field=models.ImageField(blank=True, null=True, upload_to=core.models.get_image_filename, verbose_name='Image1'),
        ),
        migrations.AddField(
            model_name='images',
            name='dec_image2',
            field=models.ImageField(blank=True, null=True, upload_to=core.models.get_image_filename, verbose_name='Image2'),
        ),
        migrations.AddField(
            model_name='images',
            name='dec_image3',
            field=models.ImageField(blank=True, null=True, upload_to=core.models.get_image_filename, verbose_name='Image3'),
        ),
        migrations.AddField(
            model_name='images',
            name='dec_image4',
            field=models.ImageField(blank=True, null=True, upload_to=core.models.get_image_filename, verbose_name='Image4'),
        ),
        migrations.AddField(
            model_name='images',
            name='dec_image5',
            field=models.ImageField(blank=True, null=True, upload_to=core.models.get_image_filename, verbose_name='Image5'),
        ),
    ]
