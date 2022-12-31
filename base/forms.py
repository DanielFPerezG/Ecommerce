from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['image','name','topic', 'price','bio','cost','stock']
