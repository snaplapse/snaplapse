from rest_framework import generics
from rest_framework import mixins

from ..models import Flag, Photo
from ..serializers import FlagSerializer

class FlagList(generics.ListCreateAPIView, mixins.UpdateModelMixin):
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
            serializer = self.get_serializer(photo, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        return self.create(request, *args, **kwargs)


class FlagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer