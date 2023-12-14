from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.hashers import check_password
from django.views.decorators.cache import never_cache
from django.utils import timezone

from django.db.models import Q, F
from base.models import Product, Topic, Banner, User, Cart, UserAddress, PurchaseOrder, PurchaseOrderItem, ShippingCost, Cupon

from .helpers import ProductCart, CuponAdmin

from cookie_consent.views import CookieGroupAcceptView

from store.forms import UserForm, MyUserCreationForm

from datetime import timedelta
import string
import random
import json

def cookiePolicy(request):
    return render(request, 'store/cookiePolicy.html')

def usePolicy(request):
    return render(request, 'store/usePolicy.html')
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'El correo electrónico no está registrado')
            return redirect('store:login')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('store:home')
        else:
            messages.error(request, 'El correo electrónico o la contraseña son incorrectos')

    context = {'page': page, 'messages': messages.get_messages(request)}
    return render(request, 'store/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('store:home')

def registerPage(request):
    page = 'register'

    if request.method == 'POST':
        name = request.POST.get('name').capitalize()
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        acceptUsePolicy = request.POST.get('usePolicy')
        acceptCommPolicy = request.POST.get('commPolicy')

        # Check if the user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electronico ya está en uso.')
            return redirect('store:register')

        # Verify if passwords match
        if password != confirmPassword:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('store:register')

        if not acceptUsePolicy:
            messages.error(request, 'Es necesario que aceptes las políticas de privacidad y condiciones de uso para registrarte.')
            return redirect('store:register')

        # Create user
        user = User.objects.create_user(username=email, email=email, password=password, name=name)
        if acceptCommPolicy:
            user.commPolicy = True
        user.save()

        # Authenticate and login the user
        user = authenticate(request, username=email, password=password)

        # Envía el correo electrónico con la nueva contraseña utilizando la plantilla HTML
        subject = '¡Bienvenido a Edjo!'
        from_email = 'danielfeperezgalindo@gmail.com'  # Coloca aquí tu dirección de correo Gmail
        recipient_list = [email]

        cuponName = CuponAdmin.FirstOrderCupon(user)


        # Renderiza la plantilla HTML con los datos necesarios
        html_message = render_to_string('email/cuponFirstOrder.html', {'cuponName': cuponName.cupon, 'value': cuponName.value})
        plain_message = strip_tags(html_message)

        # Crea el objeto EmailMultiAlternatives para enviar el correo con contenido HTML y texto plano
        msg = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list)
        msg.attach_alternative(html_message, "text/html")
        msg.send()


        if user is not None:
            login(request, user)
            return redirect('store:home')

    context = {'page': page, 'messages': messages.get_messages(request)}
    return render(request, 'store/login_register.html',context)

def generateRandomPassword(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def resetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            newPassword = generateRandomPassword()
            user.set_password(newPassword)
            user.save()

            # Envía el correo electrónico con la nueva contraseña utilizando la plantilla HTML
            subject = 'Solicitud de cambio de contraseña'
            from_email = 'danielfeperezgalindo@gmail.com'  # Coloca aquí tu dirección de correo Gmail
            recipient_list = [email]

            # Renderiza la plantilla HTML con los datos necesarios
            html_message = render_to_string('email/resetPasswordEmail.html', {'newPassword': newPassword})
            plain_message = strip_tags(html_message)

            # Crea el objeto EmailMultiAlternatives para enviar el correo con contenido HTML y texto plano
            msg = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list)
            msg.attach_alternative(html_message, "text/html")
            msg.send()

            return redirect('store:login')
        except User.DoesNotExist:
            messages.error(request, 'El correo electronico no esta registrado.')
            return redirect('store:resetPassword')

    return render(request, 'store/resetPassword.html')

