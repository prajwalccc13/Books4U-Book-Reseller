# Generated by Django 3.0 on 2019-12-11 04:47

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_image',
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=core.models.get_image_filename, verbose_name='Image')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.Product')),
            ],
        ),
    ]