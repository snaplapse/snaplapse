"""snaplapse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from media import views


urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('media/create_bucket/', views.create_bucket),
    path('media/get_bucket/<str:bucket_name>', views.get_bucket),
    path('media/list_buckets/', views.list_buckets),
    path('media/list_objects/<str:bucket_name>', views.list_objects),
    path('media/upload_file/<str:bucket_name>', views.upload_file),
    path('media/delete_objects/<str:bucket_name>', views.delete_objects),
]
