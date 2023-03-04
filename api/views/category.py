from rest_framework import generics

from django.shortcuts import get_object_or_404

from ..models import Category
from ..serializers import CategorySerializer

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

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailByName(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_fields = ['name']
