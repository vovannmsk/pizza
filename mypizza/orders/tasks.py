from celery import shared_task   # для асинхронных задач
from django.core.mail import send_mail
from django.conf import settings
from .models import Order
from django.shortcuts import get_object_or_404
# from mypizza.celery_task import app
# from django.template.loader import render_to_string


@shared_task
# @app.task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    # order = Order.objects.get(id=order_id)
    order = get_object_or_404(Order, id=order_id)
    subject = 'Заказ № {}'.format(order.id)   # тема письма
    message = 'Уважаемый (-ая) {},\n\n' \
              'Вы разместили заказ.\n'\
              'Ваш заказ №{}.\n' \
              'Сумма заказа - {} руб.'.format(order.first_name, order.id, order.get_total_cost())
    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email])

    # так можно послать текст письма из html
    # message = render_to_string('path/to/template.html', {'test_variable': 'xxx'})
    # send_mail('Тема', message, settings.EMAIL_HOST_USER, [order.email], html_message=message)

    return mail_sent
