from django.shortcuts import render

from base.models import Product, Topic

# Create your views here.


def home(request):
    products = Product.objects.all().order_by('-discount')
    topics = Topic.objects.all()

    context = {'products':products,'topics':topics}
    return render(request, 'store/home.html', context)