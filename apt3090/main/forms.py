from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'



class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'user', 'email', 'phone']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerProfileForm(ModelForm):
    class Meta:
        model = Customer
        fields ='__all__'


class CreditCardForm(ModelForm):
    class Meta:
        model = CreditCard
        fields = '__all__'