def home(request):
    topics = Topic.objects.all()
    banners = Banner.objects.all()
    products = Product.objects.order_by('-discount')

    if request.user.is_authenticated:
        cart, create = Cart.objects.get_or_create(user=request.user)
        numberProductsCart = ProductCart.numberProducts(cart)

        context = {
            'topics': topics,
            'banners': banners,
            'numberProductsCart': numberProductsCart,
            'products': products}

    else:
        context = {
            'topics': topics,
            'banners': banners,
            'products': products}

    # Iterate through topics and handle instances with no image assigned
    for topic in topics:
        if topic.image and topic.image.file:
            topic.image_url = topic.image.url
        else:
            topic.image_url = None

    return render(request, 'store/home.html', context)


def shopDetail(request,pk):
    product = Product.objects.get(id=pk)
    products = Product.objects.all()
    topics = Topic.objects.all()

    if request.user.is_authenticated:
        cart, create = Cart.objects.get_or_create(user=request.user)
        numberProductsCart = ProductCart.numberProducts(cart)

        context = {
            'products':products,
            'product':product,
            'topics':topics,
            'numberProductsCart':numberProductsCart
            }
    else:
        context = {
            'products': products,
            'product': product,
            'topics': topics
        }

    return render(request,'store/shopDetail.html', context)

def store(request):
    query = request.GET.get('q') if request.GET.get('q') != None else ''
    query_max_price = request.GET.get('q_max_price') if request.GET.get('q_max_price') != None else ''
    query_min_price = request.GET.get('q_min_price') if request.GET.get('q_min_price') != None else ''
    query_min_discount = request.GET.get('q_min_discount') if request.GET.get('q_min_discount') != None else ''
    order_by = request.GET.get('order_by', 'default_orders') 
    topics = Topic.objects.all()
    if request.user.is_authenticated:
        cart, create = Cart.objects.get_or_create(user=request.user)
        numberProductsCart = ProductCart.numberProducts(cart)

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
        products = Product.objects.all().order_by('-discount')
    
    if order_by=="priceDiscount":
        products = products.order_by('priceDiscount')
    elif order_by=="-priceDiscount":
        products = products.order_by('-priceDiscount')
    elif order_by=="name":
        products = products.order_by('name')
    elif order_by=="-name":
        products = products.order_by('-name')
    elif order_by=="discount":
        products = products.order_by('-discount')
    elif order_by=="-discount":
        products = products.order_by('discount')
    
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    products = page_obj.object_list

    if request.user.is_authenticated:
        context = {'products':products,'topics':topics,'query':query,'page_obj':page_obj,'products':products,'order_by':order_by,'numberProductsCart':numberProductsCart}
    else:
        context = {'products': products, 'topics': topics, 'query': query, 'page_obj': page_obj, 'products': products, 'order_by': order_by,}
    return render(request, 'store/store.html', context)

@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@login_required(login_url='login')
def addCart(request,pk):
    product = Product.objects.get(id=pk)
    cart, create = Cart.objects.get_or_create(user=request.user)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart.add_product(product)

    numberProductsCart = ProductCart.numberProducts(cart)
    newProductCarts = ProductCart.newProductCart(cart, product)
    numberProductsCart = json.dumps(numberProductsCart)
    newProductCarts = json.dumps(newProductCarts)

    data = {"json1": numberProductsCart, "json2": newProductCarts}
    data = json.dumps(data)
    return HttpResponse(data)

def addCartDetail(request,pk):
    product = Product.objects.get(id=pk)
    cart, create = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart.add_product(product)
        data = json.loads(request.body)
        productCart = cart.obtain_products()

        for i in data:
            for productDetail in productCart:
                if productDetail["id"] == int(i["id"]):
                    productDetail["quantity"] = int(i["quantity"])
                    productDetail["total"] = productDetail["price"] * productDetail["quantity"]
                    break

        cart.products = productCart
        cart.products = json.dumps(cart.products)
        cart.save()
        return JsonResponse({'success': True, 'message': 'Producto agregado al carrito exitosamente'})
    return JsonResponse({})

