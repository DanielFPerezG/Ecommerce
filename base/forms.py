from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Topic, Banner
from django.forms import ModelForm, Textarea


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['image','name','topic', 'price','bio','cost','stock','discount']
        labels = {
            'name': 'Nombre',
            'topic': 'Categoría',
            'price': 'Precio',
            'bio': 'Descripción',
            'cost': 'Costo',
            'stock': 'Inventario',
            'discount': 'Descuento'
        }
        widgets = {
            'bio': Textarea(attrs={'class': 'form-control', 'rows': 3}),  # Usa el widget Textarea para 'bio'
        }

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['image','bio']
        labels = {
            'bio': 'Descripción',
        }
        widgets = {
            'bio': Textarea(attrs={'class': 'form-control', 'rows': 3}),  # Usa el widget Textarea para 'bio'
        }

class BannerForm(ModelForm):
    class Meta:
        model = Banner
        fields = ['image','title', 'message']
        labels = {
            'title': 'Titulo del Banner',
            'message': 'Mensaje del Banner',
        }