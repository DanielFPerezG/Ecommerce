from django.shortcuts import render

from base.models import Product

# Create your views here.


def home(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'store/home.html', context)