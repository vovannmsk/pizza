# Generated by Django 4.1.2 on 2022-11-17 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_shop', '0009_feedbacks_buyers_alter_pizza_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='slug',
            field=models.SlugField(max_length=200, verbose_name='URL'),
        ),
    ]
