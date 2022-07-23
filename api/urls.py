from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    re_path('^users/(?P<username>.+)/$', views.UserDetailByName.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
