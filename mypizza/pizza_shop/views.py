from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
# from django.core.mail.backends import console
from django.shortcuts import render, redirect
# from rest_framework.renderers import TemplateHTMLRenderer

# from django.urls import reverse_lazy
# from django.views.decorators.http import require_POST
# from .models import Pizza, TypeOfProduct, Feedbacks, Buyers
from cart.forms import CartAddProductForm

from django.views.generic import ListView, DetailView, CreateView
from .forms import *

from .serializers import PizzaSerializer, ProductDetailSerializer, FeedbackCreateSerializer, CategoriesSerializer, \
    FeedbackViewSerializer, FeedbacksUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView   # , ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, viewsets  # , renderers, generics
# from rest_framework.permissions import IsAuthenticated

# from django_filters.rest_framework import DjangoFilterBackend


# =====================================================================================================================
# вывод данных с помощью метода def
# =====================================================================================================================
def list_app(request):
    return render(request, 'pizza_shop/list_app.html')


# =====================================================================================================================
# вывод данных с помощью ViewSet и router
# =====================================================================================================================
class ListAllProducts(ModelViewSet):
    queryset = Pizza.objects.filter(is_ready=True)
    serializer_class = PizzaSerializer


# =====================================================================================================================
# вывод данных с помощью классов ViewSet
# =====================================================================================================================
class PizzaListVS(viewsets.ReadOnlyModelViewSet):
    """Вывод всех продуктов через ViewSet"""

    queryset = Pizza.objects.filter(is_ready=True)
    serializer_class = PizzaSerializer


class ProductDetailViewVS(viewsets.ReadOnlyModelViewSet):
    """Вывод сведений по одному товару (вместе с отзывами по нему)"""

    queryset = Pizza.objects.all()
    serializer_class = ProductDetailSerializer


class ProductsFromCategoryVS(viewsets.ReadOnlyModelViewSet):
    """Вывод всех продуктов одной категории через ViewSet"""
    serializer_class = PizzaSerializer

    def get_queryset(self):
        """'этот метод вместо строки queryset = ... """
        return Pizza.objects.filter(is_ready=True, type_product=self.kwargs["type_product"]).order_by('id')


class ListOfCategoriesVS(viewsets.ReadOnlyModelViewSet):
    """Вывод всех категорий продуктов через ViewSet"""

    queryset = TypeOfProduct.objects.all().order_by('id')
    serializer_class = CategoriesSerializer


class FeedbackCreateVS(viewsets.ModelViewSet):
    """Добавление отзыва на товар с помощью класса ModelViwSet"""
    serializer_class = FeedbackCreateSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        """Переопределил метод, чтобы полю user присвоить значение актуального юзера"""
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class FeedbackViewVS(viewsets.ReadOnlyModelViewSet):
    """Вывод отзывов на один товар"""
    serializer_class = FeedbackViewSerializer

    def get_queryset(self):
        """'этот метод вместо строки queryset = ... """
        return Feedbacks.objects.filter(product=self.kwargs["product"]).order_by('id')


# =====================================================================================================================
# вывод данных с помощью классов APIView
# =====================================================================================================================
class PizzaList(APIView):
    """Вывод всех продуктов через serializer"""

    def get(self):
        products = Pizza.objects.filter(is_ready=True)
        serializer = PizzaSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    """Вывод сведений по одному товару (вместе с отзывами по нему)"""

    def get(self, pk):
        product = Pizza.objects.get(id=pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


class ProductsFromCategory(APIView):
    """Вывод всех продуктов одной категории через serializer"""

    def get(self, pk):
        products = Pizza.objects.filter(is_ready=True, type_product=pk).order_by('id')
        serializer = PizzaSerializer(products, many=True)
        return Response(serializer.data)


class ListOfCategories(APIView):
    """Вывод всех категорий продуктов через serializer"""

    def get(self):
        categories = TypeOfProduct.objects.all().order_by('id')
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)


class FeedbackCreate(APIView):
    """Создание отзыва из формы"""

    def post(self, request):
        feedback = FeedbackCreateSerializer(data=request.data)
        feedback.is_valid(raise_exception=True)
        feedback.save(user=self.request.user)
        # сохраняем проверенные данные в базе, при этом полю user присваиваем значение текущего зарегистрированного
        # пользователя (self.request.user)
        return Response({'post': feedback.data})
        # другой вариант записи
        # if feedback.is_valid():
        #     feedback.save()
        # return Response(status=201)


class FeedbackView(APIView):
    """Вывод отзывов на один товар"""

    def get(self, pk):
        feedback = Feedbacks.objects.filter(product=pk).order_by('id')
        serializer = FeedbackViewSerializer(feedback, many=True)
        return Response(serializer.data)


