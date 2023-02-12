from django.shortcuts import render

from base.models import Product, Topic, Banner

# Create your views here.


def home(request):
    products = Product.objects.all().order_by('-discount')
    topics = Topic.objects.all()
    banners = Banner.objects.all()
    discount_10 = 0
    discount_20 = 0

    for product in products:
        if product.discount >= 10:
            discount_10+=1
        if product.discount >= 20:
            discount_20+=1


    context = {
        'products':products,
        'topics':topics,
        'banners':banners,
        'discount_10':discount_10,
        'discount_20':discount_20}
    return render(request, 'store/home.html', context)


def shopDetail(request,pk):
    product = Product.objects.get(id=pk)
    topics = Topic.objects.all()

    context = {
        'product':product,
        'topics':topics
        }

    return render(request,'store/shopDetail.html', context)