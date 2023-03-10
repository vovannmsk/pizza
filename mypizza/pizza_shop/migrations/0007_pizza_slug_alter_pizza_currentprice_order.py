# Generated by Django 4.1.2 on 2022-10-31 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_shop', '0006_buyers_address_buyers_phonenumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='currentPrice',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Текущая цена'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderNumber', models.IntegerField(default=1, null=True, verbose_name='Номер заказа')),
                ('quantity', models.IntegerField(verbose_name='Количество (шт.)')),
                ('buyersname', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='pizza_shop.buyers', verbose_name='Имя покупателя')),
                ('product', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='pizza_shop.pizza', verbose_name='Наменование продукта')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['orderNumber'],
            },
        ),
    ]
