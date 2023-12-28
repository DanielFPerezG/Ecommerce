from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "base"   


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('home', views.home, name="home"),

    path('createProduct', views.createProduct, name="createProduct"),
    path('adminProduct', views.adminProduct, name="adminProduct"),
    path('deleteProduct/<str:pk>', views.deleteProduct, name="deleteProduct"),
    path('updateProduct/<str:pk>', views.updateProduct, name="updateProduct"),

    path('adminTopic', views.adminTopic, name="adminTopic"),
    path('updateTopic/<str:pk>', views.updateTopic, name="updateTopic"),
    path('deleteTopic/<str:pk>', views.deleteTopic, name="deleteTopic"),

    path('createBanner', views.createBanner, name="createBanner"),
    path('adminBanner', views.adminBanner, name="adminBanner"),
    path('updateBanner/<str:pk>', views.updateBanner, name="updateBanner"),
    path('deleteBanner/<str:pk>', views.deleteBanner, name="deleteBanner"),

    path('adminOrder', views.adminOrder, name="adminOrder"),
    path('viewOrderDetail/<str:pk>', views.viewOrderDetail, name="viewOrderDetail"),
    path('cancelOrder/<str:pk>', views.cancelOrder, name="cancelOrder"),
    path('updateOrder/<str:pk>', views.updateOrder, name="updateOrder"),

    path('createCupon', views.createCupon, name="createCupon"),
    path('adminCupon', views.adminCupon, name="adminCupon"),
    path('updateCupon/<str:pk>', views.updateCupon, name="updateCupon"),

    path('createEmail', views.createEmail, name="createEmail"),
    path('adminEmail', views.adminEmail, name="adminEmail"),
    path('sendEmail/<str:pk>', views.sendEmail, name="sendEmail"),

    path('updateShippingCost', views.updateShippingCost, name="updateShippingCost"),

    path('dashBoardLastOrder', views.dashBoardLastOrder, name="dashBoardLastOrder"),


    path('store/', include('store.urls', namespace='store')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)