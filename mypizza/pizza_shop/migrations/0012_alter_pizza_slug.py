# Generated by Django 4.1.2 on 2022-11-17 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_shop', '0011_alter_typeofproduct_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='URL'),
        ),
    ]
