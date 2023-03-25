from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator

from django.db.models import Q
from base.models import Product, Topic, Banner, User

from store.forms import UserForm, MyUserCreationForm

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email = email)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, email = email, password=password)

        if user is not None:
            login(request, user)
            return redirect('store:home')
        else:
            messages.error(request, 'Username or password is incorrect')

    context= {'page': page}
    return render(request, 'store/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('store:home')

def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'page': page, 'form':form}
    return render(request, 'store/login_register.html',context)

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
    products = Product.objects.all()
    topics = Topic.objects.all()

    context = {
        'products':products,
        'product':product,
        'topics':topics
        }

    return render(request,'store/shopDetail.html', context)

def store(request):
    query = request.GET.get('q') if request.GET.get('q') != None else ''
    query_max_price = request.GET.get('q_max_price') if request.GET.get('q_max_price') != None else ''
    query_min_price = request.GET.get('q_min_price') if request.GET.get('q_min_price') != None else ''
    query_min_discount = request.GET.get('q_min_discount') if request.GET.get('q_min_discount') != None else ''
    order_by = request.GET.get('order_by', 'default_orders') 
    topics = Topic.objects.all()

    if query_max_price != '' and query_min_price != '': 
        products = Product.objects.filter(
            Q(price__gte=query_min_price) &
            Q(price__lte=query_max_price))
    elif query_max_price != '': 
        products = Product.objects.filter(
            Q(price__lte=query_max_price)
            )
    elif query_min_discount != '': 
        products = Product.objects.filter(
            Q(discount__gte=query_min_discount)
            )
        print('hpt')
    elif query:
        products = Product.objects.filter(
            Q(topic__name__icontains = query)|
            Q(name__icontains= query)|
            Q(bio__icontains= query)
        )
    else: 
        products = Product.objects.all()
    
    if order_by=="priceDiscount":
        products = products.order_by('priceDiscount')
    elif order_by=="-priceDiscount":
        products = products.order_by('-priceDiscount')
    elif order_by=="name":
        products = products.order_by('name')
    elif order_by=="-name":
        products = products.order_by('-name')
    elif order_by=="discount":
        products = products.order_by('discount')
    elif order_by=="-discount":
        products = products.order_by('-discount')
    
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    products = page_obj.object_list

    context = {'products':products,'topics':topics,'query':query,'page_obj':page_obj,'products':products,'order_by':order_by}
    return render(request, 'store/store.html', context)
