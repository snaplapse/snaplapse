from rest_framework import generics
from rest_framework.exceptions import ValidationError

from ..models import Location
from ..serializers import LocationSerializer
import math

class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class NearbyLocations(generics.ListAPIView):
    serializer_class = LocationSerializer
    
    def get_queryset(self):
        params = self.request.query_params
        
        try:
            latitude = float(params.get('coordinates').split(',')[0])
            longitude = float(params.get('coordinates').split(',')[1])
            radius = float(params.get('radius'))

            lat1 = latitude - (radius / 6378000) * (180 / math.pi)
            lat2 = latitude + (radius / 6378000) * (180 / math.pi)
            lng1 = longitude - (radius / 6378000) * (180 / math.pi) / math.cos(latitude * math.pi/180)
            lng2 = longitude + (radius / 6378000) * (180 / math.pi) / math.cos(latitude * math.pi/180)
            queryset = Location.objects.filter(
                latitude__gte = lat1, 
                latitude__lte = lat2,
                longitude__gte = lng1,
                longitude__lte = lng2
            ).order_by('id')

            return queryset
        except:
            raise ValidationError("Invalid request.")
