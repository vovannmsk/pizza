from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from pizza_shop.models import TypeOfProduct
from .models import Pizza
from .models import OrderItem
from .models import Order


# from .serializers import OrderSerializer, OrderItemCreateSerializer, OrderItemSerializer


class OrdersTests(APITestCase):

    def setUp(self):
        # пользователь1
        user_test1 = User.objects.create_user(username='test2233', password="pass334sa")
        user_test1.save()
        self.user_test1_token = Token.objects.create(user=user_test1)
        # пользователь2
        user_test2 = User.objects.create_user(username='test2332', password="pass334dd")
        user_test2.save()
        self.user_test2_token = Token.objects.create(user=user_test2)

        self.first_order = Order.objects.create(
            first_name='Иван',
            last_name='Иванов',
            email='Ivanov123@yandex.ru',
            address='Тула',
            username=user_test1
        )
        self.second_order = Order.objects.create(
            first_name='Маша',
            last_name='Иванова',
            email='IvanovaM321@yandex.ru',
            address='Тула',
            username=user_test1
        )

        self.first_category = TypeOfProduct.objects.create(nameOfType="Пицца", slug="pizza")
        self.second_category = TypeOfProduct.objects.create(nameOfType="Напитки", slug="drinks")
        self.first_product = Pizza.objects.create(
            name="Пицца Неаполитанская",
            shortName="Неаполитанская",
            slug="pizza_naples",
            currentPrice=1000,
            is_ready=True,
            type_product=self.first_category
        )
        self.second_product = Pizza.objects.create(
            name="Лимонад Советский 1л",
            shortName="Лимонад 1л",
            slug="limonade",
            currentPrice=100,
            is_ready=True,
            type_product=self.second_category
        )

        OrderItem.objects.create(
            order=self.first_order,
            product=self.first_product,
            price=400,
            quantity=3
        )
        OrderItem.objects.create(
            order=self.first_order,
            product=self.second_product,
            price=500,
            quantity=2
        )

    def test_create_order(self):
        """  Тестируем создание шапки заказа (без списка товаров, т.е. без табличной части) """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)

        url = reverse('create_order')
        data = {'first_name': 'Александр',
                'last_name': 'Иванов',
                'email': 'Ivanov3456@yandex.ru',
                'address': 'Москва'
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 3)
        self.assertEqual(Order.objects.get(pk=3).first_name, 'Александр')

    def test_create_items_for_order(self):
        """ Тестирование создания табличной части заказа (товаров, количества, суммы и т.д.) """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        url = reverse('create_order_items')
        data = {'order': self.first_order.id,
                'product': self.second_product.id,
                'price': 500,
                'quantity': 2
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderItem.objects.count(), 3)
        # print(response.json())

    def test_orders_list(self):
        """Тест выдачи списка всех заказов текущего пользователя(без товаров)"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)

        url = reverse('my_orders_api')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # print(response.status_code)
        # print(response.json().get("results"))
        # print(response.data)
        self.assertEqual(len(response.data), 2)

    def test_products_in_order(self):
        """ Тестируем выдачу всех продуктов одного выбранного заказа """
        url = reverse('orders_items', kwargs={"order_id": self.first_order.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
