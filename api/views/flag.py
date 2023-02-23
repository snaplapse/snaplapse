from rest_framework import generics

from ..models import Flag
from ..serializers import FlagSerializer


class FlagList(generics.ListCreateAPIView):
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer


class FlagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer
