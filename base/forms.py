from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Topic
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
        fields = ['image']
