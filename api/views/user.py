import json

# from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.core import serializers
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import User
from ..serializers import UserSerializer


class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        object_filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: # Ignore empty fields.
                object_filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **object_filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailByName(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_fields = ['username']

@api_view(['POST'])
def login(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    name, sec = body['username'], body['secret']

    try:
        user = User.objects.get(username=name)

        if check_password(sec, user.secret):
            return Response({'success': True, 'message': "User authenticated", 'data': serializers.serialize('json', [user])}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': "Authentication credentials invalid", 'data': None}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'success': False, 'message': "Authentication credentials invalid", 'data': None}, status=status.HTTP_400_BAD_REQUEST)
