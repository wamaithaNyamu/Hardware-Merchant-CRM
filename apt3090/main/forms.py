from django.forms import ModelForm
from .models import *


class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'


class InternForm(ModelForm):
	class Meta:
		model = Intern
		fields = '__all__'


class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = '__all__'

class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'