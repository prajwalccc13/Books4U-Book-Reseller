# Generated by Django 3.0 on 2019-12-11 04:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
                ('status', models.BooleanField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.CharField(choices=[('New', 'New'), ('Old', 'New')], default='New', max_length=4)),
                ('name', models.CharField(max_length=100)),
                ('published_date', models.DateTimeField(auto_now=True)),
                ('product_image', models.ImageField(upload_to='product')),
                ('description', models.CharField(max_length=2000)),
                ('author', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('total_quantity', models.IntegerField(default=1)),
                ('remaining_quantity', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]