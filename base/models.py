from django.db import models
from django.contrib.auth.models import AbstractUser

import os
import json

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    lastName = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    phone = models.PositiveIntegerField(null=True)
    state = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=200)
    bio = models.CharField(max_length=1000,null=True)
    image = models.ImageField(null=True, upload_to='topic/')

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
    name = models.CharField(max_length=150,null=True)
    bio = models.CharField(max_length=1000,null=True)
    image = models.ImageField(null=True, upload_to='product/')
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
        super(Product, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            old_image = Product.objects.get(pk=self.pk).image
            if self.image and old_image != self.image:
                if os.path.isfile(old_image.path):
                    os.remove(old_image.path)
        super(Product, self).save(*args, **kwargs)


    def __str__(self):
        return self.name

    class Meta:
        order_with_respect_to = 'discount'

class Banner(models.Model):

    title = models.CharField(max_length=150,null=True)
    type = models.CharField(max_length=150,null=True)
    message = models.CharField(max_length=150,null=True)
    image = models.ImageField(null=True, upload_to='banner/')
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
                'price': int(product.price),
                'quantity': 1,
                'image_url': product.image.url,
                'total': int(product.price)*1
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