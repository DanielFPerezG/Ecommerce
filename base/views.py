from django.shortcuts import render

# Create your views here.

def loginPage(request):
    page = 'login'
    # if request.user.is_authenticated:
    #     return redirect('home')

    # if request.method == 'POST':
    #     email = request.POST.get('email').lower()
    #     password = request.POST.get('password')

    #     try:
    #         user = User.objects.get(email = email)
    #     except:
    #         messages.error(request, 'User does not exist')
        
    #     user = authenticate(request, email = email, password=password)

    #     if user is not None:
    #         login(request, user)
    #         return redirect('home')
    #     else:
    #         messages.error(request, 'Username or password is incorrect')

    context= {'page': page}
    return render(request, 'base/login_register.html', context)

def home(request):
    return render(request, 'base/home.html')