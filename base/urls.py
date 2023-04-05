from django.urls import path
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

    path('createBanner', views.createBanner, name="createBanner"),
    path('updateBanner/<str:pk>', views.updateBanner, name="updateBanner"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)