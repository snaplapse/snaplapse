from rest_framework import generics
from rest_framework.response import Response

from ..models import Flag, Photo
from ..serializers import FlagSerializer

class FlagList(generics.ListCreateAPIView):
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer

    def post(self, request, *args, **kwargs):
        photo_id = request.data.get("photo")
        # count photo_flags to get num flags for the photo
        photo_flags = len(Flag.objects.filter(photo=photo_id))
        # set photo visible to false if num flags >= 2
        if photo_flags >= 2:
            photo = Photo.objects.filter(id=photo_id)[0]
            photo.visible = False
            photo.save()
        return self.create(request, *args, **kwargs)


class FlagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer

    def delete(self, request, *args, **kwargs):
        flag = self.get_object()
        # count photo_flags to get num flags for the photo
        photo_flags = len(Flag.objects.filter(photo=flag.photo.id))
        # set photo visible to true if num flags <= 3
        if photo_flags <= 3:
            photo = Photo.objects.filter(id=flag.photo.id)[0]
            photo.visible = True
            photo.save()
        # Remove flag
        flag.delete()

        return Response()