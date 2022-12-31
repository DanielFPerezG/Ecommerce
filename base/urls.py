from django.urls import path
from django.contrib import admin

from . import views

app_name = "base"   


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('home', views.home, name="home"),
    path('createProduct', views.createProduct, name="createProduct")

]