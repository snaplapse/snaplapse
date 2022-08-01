from django.contrib import admin

from .models import Category, Like, Location, Photo, Tag, User


admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Location)
admin.site.register(Photo)
admin.site.register(Tag)
admin.site.register(User)
