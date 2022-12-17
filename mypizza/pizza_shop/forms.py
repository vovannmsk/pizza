from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

from .models import *


""" Форма добавления нового отзыва о товаре"""
class AddFeedbackForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].empty_label = "Продукт не выбран"

    class Meta:
        model = Feedbacks
        fields = ['buyer', 'product', 'comment']
        widgets = {
            'buyer': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-control'}),
        }

    # buyers = forms.CharField(max_length=50, default="Анонимный покупатель", label="Имя")
    # product = forms.ModelChoiceField(queryset=Pizza.objects.filter(is_ready=True), initial=1, label="Продукт", empty_label="продукт не выбран")
    # comment = forms.CharField(max_length=200, label="Ваш отзыв")


# форма для регистрации нового пользователя
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

#форма для входа на сайт по логину и паролю
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))