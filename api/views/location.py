from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Location
from ..serializers import LocationSerializer
from django.db import connection
from recommendations import recommender
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
            count = 20 # default 20 results
            if params.get('count'):
                count = float(params.get('count'))

            lat1 = latitude - (radius / 6378000) * (180 / math.pi)
            lat2 = latitude + (radius / 6378000) * (180 / math.pi)
            lng1 = longitude - (radius / 6378000) * (180 / math.pi) / math.cos(latitude * math.pi/180)
            lng2 = longitude + (radius / 6378000) * (180 / math.pi) / math.cos(latitude * math.pi/180)
            queryset = Location.objects.filter(
                latitude__gte = lat1, 
                latitude__lte = lat2,
                longitude__gte = lng1,
                longitude__lte = lng2
            ).order_by('id')[0:count]   # grabs the top 'count' results by id, maybe order by proximity in the future!

            return queryset
        except:
            raise ValidationError("Invalid request.")
        
class Recommendations(generics.ListAPIView):
    serializer_class = LocationSerializer
    
    def get_queryset(self):
        params = self.request.query_params

        try:
            user_id = int(params.get('userId'))
            latitude = float(params.get('coordinates').split(',')[0])
            longitude = float(params.get('coordinates').split(',')[1])
            radius = float(params.get('radius'))

            queryset = recommender.make_recommendations(user_id, latitude, longitude, radius)
            return queryset
        except:
            raise ValidationError("Invalid request.")

def processQueryToDictList(query):
    cursor = connection.cursor()
    cursor.execute(query)
    
    columns = [col[0] for col in cursor.description]
    results = [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    return results

@api_view(['GET'])
def locationsLikeCountsByUser(request, userId):
    query = '''SELECT photo_likes.user_id, api_location.id AS location_id, COUNT(like_id) AS likes 
            FROM api_location RIGHT OUTER JOIN (
                SELECT api_like.user_id AS user_id, api_photo.location_id AS location_id, api_like.id AS like_id 
                FROM api_photo INNER JOIN api_like ON api_photo.id = api_like.photo_id WHERE api_like.user_id={}
            ) AS photo_likes 
            ON api_location.id = photo_likes.location_id 
            GROUP BY photo_likes.user_id, api_location.id 
            ORDER BY api_location.id'''.format(userId)
    locations_likes = processQueryToDictList(query)

    return Response({'results': locations_likes}, status=status.HTTP_200_OK)

@api_view(['GET'])
def locationsLikeCountsAllUsers(request):
    query = '''SELECT photo_likes.user_id, api_location.id AS location_id, COUNT(like_id) AS likes 
            FROM api_location RIGHT OUTER JOIN (
                SELECT api_like.user_id AS user_id, api_photo.location_id AS location_id, api_like.id AS like_id 
                FROM api_photo INNER JOIN api_like ON api_photo.id = api_like.photo_id 
            ) AS photo_likes 
            ON api_location.id = photo_likes.location_id 
            GROUP BY photo_likes.user_id, api_location.id 
            ORDER BY api_location.id'''
    locations_likes = processQueryToDictList(query)

    return Response({'results': locations_likes}, status=status.HTTP_200_OK)
