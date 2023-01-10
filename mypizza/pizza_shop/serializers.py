from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Pizza, Feedbacks, TypeOfProduct


class PizzaSerializer(ModelSerializer):
    type_product = serializers.SlugRelatedField(slug_field='nameOfType', read_only=True)
    adress = serializers.URLField(source='get_absolute_url')

    class Meta:
        model = Pizza
        fields = ['id', 'pk', 'name', 'shortName', 'ingredients', 'currentPrice', 'photo', 'type_product', 'adress']


class FeedbackCreateSerializer(ModelSerializer):
    """Создание отзыва"""

    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # можно сделать скрытое поле, по умолчанию присваивать ему текущего юзера

    class Meta:
        model = Feedbacks
        fields = '__all__'


class FeedbackViewSerializer(ModelSerializer):
    """Вывод отзывов"""
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Feedbacks
        fields = ("buyer", "comment", "user")


class ProductDetailSerializer(ModelSerializer):
    """Вывод сведений по одному товару (вместе с отзывами по нему)"""
    type_product = serializers.SlugRelatedField(slug_field='nameOfType', read_only=True)
    feedbacks = FeedbackViewSerializer(many=True)

    class Meta:
        model = Pizza
        fields = '__all__'


class CategoriesSerializer(ModelSerializer):
    """Вывод списка категорий"""

    class Meta:
        model = TypeOfProduct
        fields = ['id', 'nameOfType', 'slug']
