from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Topic


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['image','name','topic', 'price','bio','cost','stock','discount']

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['image']
