from django.db import models
from pizza_shop.models import Pizza


# Create your models here.


class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='e-mail')
    address = models.CharField(max_length=250, verbose_name='Адрес доставки')
    postal_code = models.CharField(max_length=20, verbose_name='Почтовый индекс', blank=True)
    city = models.CharField(max_length=100, verbose_name='Город', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Заказ создан')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='Заказ дополнен')
    paid = models.BooleanField(default=False, verbose_name='Оплачено')
    username = models.CharField(max_length=50, default='admin', verbose_name='Логин')
    # username соответствует имени, под которым пользователь залогинился
    # необходимо для вывода списка заказов конкретного пользователя
    delivered = models.BooleanField(default=False, verbose_name='Доставлен')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая сумма заказа', null=True,
                                       default=0)
    phone = models.CharField(max_length=20, verbose_name='Телефон заказчика', null=True, default="")

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.PROTECT, verbose_name='Заказ №')
    product = models.ForeignKey(Pizza, related_name='order_items', on_delete=models.PROTECT, verbose_name='Продукт')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
