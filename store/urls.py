from django.urls import path
from . import views

app_name = "store"   


urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('userProfile', views.userProfile, name="userProfile"),
    path('personalInformation', views.personalInformation, name="personalInformation"),
    path('updateUserInfo/<str:pk>', views.updateUserInfo, name="updateUserInfo"),
    path('securityInformation', views.securityInformation, name="securityInformation"),
    path('updatePassword/<str:pk>', views.updatePassword, name="updatePassword"),

    path('userAddress', views.userAddress, name="userAddress"),
    path('createAddress', views.createAddress, name="createAddress"),
    path('deleteAddress/<str:pk>', views.deleteAddress, name="deleteAddress"),

    path('', views.home, name="home"),
    path('shopDetail/<str:pk>', views.shopDetail, name="shopDetail"),
    path('store', views.store, name="store"),
    path('addCart/<str:pk>', views.addCart, name="addCart"),
    path('addCartDetail/<str:pk>', views.addCartDetail, name="addCartDetail"),
    path('viewCart', views.viewCart, name="viewCart"),
    path('checkout', views.checkout, name="checkout"),

    path('updateCart', views.updateCart, name='updateCart'),
    path('deleteCart/<str:pk>', views.deleteCart, name='deleteCart'),
]