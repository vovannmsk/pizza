from django.contrib.auth.models import User
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.test import force_authenticate

from .models import Pizza
from .models import OrderItem
from .models import Order
from .views import OrderCreate

from .serializers import OrderSerializer, OrderItemCreateSerializer, OrderItemSerializer

class OrdersTests(APITestCase):

    # def setUp(self):
    #     self.example_order = Order.objects.create(first_name='Иван', last_name='Иванов', total_amount=1.00)
    #     Order.objects.create(first_name='Маша', last_name='Петрова', total_amount=2.00)

    def test_create_order(self):
        """  тестируем создание заказа (без списка товаров) """

        url = reverse('create_order')
        data = {'first_name': 'Иван'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().first_name, 'Иван')

    def test_orders_list(self):
        """Тест вывода списка всех заказов (без товаров)"""

        response = self.client.get(reverse('my_orders_api'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # print(response.status_code)
        # print(response.json().get("results"))
        # print(response.data)
        # self.assertEqual(len(response.json(["results"])), 2)

