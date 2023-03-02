from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from base.models import Product, Topic, Banner, User

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
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('store:home')

def registerPage(request):
    pass
    # page = 'register'
    # form = MyUserCreationForm()

    # if request.method == 'POST':
    #     form = MyUserCreationForm(request.POST)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         user.username = user.username.lower()
    #         user.save()
    #         login(request, user)
    #         return redirect('home')
    #     else:
    #         messages.error(request, 'An error occurred during registration')


    # return render(request, 'base/login_register.html',{'form':form})

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