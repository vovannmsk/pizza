from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()
router.register('api/list', ListAllProducts)

urlpatterns = [
    path('', pizza_main, name='home'),
    path('list/', List_Of_Product.as_view(), name='list'),
    path('list/<int:type_id>/', List_Product_Category.as_view(), name='type'),
    path('product/<int:product_id>/', ShowProduct.as_view(), name='show_product'),
    path('add_feedback/', AddFeedback.as_view(), name='add_feedback'),
    path('feedback/<int:feedback_id>/', ShowFeedback.as_view(), name='show_feedback'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

    path('list_app/', list_app, name='list_app'),
]

urlpatterns += router.urls
