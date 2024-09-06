from django.contrib import admin
from django.urls import path, include
from APP import views

urlpatterns = [
    path('', views.index, name='index'),  
    path('api/v1/', include('APP.urls')),  
    path('admin/', admin.site.urls), 
    path('api-auth/', include('rest_framework.urls')),  
]