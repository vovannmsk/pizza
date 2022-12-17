from django.http import HttpRequest
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_POST

from pizza_shop.models import Pizza
from .cart import Cart
from .forms import CartAddProductForm
#from pizza_shop.views import show_product


# Create your views here.
# метод применяется, при нажатии кнопки "Обновить" и кнопки "Добавить в корзину"
# переходим сюда по ссылке  cart/add/<int:product_id>/
@require_POST
def cart_add(request, product_id):
    host2 = request.META["HTTP_REFERER"]   #сохраняем страницу, с которой пришел запрос
    cart = Cart(request)
    product = get_object_or_404(Pizza, pk=product_id)   # продукт, по которому идёт изменение количества
    form = CartAddProductForm(request.POST)
    if form.is_valid():      # если данные в форме прошли проверку
        cd = form.cleaned_data  # очищенные данные из формы

        cart.add(product=product,           # в метод add класса Cart модуля cart.py  передаём продукт
                 quantity=cd['quantity'],   # количество товара (при нажатии кнопки "Добавить в корзину")
                 update_quantity=cd['update'])  # количество товара (при нажатии кнопки "Обновить")


    return redirect(host2)      # переходим на страницу, с которой пришел запрос

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Pizza, pk=product_id)  # продукт, который удаляем
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})
