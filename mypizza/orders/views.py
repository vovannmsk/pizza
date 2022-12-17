from django.views.generic import ListView

from cart.cart import Cart
from django.shortcuts import render
from .tasks import order_created

from .forms import OrderCreateForm
from .models import OrderItem
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order

# from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
# import weasyprint


# from jinja2 import Environment, FileSystemLoader
import pdfkit


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})

#    env = Environment(loader=FileSystemLoader('.'))
#    template = env.get_template('orders/order/pdf.html')

#    pdf_template = template.render({'order': order})

#    pdfkit.from_string(pdf_template, 'order_{}.pdf'.format(order.id))
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_string(html, 'order_{}.pdf'.format(order.id), configuration=config)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "filename=\'order_{}.pdf'".format(order.id)
    #    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[
    #        weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return render(request, 'orders/order/pdf.html', {'order': order})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # пересылка Email получателю асинхронно
            # order_created.delay(order.id)
            # пересылка Email получателю обычным способом
            order_created(order.id)
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

# получение списка заказов конкретного покупателя (с помощью класса)
class my_orders(ListView):
    # paginate_by = 3
    model = Order
    template_name = 'orders/my_orders.html'
    context_object_name = 'users_orders'    # как данные будут называться в html
 #   allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)    # получаем уже сформированный контекст
        context['user1'] = self.request.user
        # context['id_username'] = self.request.user.id_username

        # context['cart_product_form'] = CartAddProductForm()  # передаём корзину в html
        context['title'] = 'Ваши заказы'
        # context['category'] = self.kwargs['type_id']
        return context

    def get_queryset(self):
        username_ = self.request.user
        return Order.objects.filter(username=username_)


#        return Pizza.objects.filter(type_product__slug=self.kwargs['type_slug'], is_ready=True)
#       такой запрос был бы, если использовать отбор по слагу.
#       В urls.py должен быть <int:type_slug> вместо <int:type_id>