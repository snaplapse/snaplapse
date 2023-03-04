import io
import base64
from django.http import FileResponse
from rest_framework import generics

from ..models import Photo
from ..serializers import PhotoSerializer


class PhotoList(generics.ListCreateAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        user = self.request.query_params.get('user')
        location = self.request.query_params.get('location')
        photos = Photo.objects.all()
        if user is not None:
            photos = photos.filter(user=user)
        if location is not None:
            photos = photos.filter(location=location)
        return photos

class PhotoPrefixList(generics.ListCreateAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        photos = Photo.objects.all()
        for photo in photos:
            photo.bitmap = "data:image/jpeg;base64," + photo.bitmap

        user = self.request.query_params.get('user')
        if user is None:
            return photos
        return photos.filter(user=user)

class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

# test endpoint :3
class PhotoDownload(generics.GenericAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        bitmap = instance.bitmap
        decoded = base64.b64decode(bitmap)
        binary_io = io.BytesIO(decoded)
        response = FileResponse(binary_io)
        response['Content-Type'] = 'application/x-binary'
        response['Content-Disposition'] = 'attachment; filename="TEST_IMAGE.png"'
        return response
