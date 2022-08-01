from rest_framework import generics

from ..models import Tag
from ..serializers import TagSerializer


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queyrset = Tag.objects.all()
    serializer_class = TagSerializer
