from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
# from rest_framework_simplejwt.tokens import Token

from .models import TypeOfProduct, Pizza, Feedbacks
from .serializers import ProductDetailSerializer, PizzaSerializer


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

        # пользователь1
        user_test1 = User.objects.create_user(username='test2233', password="pass334sa")
        user_test1.save()
        self.user_test1_token = Token.objects.create(user=user_test1)
        # пользователь2
        user_test2 = User.objects.create_user(username='test2332', password="pass334dd")
        user_test2.save()
        self.user_test2_token = Token.objects.create(user=user_test2)

        Feedbacks.objects.create(buyer='Иван',
                                 product=self.first_product,
                                 comment="Супер!!!",
                                 user=user_test1
                                )
        Feedbacks.objects.create(
                                 buyer='Маша',
                                 product=self.first_product,
                                 comment="Отлично!!!",
                                 user=user_test1
                                )
        Feedbacks.objects.create(
                                 buyer='Оля',
                                 product=self.second_product,
                                 comment="Просто отлично!!!",
                                 user=user_test2
                                )


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
        self.assertTrue({'id': 1,
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

    def test_products_from_category(self):
        """ Тестирование выдачи списка товаров одной выбранной категории """
        url = reverse('products_from_category2', kwargs={"type_product": self.first_category.id})
        response = self.client.get(url,  format='json')
        self.assertEqual(len(response.data), 1)
        self.assertTrue({'id': 1,
                         'pk': 1,
                         'name': 'Пицца Неаполитанская',
                         'shortName': 'Неаполитанская',
                         'ingredients': '',
                         'currentPrice': '1000.00',
                         'photo': None,
                         'type_product': 'Пицца',
                         'adress': '/product/1/'
                         } in response.json())
        serializer_data = PizzaSerializer(self.first_product).data
        # print(serializer_data)
        # print(response.json())
        self.assertTrue(serializer_data in response.json())

    def test_create_feedback(self):
        """ Тестирование создания отзыва на выбранный товар """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)

        url = reverse('create_feedback2')  # , kwargs={"product": self.first_product.id})
        data = {
                'buyer': 'Иван',
                'product': self.first_product.id,
                'comment': "Супер!!!"
               }
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_feedback(self):
        """ Тестирование выдачи отзывов на выбранный товар """

        url = reverse('list_feedbacks2', kwargs={"product": self.first_product.id})
        response = self.client.get(url, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


        url = reverse('list_feedbacks2', kwargs={"product": self.second_product.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_feedbaks_for_user(self):
        """ Тестирование выдачи списка отзывов одного выбранного пользователя """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        url = reverse('list_user_feedbacks')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # проверяем кол-во отзывов у первого пользователя
        # print(response.json())

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test2_token.key)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # проверяем кол-во отзывов у второго пользователя

