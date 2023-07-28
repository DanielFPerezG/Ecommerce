from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

from .forms import ProductForm, TopicForm, BannerForm
from .models import User, Topic, Product, Banner, PurchaseOrder
from .helpers import ImageHandler
import tempfile
import os


# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

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
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')

    context= {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def home(request):
    return render(request, 'base/home.html')

@login_required(login_url='login')
def createProduct(request):
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        price = int(request.POST.get('price'))
        discount = int(request.POST.get('discount'))
        topic, created = Topic.objects.get_or_create(name=topic_name)
        if discount>0:
            priceDiscount = price - (price*(discount/100))
        else:
            priceDiscount = price

        # Save image to temporary file
        img = request.FILES['image']
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(img.read())
            temp_file.flush()

        imgDetail = request.FILES['imageDetail']
        with tempfile.NamedTemporaryFile(delete=False) as temp_fileDetail:
            temp_fileDetail.write(imgDetail.read())
            temp_fileDetail.flush()

        imgDetailSecond = request.FILES['imageDetailSecond']
        with tempfile.NamedTemporaryFile(delete=False) as temp_fileDetailSecond:
            temp_fileDetailSecond.write(imgDetailSecond.read())
            temp_fileDetailSecond.flush()


        product = Product(
            topic=topic,
            name=request.POST.get('name'),
            message=request.POST.get('message'),
            bio=request.POST.get('bio'),
            price=price,
            cost=request.POST.get('cost'),
            discount=discount,
            stock=request.POST.get('stock'),
            priceDiscount=priceDiscount
        )

        # Change image resolution
        ImageHandler.save_resized_image_create(temp_file, img, object = product, type = "productHome")
        ImageHandler.save_resized_image_create(temp_fileDetail, imgDetail, object=product, type="productDetail")
        ImageHandler.save_resized_image_create(temp_fileDetailSecond, imgDetailSecond, object=product, type="productDetailSecond")

        product.save()

        # Remove temporary file
        os.remove(temp_file.name)
        return redirect('adminProduct')
    
    return render(request, 'base/createProduct.html', {'topics':topics})

@login_required(login_url='login')
def adminProduct(request):
    products = Product.objects.all()

    return render(request, 'base/adminProduct.html', {'products':products})

@login_required(login_url='login')
def deleteProduct(request,pk):
    product = Product.objects.get(id=pk)
    product.delete()

    return redirect('adminProduct')


@login_required(login_url='login')
def updateProduct(request,pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    img = product.image
    img_name = img.name

    if request.method == 'POST':
        if 'submit' in request.POST:
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()

                if product.priceDiscount>0:
                    priceDiscount = product.price - (product.price*(product.discount/100))
                else:
                    priceDiscount = product.price

                product.priceDiscount =priceDiscount
                product.save()


                return redirect('adminProduct')

    return render(request,'base/updateProduct.html', {'form':form, 'product':product})

@login_required(login_url='login')
def adminTopic(request):
    topics = Topic.objects.all()

    return render(request, 'base/adminTopic.html', {'topics':topics})

@login_required(login_url='login')
def updateTopic(request,pk):
    topic = Topic.objects.get(id=pk)
    form = TopicForm(instance=topic)

    if request.method == 'POST':
        if 'submit' in request.POST:
            form = TopicForm(request.POST, request.FILES, instance=topic)
            if form.is_valid():
                form.save()
                return redirect('adminTopic')

    return render(request,'base/updateTopic.html', {'form':form, 'topic':topic})

@login_required(login_url='login')
def createBanner(request):
    topics = Topic.objects.all()

    if request.method == "POST":
        type = request.POST.get('type')
        title = request.POST.get('title')
        message=request.POST.get('message')
        # Save image to temporary file
        img = request.FILES['image']
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(img.read())
            temp_file.flush()

        if type == "Categoria":
            topic_name = request.POST.get('topic')
            topic, created = Topic.objects.get_or_create(name=topic_name)

            banner = Banner.objects.create(
                topic=topic,
                title=title,
                message=message,
                type=type
                )
            # Change image resolution
            ImageHandler.save_resized_image_create(temp_file, img, object=banner, type="banner")
            banner.save()
            # Remove temporary file
            os.remove(temp_file.name)
            return redirect('home')
        
        elif type == "Precio Maximo":
            maxPrice = int(request.POST.get('maxPrice'))
            banner = Banner.objects.create(
                maxPrice=maxPrice,
                title=title,
                message=message,
                type=type
                )

            # Change image resolution
            ImageHandler.save_resized_image_create(temp_file, img, object=banner, type="banner")
            # Remove temporary file
            os.remove(temp_file.name)
            return redirect('home')
        
        elif type == "Rango de Precio":
            maxPrice = int(request.POST.get('maxPrice'))
            minPrice = int(request.POST.get('minPrice'))
            banner = Banner.objects.create(
                maxPrice=maxPrice,
                minPrice=minPrice,
                title=title,
                message=message,
                type=type
                )

            # Change image resolution
            ImageHandler.save_resized_image_create(temp_file, img, object=banner, type="banner")
            # Remove temporary file
            os.remove(temp_file.name)
            return redirect('home')
        
        elif type == "Descuento Minimo":
            minDiscount = int(request.POST.get('minDiscount'))
            banner = Banner.objects.create(
                minDiscount=minDiscount,
                title=title,
                message=message,
                type=type
                )

            # Change image resolution
            ImageHandler.save_resized_image_create(temp_file, img, object=banner, type="banner")
            # Remove temporary file
            os.remove(temp_file.name)
            return redirect('home')

    
    return render(request, 'base/createBanner.html', {'topics':topics})

@login_required(login_url='login')
def updateBanner(request,pk):
    banner = Banner.objects.get(id=pk)
    form = BannerForm(instance=banner)

    if request.method == 'POST':
        if 'submit' in request.POST:
            form = BannerForm(request.POST, request.FILES, instance=banner)
            if form.is_valid():
                form.save()
                return redirect('adminBanner')

    return render(request,'base/updateBanner.html', {'form':form, 'banner':banner})

@login_required(login_url='login')
def adminBanner(request):
    banners = Banner.objects.all()

    return render(request, 'base/adminBanner.html', {'banners': banners})

@login_required(login_url='login')
def deleteBanner(request,pk):
    banner = Banner.objects.get(id=pk)
    banner.delete()

    return redirect('adminBanner')

@login_required(login_url='login')
def adminOrder(request):
    orders = PurchaseOrder.objects.all().order_by('-createdAt')

    return render(request, 'base/adminOrder.html', {'orders':orders})