from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Pizza, Order, OrderItem


class OrderSerializer(ModelSerializer):
    # type_product = serializers.SlugRelatedField(slug_field='nameOfType', read_only=True)
    # adress = serializers.URLField(source='get_absolute_url')

    class Meta:
        model = Order
        fields = ['id', 'pk', 'first_name', 'last_name', 'email', 'address', 'username', 'created', 'paid', 'delivered',
                  'total_amount', 'phone']


# class OrderItemSerializer(ModelSerializer):
#     order = OrderSerializer()
#
#     class Meta:
#         model = OrderItem
#         fields = ['id', 'pk', 'product', 'price', 'quantity', 'order']

class PizzaSerializer(ModelSerializer):
    type_product = serializers.SlugRelatedField(slug_field='nameOfType', read_only=True)
    adress = serializers.URLField(source='get_absolute_url')

    class Meta:
        model = Pizza
        fields = ['id', 'pk', 'name', 'shortName', 'ingredients', 'currentPrice', 'photo', 'type_product', 'adress']
        #fields = ['id', 'pk', 'name', 'shortName', 'currentPrice', 'photo', 'adress']
        # fields = '__all__'

class OrderItemSerializer(ModelSerializer):
    product = PizzaSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'pk', 'order', 'product', 'price', 'quantity']

class OrderItemCreateSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'pk', 'order', 'product', 'price', 'quantity']

