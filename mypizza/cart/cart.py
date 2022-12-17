from django.conf import settings
from pizza_shop.models import Pizza
from decimal import *

class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:     # если товара еще нет в корзине
            self.cart[product_id] = {'quantity': 0, 'price': str(product.currentPrice)}  # добавляем строчку с товаром
                                                                                        # и его ценой в корзину
        if update_quantity:                                     # если нажимали кнопку "обновить"
            self.cart[product_id]['quantity'] = quantity        # то обновленное количество товара вносимв корзину
        else:                                                   # а если нажимали кнопку "Добавит в корзину"
            self.cart[product_id]['quantity'] += quantity       # прибавляем к уже существующему количеству новое кол-во
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart
        :param product:
        :return:
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart

        # products = Product.objects.filter(id__in=product_ids)
        products = Pizza.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        """
        remove cart from session
        :return:
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True