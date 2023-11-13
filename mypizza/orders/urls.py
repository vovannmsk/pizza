from django.urls import path
from . import views
from .views import OrderCreate, OrderItemCreate, MyOrdersList, OrderItems

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('myorders/', views.my_orders.as_view(), name='my_orders'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),

    # далее идут контрольные точки, сформированные с помощью методов на DRF
    path('api/v1/generic/create_order/', OrderCreate.as_view(), name='create_order'),
    path('api/v1/generic/create_order_item/', OrderItemCreate.as_view(), name='create_order_items'),
    # path('api/v1/generic/create_order_plus_item/', OrderCreatePlusItem.as_view(), name='create_order'),
    path('api/v1/generic/my_orders/', MyOrdersList.as_view(), name='my_orders_api'),
    path('api/v1/generic/order_items/<int:order_id>', OrderItems.as_view(), name='orders_items'),   # продукты в заказе
]