@never_cache
def viewCart(request):
    cost = ShippingCost.objects.first()
    cart = Cart.objects.get(user=request.user)
    products = Product.objects.all()
    numberProductsCart = ProductCart.numberProducts(cart)
    subTotal = ProductCart.subtotalCart(cart,'cart')
    total = subTotal + cost.cost
    productCartWithStock = ProductCart.productCartWithStock(cart, products)

    context = {'cart': cart, 'productCart': productCartWithStock,'numberProductsCart': numberProductsCart, 'subTotal': subTotal, 'total': total, 'cost': cost}
    return render(request, 'store/viewCart.html', context)

@csrf_exempt
def updateCart(request):
    cart = Cart.objects.get(user=request.user)
    productCart = cart.obtain_products()
    shippingCost = ShippingCost.objects.first()

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)

        for product in productCart:
            for i in data:
                if product["id"] == int(i["id"]):
                    product["quantity"] = int(i["quantity"])
            if product["quantity"] == 0:
                cart.delete_product(product["id"])

            product["total"] = product["price"]*product["quantity"]
            product["shippingCost"] = shippingCost.cost
        cart.products = productCart
        cart.products = json.dumps(cart.products)
        cart.save()
        productCart = json.dumps(productCart)
    return HttpResponse(productCart)

def deleteCart(request,pk):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        cart.delete_product(int(pk))
        cart.save()
    return redirect('store:viewCart')

def userProfile(request):
    cart = Cart.objects.get(user=request.user)
    numberProductsCart = ProductCart.numberProducts(cart)

    context = {'numberProductsCart': numberProductsCart}
    return render(request, 'store/userProfile.html', context)

def personalInformation(request):
    cart = Cart.objects.get(user=request.user)
    numberProductsCart = ProductCart.numberProducts(cart)

    context = {'numberProductsCart': numberProductsCart}
    return render(request, 'store/personalInformation.html', context)


@csrf_exempt
def updateUserInfo(request,pk):

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':

        if request.user.id == int(pk):
            data = json.loads(request.body)
            new_info = data.get('newInfo')
            info_type = data.get('type')

            user = User.objects.get(pk=pk)

            if info_type == 'name':
                user.name = new_info
            elif info_type == 'lastName':
                user.lastName = new_info
            elif info_type == 'card':
                user.card = new_info
            elif info_type == 'phone':
                user.phone = new_info

            user.save()

            return JsonResponse({'message': 'User information updated successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request.'})


def userAddress(request):
    cart = Cart.objects.get(user=request.user)
    addresses = UserAddress.objects.filter(user=request.user)

    numberProductsCart = ProductCart.numberProducts(cart)

    context = {'numberProductsCart': numberProductsCart, 'addresses': addresses}
    return render(request, 'store/userAddress.html', context)

@csrf_exempt
@login_required
def createAddress(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)

        address = data.get('address')
        state = data.get('state')
        city = data.get('city')
        complement = data.get('complement')

        if request.user.addresses.count() >= 5:
            return redirect('store:userAddress')
        user_address = UserAddress.objects.create(
            user=request.user,
            address=address,
            state=state,
            city=city,
            complement=complement
        )

        user_address.save()

        return JsonResponse({'message': 'User information updated successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request.'})


@csrf_exempt
@login_required(login_url='login')
def deleteAddress(request,pk):
    address = UserAddress.objects.get(id=pk)
    if address.user == request.user:
        address.delete()
        return JsonResponse({'message': 'Dirección eliminada correctamente'})

def securityInformation(request):
    cart = Cart.objects.get(user=request.user)
    numberProductsCart = ProductCart.numberProducts(cart)

    context = {'numberProductsCart': numberProductsCart}
    return render(request, 'store/securityInformation.html', context)

@login_required(login_url='login')
def deleteUser(request, pk):
    if  request.user.id == int(pk):
        user = User.objects.get(pk=pk)

        # Eliminar direcciones asociadas al usuario
        UserAddress.objects.filter(user=user).delete()

        # Limpiar campos de datos personales en el usuario
        user.username = user.name[0::-1]+str(random.randint(100, 999))+"@example.com"
        user.name = None
        user.lastName = None
        user.email = None
        user.phone = None
        user.card = None
        user.usePolicy = False
        user.commPolicy = False

        # Guardar el usuario sin datos personales
        user.save()
        logout(request)
        return redirect('store:home')

