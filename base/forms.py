from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Topic, Banner
from django.forms import ModelForm, Textarea

from .helpers import ImageHandler

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['image', 'message', 'imageDetail', 'imageDetailSecond', 'name', 'topic', 'price', 'bio', 'cost', 'stock', 'discount']
        labels = {
            'name': 'Nombre',
            'message': 'Mensaje',
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

    def save(self, commit=True):
        product = super().save(commit=False)
        if self.cleaned_data.get('imageDetail') and self.cleaned_data.get(
                'imageDetailSecond') and self.cleaned_data.get('image'):
            imgDetail = self.cleaned_data['imageDetail']
            product.imageDetail.save(imgDetail.name,
                                     ImageHandler.save_resized_image_update(image=imgDetail, type='productDetail'),
                                     save=False)
            imgDetailSecond = self.cleaned_data['imageDetailSecond']
            product.imageDetailSecond.save(imgDetailSecond.name,
                                           ImageHandler.save_resized_image_update(image=imgDetailSecond,
                                                                                  type='productDetail'), save=False)
            img = self.cleaned_data['image']
            product.image.save(img.name, ImageHandler.save_resized_image_update(image=img, type='productHome'),
                               save=False)
        if commit:
            product.save()
        return product

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['image','title','bio']
        labels = {
            'bio': 'Descripción',
        }
        widgets = {
            'bio': Textarea(attrs={'class': 'form-control', 'rows': 3}),  # Usa el widget Textarea para 'bio'
        }

    def save(self, commit=True):
        topic = super().save(commit=False)
        if self.cleaned_data.get('image'):
            img = self.cleaned_data['image']
            topic.image.save(img.name, ImageHandler.save_resized_image_update(img, 'Topic'), save=False)
        if commit:
            topic.save()
        return topic

class BannerForm(ModelForm):
    class Meta:
        model = Banner
        fields = ['image','title', 'message']
        labels = {
            'title': 'Titulo del Banner',
            'message': 'Mensaje del Banner',
        }

    def save(self, commit=True):
        banner = super().save(commit=False)
        if self.cleaned_data.get('image'):
            img = self.cleaned_data['image']
            banner.image.save(img.name, ImageHandler.save_resized_image_update(img, 'Banner'), save=False)
        if commit:
            banner.save()
        return banner