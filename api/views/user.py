from django.shortcuts import get_object_or_404
from rest_framework import generics

from ..models import User
from ..serializers import UserSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailByName(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_fields = ['username']

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        get_object_filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:
                get_object_filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **get_object_filter)
        self.check_object_permissions(self.request, obj)
        return obj
