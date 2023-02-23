from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    re_path('^users/(?P<username>.+)/$', views.UserDetailByName.as_view()),
    path('login/', views.login),
    path('photos/', views.PhotoList.as_view()),
    path('photos/<int:pk>/', views.PhotoDetail.as_view()),
    path('locations/', views.LocationList.as_view()),
    path('locations/<int:pk>/', views.LocationDetail.as_view()),
    path('locations/nearby', views.NearbyLocations.as_view()),
    path('locations/<int:pk>/categories/', views.LocationCategories.as_view()),
    path('locations/likes/<int:user_id>/', views.locations_like_counts_by_user),
    path('locations/likes/', views.locations_like_counts_all_users),
    path('flags/', views.FlagList.as_view()),
    path('flags/<int:pk>/', views.FlagDetail.as_view()),
    path('likes/', views.LikeList.as_view()),
    path('likes/<int:pk>/', views.LikeDetail.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('categories/<int:pk>/', views.CategoryDetail.as_view()),
    path('tags/', views.TagList.as_view()),
    path('tags/<int:pk>/', views.TagDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
