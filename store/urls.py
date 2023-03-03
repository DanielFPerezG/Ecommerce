from django.urls import path
from . import views

app_name = "store"   


urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('shopDetail/<str:pk>', views.shopDetail, name="shopDetail"),
    path('store', views.store, name="store"),
    
    
]