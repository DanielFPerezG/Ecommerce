from django.urls import path
from . import views

from cookie_consent.views import CookieGroupAcceptView, CookieGroupDeclineView

app_name = "store"   


urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('cookiePolicy/', views.cookiePolicy, name="cookiePolicy"),
    path('usePolicy/', views.usePolicy, name="usePolicy"),

    path('userProfile', views.userProfile, name="userProfile"),
    path('personalInformation', views.personalInformation, name="personalInformation"),
    path('updateUserInfo/<str:pk>', views.updateUserInfo, name="updateUserInfo"),
    path('securityInformation', views.securityInformation, name="securityInformation"),
    path('updatePassword/<str:pk>', views.updatePassword, name="updatePassword"),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('deleteUser/<str:pk>', views.deleteUser, name="deleteUser"),
    
    path('viewOrder', views.viewOrder, name="viewOrder"),
    path('viewOrderDetail/<str:pk>', views.viewOrderDetail, name="viewOrderDetail"),

    path('userAddress', views.userAddress, name="userAddress"),
    path('createAddress', views.createAddress, name="createAddress"),
    path('deleteAddress/<str:pk>', views.deleteAddress, name="deleteAddress"),

    path('', views.home, name="home"),
    path('aboutUs', views.aboutUs, name="aboutUs"),
    path('shopDetail/<str:pk>', views.shopDetail, name="shopDetail"),
    path('store', views.store, name="store"),
    path('addCart/<str:pk>', views.addCart, name="addCart"),
    path('addCartDetail/<str:pk>', views.addCartDetail, name="addCartDetail"),
    path('viewCart', views.viewCart, name="viewCart"),
    path('checkout', views.checkout, name="checkout"),
    path('createOrder/<str:pk>', views.createOrder, name="createOrder"),
    path('cancelStoreOrder/<str:pk>', views.cancelStoreOrder, name="cancelStoreOrder"),

    path('validateCupon', views.validateCupon, name="validateCupon"),
    path('removeCupon', views.removeCupon, name="removeCupon"),

    path('updateCart', views.updateCart, name='updateCart'),
    path('deleteCart/<str:pk>', views.deleteCart, name='deleteCart'),
]