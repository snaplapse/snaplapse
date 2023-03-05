from rest_framework import generics

from ..models import Like
from ..serializers import LikeSerializer


class LikeList(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_queryset(self):
        user = self.request.query_params.get('user')
        photo = self.request.query_params.get('photo')
        likes = Like.objects.all()
        if user is not None:
            likes = likes.filter(user=user)
        if photo is not None:
            likes = likes.filter(photo=photo)
        return likes


class LikeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
