# Generated by Django 4.1.2 on 2022-11-17 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_shop', '0012_alter_pizza_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeofproduct',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
    ]