@login_required(login_url='login')
def updatePassword(request,pk):

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.id == int(pk):
            data = json.loads(request.body)
            lastPassword = data.get('lastPassword')
            newPassword = data.get('newPassword')
            confirmPassword = data.get('confirmPassword')

            user = User.objects.get(pk=pk)

            # Verify if passwords match
            if not check_password(lastPassword, user.password):
                return JsonResponse({'error': 'La contraseña actual es incorrecta.'})

            if newPassword != confirmPassword:
                return JsonResponse({'error': 'La nueva contraseña no es igual.'})


            user.set_password(newPassword)

            user.save()

            return JsonResponse({'message': 'User information updated successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request.'})


def checkout(request):
    cart = Cart.objects.get(user=request.user)
    addresses = UserAddress.objects.filter(user=request.user)
    addresses_json = json.dumps(list(addresses.values()))
    cost = ShippingCost.objects.first()
    cart.cupon = None
    cart.save()

    products = Product.objects.all()
    numberProductsCart = ProductCart.numberProducts(cart)
    productCartWithStockCheckout = ProductCart.productCartWithStockCheckout(cart, products)
    subTotal = ProductCart.subtotalCart(productCartWithStockCheckout, 'checkout')
    total = subTotal + cost.cost
    if cart.cupon:
        subTotalDiscount = subTotal - subTotal * (cart.cupon.value/100)
        totalDiscount = subTotalDiscount + cost.cost
        context = {'subTotalDiscount': subTotalDiscount, 'totalDiscount':totalDiscount,  'cart': cart, 'productCart': productCartWithStockCheckout, 'numberProductsCart': numberProductsCart,
                   'subTotal': subTotal, 'total': total, 'addresses': addresses, 'addresses_json': addresses_json,
                   'cost': cost}
        return render(request, 'store/checkout.html', context)

    context = {'cart': cart, 'productCart': productCartWithStockCheckout,'numberProductsCart': numberProductsCart, 'subTotal': subTotal, 'total': total, 'addresses': addresses, 'addresses_json': addresses_json, 'cost': cost}
    return render(request, 'store/checkout.html', context)

def createOrder(request, pk):
    shippingCost = ShippingCost.objects.first()
    cart = Cart.objects.get(user=request.user)
    selectedAddress = UserAddress.objects.get(pk=pk)
    products = Product.objects.all()

    existing_pending_orders = PurchaseOrder.objects.filter(user=request.user, status="Pendiente de pago")
    if existing_pending_orders.exists():
        return redirect('store:checkout')
    if selectedAddress.user.id == request.user.id:
        if products:
            productCartWithStockCreateOrder = ProductCart.productCartWithStockCreateOrder(cart, products)
            subTotal = ProductCart.subtotalCart(productCartWithStockCreateOrder, '') + shippingCost.cost


            order = PurchaseOrder.objects.create(
                user=request.user,
                status="Pendiente de pago",
                address=selectedAddress.address,
                state=selectedAddress.state,
                city=selectedAddress.city,
                complement=selectedAddress.complement,
                total= subTotal,
                shippingCost=shippingCost.cost
            )

            for productJson in productCartWithStockCreateOrder:
                product = Product.objects.get(pk=productJson['id'])
                productCost =  product.cost
                productTopic = product.topic
                orderItem = PurchaseOrderItem.objects.create(
                    product = product,
                    order=order,
                    user=request.user,
                    productName=productJson['name'],
                    price=productJson['price'],
                    cost = productCost,
                    quantity=productJson['quantity'],
                    total=productJson['price']*productJson['quantity'],
                    productTopic = productTopic,
                )
                product = Product.objects.get(pk=productJson['id'])
                product.stock = product.stock - productJson['quantity']
                product.save()
                if cart.cupon:
                    orderItem.cupon  = cart.cupon
                orderItem.save()
            if cart.cupon:
                cupon = Cupon.objects.get(pk=cart.cupon.pk)
                cupon.usedCoupon += 1
                cupon.claimedBy.add(request.user)
                cupon.save()
                order.cupon = cart.cupon
                cart.cupon = None
                cart.save()

            order.products = json.dumps(productCartWithStockCreateOrder)
            order.save()

            cart.products = json.dumps([])
            cart.save()

            return JsonResponse({'message': 'Orden creada correctamente'})

