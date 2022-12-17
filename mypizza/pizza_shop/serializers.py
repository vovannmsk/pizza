from django.urls import reverse_lazy
from rest_framework.serializers import ModelSerializer

from .models import Pizza


class PizzaSerializer(ModelSerializer):
    class Meta:
        model = Pizza
        fields = ['name', 'shortName', 'ingredients', 'currentPrice', 'photo', 'type_product']

