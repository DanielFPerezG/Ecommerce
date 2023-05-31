from django.urls import path
from . import views

app_name = "store"   


urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('userProfile', views.userProfile, name="userProfile"),

    path('', views.home, name="home"),
    path('shopDetail/<str:pk>', views.shopDetail, name="shopDetail"),
    path('store', views.store, name="store"),
    path('addCart/<str:pk>', views.addCart, name="addCart"),
    path('addCartDetail/<str:pk>', views.addCartDetail, name="addCartDetail"),
    path('viewCart', views.viewCart, name="viewCart"),

    path('updateCart', views.updateCart, name='updateCart'),
    path('deleteCart/<str:pk>', views.deleteCart, name='deleteCart'),
]