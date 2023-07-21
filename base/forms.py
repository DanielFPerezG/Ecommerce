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

        if not product.pk:
            # New product, save normally
            if commit:
                product.save()
        else:
            # Existing product, check for image changes
            old_product = Product.objects.get(pk=product.pk)

            if self.cleaned_data.get('image') and self.cleaned_data['image'] != old_product.image:
                product.image = self.cleaned_data['image']
                # Get the corresponding 'type' for the ImageHandler function
                image_type = 'productHome'
                product.image.storage.save(
                    Product.get_product_image_path(product, product.image.name, 'image'),
                    ImageHandler.save_resized_image_update(image=product.image, type=image_type)
                )

            if self.cleaned_data.get('imageDetail') and self.cleaned_data['imageDetail'] != old_product.imageDetail:
                product.imageDetail = self.cleaned_data['imageDetail']
                # Get the corresponding 'type' for the ImageHandler function
                image_type = 'productDetail'
                product.imageDetail.storage.save(
                    Product.get_product_image_path(product, product.imageDetail.name, 'imageDetail'),
                    ImageHandler.save_resized_image_update(image=product.imageDetail, type=image_type)
                )

            if self.cleaned_data.get('imageDetailSecond') and self.cleaned_data['imageDetailSecond'] != old_product.imageDetailSecond:
                product.imageDetailSecond = self.cleaned_data['imageDetailSecond']
                # Get the corresponding 'type' for the ImageHandler function
                image_type = 'productDetailSecond'
                product.imageDetailSecond.storage.save(
                    Product.get_product_image_path(product, product.imageDetailSecond.name, 'imageDetailSecond'),
                    ImageHandler.save_resized_image_update(image=product.imageDetailSecond, type=image_type)
                )

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