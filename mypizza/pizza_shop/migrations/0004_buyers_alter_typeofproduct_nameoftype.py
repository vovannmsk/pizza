# Generated by Django 4.1.2 on 2022-10-30 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_shop', '0003_pizza_type_product_alter_pizza_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='Имя покупателя')),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='typeofproduct',
            name='nameOfType',
            field=models.CharField(db_index=True, max_length=50, verbose_name='Тип продукта'),
        ),
    ]