def viewOrder(request):
    cart = Cart.objects.get(user=request.user)
    products = Product.objects.all()
    numberProductsCart = ProductCart.numberProducts(cart)
    orders = PurchaseOrder.objects.filter(user=request.user).order_by('-createdAt')

    context = {'cart': cart, 'numberProductsCart': numberProductsCart, 'orders': orders}
    return render(request, 'store/viewOrder.html', context)

@login_required(login_url='login')
def cancelStoreOrder(request,pk):
    order = PurchaseOrder.objects.get(id=pk)
    productOrder = json.loads(order.products)
    if order.user == request.user.id:
        for item in productOrder:
            product = Product.objects.get(id=item['id'])
            product.stock += item['quantity']
            product.save()

        order.delete()

        return JsonResponse({'message': 'Cancel order successfully.'})

def viewOrderDetail(request, pk):
    cart = Cart.objects.get(user=request.user)
    products = Product.objects.all()
    numberProductsCart = ProductCart.numberProducts(cart)
    order = PurchaseOrder.objects.get(id=pk)
    products_data = order.products
    shippingCost = ShippingCost.objects.first()
    if order.user == request.user.id:
        try:
            # Utiliza json.JSONDecoder() para cargar el JSON de forma más segura.
            decoder = json.JSONDecoder()
            productsOrder = decoder.decode(products_data)
        except json.JSONDecodeError as e:
            # Maneja cualquier error de decodificación aquí.
            # Puedes imprimir el error o registrar el contenido de 'products_data' para depurar.
            print(f"Error decoding JSON: {e}")
            print(f"Invalid JSON data: {products_data}")
            productsOrder = []

        context = {'cart': cart, 'numberProductsCart': numberProductsCart, 'order': order,  'productsOrder': productsOrder, 'ShippingCost': ShippingCost}
        return render(request, 'store/viewOrderDetail.html', context)

def validateCupon(request):
    cart = Cart.objects.get(user=request.user)
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)
        cuponCode = data.get('cuponCode')

        try:
            cupon = Cupon.objects.filter(cupon=cuponCode)
            if cupon.count() > 1:
                try:
                    cupon = cupon.get(usedCoupon__lt=F('quantity'))
                except:
                    responseData = {'valid': False, 'message': 'Cupón agotado'}
                    return JsonResponse(responseData)
            else :
                cupon = Cupon.objects.get(cupon=cuponCode)
        except Cupon.DoesNotExist:
            responseData = {'valid': False, 'message': 'Cupón no válido'}
            return JsonResponse(responseData)

        if cupon.user is not None and cupon.user != request.user:
            responseData = {'valid': False, 'message': 'No puedes redimir este cupón'}
            return JsonResponse(responseData)

        if request.user in cupon.claimedBy.all():
            responseData = {'valid': False, 'message': 'Solo puedes redimir el cupon una vez'}
            return JsonResponse(responseData)

        if cupon.usedCoupon >= cupon.quantity:
            responseData = {'valid': False, 'message': 'Cupón agotado'}
            return JsonResponse(responseData)

        cart.cupon = cupon
        cart.save()
        responseData = {'valid': True, 'cuponDescription': cupon.description, 'discountValue': cupon.value}
        return JsonResponse(responseData)
    return JsonResponse({'error': 'Invalid request method'})

def removeCupon(request):
    cart = Cart.objects.get(user=request.user)
    cart.cupon = None
    cart.save()
    return redirect('store:checkout')