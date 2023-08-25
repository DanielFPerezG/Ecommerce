from django.db import models
from django.contrib.auth.models import AbstractUser

import os
import json


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    lastName = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    phone = models.PositiveIntegerField(null=True)
    card = models.PositiveIntegerField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    complement = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.address


class Topic(models.Model):
    def get_topic_image_path(instance, filename):
        return 'topic/{}'.format(filename)
    name = models.CharField(max_length=200)
    bio = models.CharField(max_length=400)
    title = models.CharField(null=True, max_length=200)
    image = models.ImageField(null=True, upload_to=get_topic_image_path)

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super(Topic, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            old_image = Topic.objects.get(pk=self.pk).image
            if self.image and old_image != self.image:
                if os.path.isfile(old_image.path):
                    os.remove(old_image.path)
        super(Topic, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    def get_product_image_path(instance, filename, field=None):
        if field:
            # Check if the instance already has an image for the field
            if instance.pk and hasattr(instance, field):
                # Get the current image filename for the field
                current_filename = os.path.basename(getattr(instance, field).path)

                # Remove the existing image file for the field
                os.remove(getattr(instance, field).path)

                # Return the existing image path for the field
                return f'product/{field}/{current_filename}'
            else:
                # Return the regular image path if it's a new instance
                return f'product/{field}/{filename}'
        else:
            # Default path when 'field' is not provided (e.g., during creation)
            return f'product/{filename}'

    name = models.CharField(max_length=150,null=True)
    message = models.CharField(max_length=150, null=True)
    bio = models.CharField(max_length=1000,null=True)
    image = models.ImageField(null=True, upload_to=get_product_image_path)
    imageDetail = models.ImageField(null=True, upload_to=get_product_image_path)
    imageDetailSecond = models.ImageField(null=True, upload_to=get_product_image_path)
    price = models.PositiveIntegerField(null=True)
    stock = models.PositiveIntegerField(null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    cost = models.PositiveIntegerField(null=True)
    discount = models.PositiveIntegerField(null=True)
    priceDiscount = models.PositiveIntegerField(null=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.image.path):
            os.remove(self.image.path)
        if os.path.isfile(self.imageDetail.path):
            os.remove(self.imageDetail.path)
        if os.path.isfile(self.imageDetailSecond.path):
            os.remove(self.imageDetailSecond.path)
        super(Product, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Store the current image paths
        old_image_path = self.image.path if self.pk else None
        old_image_detail_path = self.imageDetail.path if self.pk else None
        old_image_detail_second_path = self.imageDetailSecond.path if self.pk else None

        super(Product, self).save(*args, **kwargs)

        # Check if image paths have changed and remove old images
        if old_image_path and self.image.path != old_image_path:
            if os.path.isfile(old_image_path):
                os.remove(old_image_path)

        if old_image_detail_path and self.imageDetail.path != old_image_detail_path:
            if os.path.isfile(old_image_detail_path):
                os.remove(old_image_detail_path)

        if old_image_detail_second_path and self.imageDetailSecond.path != old_image_detail_second_path:
            if os.path.isfile(old_image_detail_second_path):
                os.remove(old_image_detail_second_path)


    def __str__(self):
        return self.name

    class Meta:
        order_with_respect_to = 'discount'

class Banner(models.Model):
    def get_banner_image_path(instance, filename):
        return 'banner/{}'.format(filename)

    title = models.CharField(max_length=150,null=True)
    type = models.CharField(max_length=150,null=True)
    message = models.CharField(max_length=150,null=True)
    image = models.ImageField(null=True, upload_to=get_banner_image_path)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    minPrice = models.PositiveIntegerField(null=True)
    maxPrice = models.PositiveIntegerField(null=True)
    minDiscount = models.PositiveIntegerField(null=True)

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super(Banner, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            old_banner = Banner.objects.get(pk=self.pk)
            if old_banner.image and self.image != old_banner.image and os.path.isfile(old_banner.image.path):
                os.remove(old_banner.image.path)
        super(Banner, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.TextField(default='[]')

    def add_product(self, product):
        if not self.pk:
            self.save()
        products_list = json.loads(self.products)
        for p in products_list:
            if p['id'] == product.id:
                p['quantity'] += 1
                p['total'] = p['price'] * p['quantity']
                break

        else:
            products_list.append({
                'id': product.id,
                'name': product.name,
                'price': int(product.priceDiscount),
                'quantity': 1,
                'image_url': product.image.url,
                'total': int(product.priceDiscount)*1
            })
        self.products = json.dumps(products_list)
        self.save()

    def delete_product(self, product_id):
        products_list = json.loads(self.products)
        for i, p in enumerate(products_list):
            if p['id'] == product_id:
                products_list.pop(i)
        self.products = json.dumps(products_list)
        self.save()

    def obtain_products(self):
        products_list = json.loads(self.products)
        products = []
        for p in products_list:
            product = {
                'id': p['id'],
                'name': p['name'],
                'price': p['price'],
                'quantity': p['quantity'],
                'image_url': p['image_url'],
                'total':p['total']
            }
            products.append(product)
        return products


class PurchaseOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    products = models.TextField(default='[]')
    status = models.CharField(max_length=100, null=True)
    total = models.PositiveIntegerField(null=True)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    complement = models.CharField(max_length=150)
    shippingCompany = models.CharField(max_length=100, null=True)
    shippingGuide = models.CharField(max_length=100, null=True)
    shippingCost = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.pk

class PurchaseOrderItem(models.Model):
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    productName = models.CharField(max_length=150)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    boughtAt = models.DateTimeField(auto_now_add=True)
    orderStatus = models.CharField(max_length=100)

class ShippingCost(models.Model):
    cost = models.IntegerField(default=15000)

    def __str__(self):
        return str(self.cost)