from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
# from rest_framework_simplejwt.tokens import Token

from .models import TypeOfProduct, Pizza
from .serializers import ProductDetailSerializer


class CategoryTests(APITestCase):
    def setUp(self):
        self.first_category = TypeOfProduct.objects.create(nameOfType="Пицца", slug="pizza")
        self.second_category = TypeOfProduct.objects.create(nameOfType="Напитки", slug="drinks")
        TypeOfProduct.objects.create(nameOfType="Суши", slug="sushi")

        self.first_product = Pizza.objects.create(
            name="Пицца Неаполитанская",
            shortName="Неаполитанская",
            slug="pizza_neapol",
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
            type_product = self.second_category
        )

        user_test1 = User.objects.create_user(username='test2233', password="pass334sa")
        user_test1.save()
        self.user_test1_token = Token.objects.create(user=user_test1)


    def test_list_category(self):
        """ Тестирование выдачи полного списка категорий """
        url = reverse('categories2')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        # print(response.data)
        # print(response.json())
        self.assertTrue({'id': 1,
                         'pk': 1,
                         'nameOfType': "Пицца",
                         'slug': "pizza"
                        } in response.json())

    def test_list_products(self):
        """ Тестирование выдачи списка продуктов (с аутентификацией и без неё)
         работает только, если в settings.py стоит параметр 'rest_framework.authentication.TokenAuthentication'
         не работает с 'rest_framework_simplejwt.authentication.JWTAuthentication' (JWT нужна для Vue)"""

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)

        url = reverse('list_products2')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # print(response.data)
        # print(response.json())
        self.assertTrue( {'id': 1,
                          'pk': 1,
                          'name': 'Пицца Неаполитанская',
                          'shortName': 'Неаполитанская',
                          'ingredients': '',
                          'currentPrice': '1000.00',
                          'photo': None,
                          'type_product': 'Пицца',
                          'adress': '/product/1/'
                         } in response.json())

    def test_product(self):
        """ Тестирование выдачи подробного описания одного выбранного товара """
        url = reverse('product_detail2', kwargs={"pk": self.second_product.id})
        response = self.client.get(url,  format='json')
        serializer_data = ProductDetailSerializer(self.second_product).data
        # print(response.data)
        # print(serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)
