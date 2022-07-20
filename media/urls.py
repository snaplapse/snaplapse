from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('create_bucket/', views.create_bucket),
    path('get_bucket/<str:bucket_name>', views.get_bucket),
    path('list_buckets/', views.list_buckets),
    path('list_objects/<str:bucket_name>', views.list_objects),
    path('upload_file/<str:bucket_name>', views.upload_file),
    path('delete_objects/<str:bucket_name>', views.delete_objects)
]

urlpatterns = format_suffix_patterns(urlpatterns)