# =====================================================================================================================
# вывод данных с помощью классов GenericAPIView (DRF)
# =====================================================================================================================
class PizzaList2(ListAPIView):
    """Вывод списка всех продуктов через serializer"""
    queryset = Pizza.objects.filter(is_ready=True).order_by('id')
    serializer_class = PizzaSerializer
    permission_classes = [permissions.IsAuthenticated]

    # pagination_class = LargeResultsSetPagination
    # так можно указать класс для разбивки на страницы
    # ИНДИВИДУАЛЬНО для данного класса

    # renderer_classes = [renderers.JSONRenderer, renderers.BrowsableAPIRenderer]
    # template_name = 'pizza_shop/list2.html'
    # template_name = 'pizza_shop/list_app.html'

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context["cart_product_form"] = CartAddProductForm()  # передаём корзину в html
    #     context["title"] = 'Список пицц для заказа'
    #     return context
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['cart_product_form'] = CartAddProductForm()  # передаём корзину в html
    #     context['title'] = 'Список пицц для заказа'
    #     context['category'] = 0
    #     return context


class ProductDetailView2(RetrieveAPIView):
    """Вывод сведений по одному товару (вместе с отзывами по нему)"""
    queryset = Pizza.objects.all()
    serializer_class = ProductDetailSerializer


class ProductsFromCategory2(ListAPIView):
    """Вывод всех продуктов одной категории через serializer"""
    serializer_class = PizzaSerializer

    def get_queryset(self):
        """'этот метод вместо строки queryset = ... """
        return Pizza.objects.filter(is_ready=True, type_product=self.kwargs["type_product"]).order_by('id')


class ListOfCategories2(ListAPIView):
    """Вывод всех категорий продуктов через serializer"""
    queryset = TypeOfProduct.objects.all().order_by('id')
    serializer_class = CategoriesSerializer


class FeedbackCreate2(CreateAPIView):
    """Создание отзыва для выбранного товара"""
    serializer_class = FeedbackCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def post(self, request):
    #     feedback = FeedbackCreateSerializer(data=request.data)
    #     feedback.is_valid(raise_exception=True)
    #     feedback.save(user=self.request.user)  # весь метод нужен из-за этой строки
    #     return Response({'post': feedback.data})

    def perform_create(self, serializer):
        """Переопределил метод, чтобы полю user присвоить значение актуального юзера"""
        serializer.save(user=self.request.user)


class FeedbackView2(ListAPIView):
    """Вывод отзывов на один товар"""
    serializer_class = FeedbackViewSerializer

    def get_queryset(self):
        """'этот метод вместо строки queryset = ... """
        return Feedbacks.objects.filter(product=self.kwargs["product"]).order_by('id')


class FeedbacksView(ListAPIView):
    """Вывод отзывов текущего пользователя"""
    serializer_class = FeedbacksUserSerializer

    def get_queryset(self):
        """'этот метод вместо строки queryset = ... """
        return Feedbacks.objects.filter(user=self.request.user.id).select_related('product')


# =====================================================================================================================
# ====================================== ОБЫЧНЫЕ VIEWS БЕЗ ИСПОЛЬЗОВАНИЯ REST_FRAMEWORKS ==============================
# =====================================================================================================================

def pizza_main(request):
    """Основная страница"""
    context = {
        'cart_product_form': CartAddProductForm(),  # передаём корзину в html
        'title': 'Пиццерия',
    }
    return render(request, 'pizza_shop/pizza_main.html', context)


# получение полного списка продуктов, доступных для заказа (с помощью класса)
class ListOfProduct(ListView):
    """Получение полного списка продуктов, доступных для заказа (с помощью класса)"""
    paginate_by = 3
    model = Pizza
    template_name = 'pizza_shop/list.html'

    # context_object_name = 'page_obj'  # как данные будут называться в html

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()  # передаём корзину в html
        context['title'] = 'Список пицц для заказа'
        context['category'] = 0
        return context

    def get_queryset(self):
        return Pizza.objects.filter(is_ready=True).select_related('type_product').order_by('id')


class ListProductsCategory(ListView):
    """Получение списка продуктов одной категории, доступных для заказа (с помощью класса)"""
    paginate_by = 3
    model = Pizza
    template_name = 'pizza_shop/list.html'

    #   allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # получаем уже сформированный контекст
        context['cart_product_form'] = CartAddProductForm()  # передаём корзину в html
        context['title'] = TypeOfProduct.objects.get(pk=self.kwargs['type_id'])
        # в title присваиваем название категории товара
        context['category'] = self.kwargs['type_id']
        return context

    def get_queryset(self):
        return Pizza.objects.filter(type_product=self.kwargs['type_id'], is_ready=True).select_related('type_product')


