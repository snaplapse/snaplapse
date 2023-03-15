import io
import base64
from django.http import FileResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from ..models import Photo
from ..serializers import PhotoSerializer, PhotoMetaSerializer


class PhotoList(generics.ListCreateAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        user = self.request.query_params.get('user')
        location = self.request.query_params.get('location')
        sort_by = self.request.query_params.get('sort_by')
        count = self.request.query_params.get('count')
        visible = self.request.query_params.get('visible')
        photos = Photo.objects.all()
        if visible is not None and visible in ('true', 'false'):
            if visible == 'true':
                photos = photos.filter(visible=True)
            else:
                photos = photos.filter(visible=False)
        if user is not None:
            photos = photos.filter(user=user)
        if location is not None:
            photos = photos.filter(location=location)
        if sort_by is not None:
            photos = photos.order_by(sort_by)
        if count is not None:
            photos = photos[:int(count)]
        return photos

class PhotoMetaList(generics.ListCreateAPIView):
    serializer_class = PhotoMetaSerializer

    def get_queryset(self):
        user = self.request.query_params.get('user')
        location = self.request.query_params.get('location')
        sort_by = self.request.query_params.get('sort_by')
        count = self.request.query_params.get('count')
        visible = self.request.query_params.get('visible')
        photos = Photo.objects.all()
        if visible is not None and visible in ('true', 'false'):
            if visible == 'true':
                photos = photos.filter(visible=True)
            else:
                photos = photos.filter(visible=False)
        if user is not None:
            photos = photos.filter(user=user)
        if location is not None:
            photos = photos.filter(location=location)
        if sort_by is not None:
            photos = photos.order_by(sort_by)
        if count is not None:
            photos = photos[:int(count)]
        return photos

class PhotoCount(generics.GenericAPIView):
    serializer_class = PhotoSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.query_params.get('user')
        location = self.request.query_params.get('location')
        sort_by = self.request.query_params.get('sort_by')
        count = self.request.query_params.get('count')
        visible = self.request.query_params.get('visible')
        photos = Photo.objects.all()
        if visible is not None and visible in ('true', 'false'):
            if visible == "true":
                photos = photos.filter(visible=True)
            else:
                photos = photos.filter(visible=False)
        if user is not None:
            photos = photos.filter(user=user)
        if location is not None:
            photos = photos.filter(location=location)
        if sort_by is not None:
            photos = photos.order_by(sort_by)
        if count is not None:
            photos = photos[:int(count)]
        return Response({'count': photos.count()}, status=status.HTTP_200_OK)

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
