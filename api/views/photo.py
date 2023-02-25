import io
import base64
from django.http import FileResponse
from rest_framework import generics

from ..models import Photo
from ..serializers import PhotoSerializer


class PhotoList(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


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
