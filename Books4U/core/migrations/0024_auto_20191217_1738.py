# Generated by Django 3.0 on 2019-12-17 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20191217_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='remaining_quantity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='total_quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]