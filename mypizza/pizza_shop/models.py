from django.db import models
from django.urls import reverse_lazy
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from django.contrib.auth.models import User

class Pizza(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Наименование продукта')
    shortName = models.CharField(max_length=20, verbose_name='Краткое наименование продукта')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='URL')
    ingredients = models.TextField(verbose_name='Список ингредиентов', blank=True)  #необязательно для заполнения
    currentPrice = models.DecimalField (max_digits=10, decimal_places=2, verbose_name='Текущая цена')
    photo = models.ImageField(upload_to='photos/', verbose_name='Фото', blank=True)  #необязательно для заполнения
    is_ready = models.BooleanField(default=True, verbose_name='Готовность для продажи')
    type_product = models.ForeignKey('TypeOfProduct', on_delete=models.PROTECT, verbose_name='Тип продукта', null=True, default=1)
    #price = models.DecimalField (max_digits=10, decimal_places=2, verbose_name='Цена', default=1000)


    # здесь мы строим функцию для админки, чтобы при нажатии на товар выскакивал сайт
    # со страничкой данного товара.
    # в скобочках функции reverse_lazy мы строим маршрут из urls.py
    def get_absolute_url(self):
       # return reverse_lazy('show_product', kwargs={"product_id": self.pk})  #вывод товара без использования REST
       return reverse_lazy('product_detail2', kwargs={"pk": self.pk})    #вывод товара через GenericAPIView

    def __str__(self):
        return self.name

    # автоматическкое создание слага
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Pizza, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты для заказа'
        ordering = ['name']

# список типов, категорий товаров (продуктов)
class TypeOfProduct(models.Model):
    nameOfType = models.CharField(max_length=50, db_index=True, verbose_name='Тип продукта')
    slug = models.SlugField(max_length=200, unique=True, db_index=True)

    # здесь мы строим функцию для админки, чтобы при нажатии на категорию продуктов выскакивал сайт
    # с уже выбранной данной категорией товара.
    # в скобочках функции reverse_lazy мы строим маршрут из urls.py
    def get_absolute_url(self):
        return reverse_lazy('type', kwargs={"type_id": self.pk})

    def __str__(self):
        return self.nameOfType

    # автоматическкое создание слага
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nameOfType)
        super(TypeOfProduct, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тип еды'
        verbose_name_plural = 'Типы еды'
        ordering = ['nameOfType']

# список покупателей. не используется.
class Buyers(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='Имя покупателя')
    phoneNumber = PhoneNumberField(unique=True, null=True, blank=True, verbose_name='Телефон покупателя')
    address = models.CharField(max_length=100, db_index=False, null=True, blank=True, verbose_name='Адрес для доставки')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        ordering = ['name']


class Feedbacks(models.Model):
    """Отзывы"""
    buyer = models.CharField(max_length=100, db_index=True, null=True, verbose_name='Имя')       #default="Анонимный покупатель"
#    buyersname = models.ForeignKey('Buyers', on_delete=models.PROTECT, verbose_name='Имя покупателя', null=True, default=1)
    product = models.ForeignKey('Pizza', on_delete=models.PROTECT, verbose_name='Наменование продукта', null=True,
                                related_name="feedbacks")
    comment = models.CharField(max_length=250, db_index=False, verbose_name='Отзыв')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь', null=True,
                                related_name='users')

    def get_absolute_url(self):
        return reverse_lazy('show_feedback', kwargs={"feedback_id": self.pk})
    #        return reverse_lazy('show_feedback', args=[str(self.pk)])  # альтернативный вариант через args

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Отзыв (комментарий)'
        verbose_name_plural = 'Отзывы (комментарии)'
        ordering = ['product']


# список заказов
class Order(models.Model):
    orderNumber = models.IntegerField(verbose_name='Номер заказа', null=True, default=1)
    product = models.ForeignKey('Pizza', on_delete=models.PROTECT, verbose_name='Наменование продукта', null=True, default=1)
    quantity = models.IntegerField(verbose_name='Количество (шт.)')
    buyersname = models.ForeignKey('Buyers', on_delete=models.PROTECT, verbose_name='Имя покупателя', null=True, default=1)

    def __str__(self):
        return self.orderNumber

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['orderNumber']