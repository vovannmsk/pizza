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

    # view через def
    path('list_app/', list_app, name='list_app'),

    # через классы APIView
    path('api/v1/list/', PizzaList.as_view(), name='list_products'),
    path('api/v1/list/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('api/v1/cat/', ListOfCategories.as_view(), name='categories'),
    path('api/v1/cat/<int:pk>/', ProductsFromCategory.as_view(), name='products_from_category'),
    path('api/v1/feedback/', FeedbackCreate.as_view(), name='create_feedback'),
    path('api/v1/feedback/<int:pk>/', FeedbackView.as_view(), name='list_feedbacks'),

    # через классы GenericAPIView
    path('api/v1/generic/list/', PizzaList2.as_view(), name='list_products2'),
    path('api/v1/generic/list/<int:pk>/', ProductDetailView2.as_view(), name='product_detail2'),
    path('api/v1/generic/cat/', ListOfCategories2.as_view(), name='categories2'),
    path('api/v1/generic/cat/<int:type_product>/', ProductsFromCategory2.as_view(), name='products_from_category2'),
    path('api/v1/generic/feedback/', FeedbackCreate2.as_view(), name='create_feedback2'),
    path('api/v1/generic/feedback/<int:product>/', FeedbackView2.as_view(), name='list_feedbacks2'),

]

urlpatterns += router.urls
