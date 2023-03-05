from rest_framework import generics

from ..models import Flag
from ..serializers import FlagSerializer


class FlagList(generics.ListCreateAPIView):
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer

    def get_queryset(self):
        user = self.request.query_params.get('user')
        photo = self.request.query_params.get('photo')
        flags = Flag.objects.all()
        if user is not None:
            flags = flags.filter(user=user)
        if photo is not None:
            flags = flags.filter(photo=photo)
        return flags


class FlagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer
