from django import template
from pizza_shop.models import TypeOfProduct

register = template.Library()


# @register.simple_tag(name='listTypeOfProduct')
# def type_product():
#     return TypeOfProduct.objects.all()


@register.inclusion_tag('pizza_shop/list_typeOfProducts.html')
def show_types_products():
    return {"typeOfProduct": TypeOfProduct.objects.all()}    # "typeOfProduct" - соответствует списку типов(категорий) товаров
                                                             # в шаблоне list_typeOfProducts.html