#        return Pizza.objects.filter(type_product__slug=self.kwargs['type_slug'], is_ready=True)
#       такой запрос был бы, если использовать отбор по слагу.
#       В urls.py должен быть <int:type_slug> вместо <int:type_id>


class ShowProduct(DetailView):
    """Просмотр одного товара вместе с отзывами по нему (с помощью класса)"""
    model = Pizza
    template_name = 'pizza_shop/show_product.html'
    pk_url_kwarg = 'product_id'  # название параметра, который передаёт в класс id (или pk)
    # slug_url_kwarg = 'product_slug'  # если используется слаг вместо id
    context_object_name = 'pizza_item'  # под этим именем в html используется наша модель

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()  # передаём корзину в html
        context['title'] = Pizza.objects.get(pk=self.kwargs['product_id'])  # в title присваиваем название товара
        context['feedbacks'] = Feedbacks.objects.filter(product=self.kwargs['product_id'])  # отзывы
        context['category'] = Pizza.objects.get(pk=self.kwargs['product_id']).type_product
        return context


class AddFeedback(CreateView):
    """Добавление нового отзыва"""
    #    model = Feedbacks                          # это для описания через модель
    #    fields = ['buyer', 'product', 'comment']   # это для описания через модель

    form_class = AddFeedbackForm  # если работаем через форму, а не через модель
    template_name = 'pizza_shop/feedbacks_form.html'
    success_url = reverse_lazy('list')  # перенаправление пользователя на эту страницу после ввода отзыва

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оставьте отзыв о товаре'
        context['buyer'] = self.request.user
        return context

        # if context['user'].is_authenticated:
        #     AddFeedbackForm.buyer = context['user'].username
        # return context

        # {% if request.user.is_authenticated %}
        #     {% form['buyer'] = request.user.username %}
        # {% else %}
        #     {% form['buyer'] = "Анонимный покупатель" %}
        # {% endif %}


# просмотр одного отзыва
class ShowFeedback(DetailView):
    model = Feedbacks
    template_name = 'pizza_shop/feedback.html'
    pk_url_kwarg = 'feedback_id'  # название параметра, который передаёт в класс id (или pk)
    context_object_name = 'feedback'  # под этим именем в html используется наша модель

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context


# добавление нового пользователя
class RegisterUser(CreateView):
    form_class = RegisterUserForm  # если работаем через форму, а не через модель
    template_name = 'pizza_shop/register.html'
    success_url = reverse_lazy('list')  # перенаправление пользователя на эту страницу после регистрации

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('list')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'pizza_shop/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('list')


def logout_user(request):
    logout(request)
    return redirect('login')

# @require_POST
# def cart_add_list(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Pizza, pk=product_id)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
#     return render(request)

# ================================== АРХИВ =======================================================================
# from django.core.paginator import Paginator

# получение списка продуктов одной категории, доступных для заказа (через функцию)
# def get_product(request, type_id):
#     pizza = Pizza.objects.filter(type_product_id=type_id, is_ready=True)
#     currentType = TypeOfProduct.objects.get(pk=type_id)
#     cart_product_form = CartAddProductForm()  # корзина
#     paginator = Paginator(pizza, 2)
#     page_num = request.GET.get('page', 1)  # 1 - по умолчанию
#     page_objects = paginator.get_page(page_num)
#     context = {'pizza': pizza,
#                'cart_product_form': cart_product_form,
#                'title': currentType,
#                'page_obj': page_objects
#                }
#     return render(request, 'pizza_shop/list.html', context)


# просмотр одного товара (вместе с отзывами по нему)
# def show_product(request, product_id):
#     pizza_item = get_object_or_404(Pizza, pk=product_id)  # сам товар
#     feedbacks = Feedbacks.objects.filter(product=product_id)  # отзывы
#     cart_product_form = CartAddProductForm()  # корзина
#
#     context = {'pizza_item': pizza_item,
#                'feedbacks': feedbacks,
#                'cart_product_form': cart_product_form,
#                'title': pizza_item.name
#                }
#     return render(request, 'pizza_shop/show_product.html', context)


# получение полного списка продуктов, доступных для заказа
# def pizza_list(request):
#     pizza = Pizza.objects.filter(is_ready=True)
#     cart_product_form = CartAddProductForm()  # корзина
#     paginator = Paginator(pizza, 2)
#     page_num = request.GET.get('page', 1)  # 1 - по умолчанию
#     page_objects = paginator.get_page(page_num)
#     context = {'pizza': pizza,
#                'cart_product_form': cart_product_form,
#                'title': 'Список пицц для заказа',
#                'page_obj': page_objects
#                }
#     return render(request, 'pizza_shop/list.html', context)
