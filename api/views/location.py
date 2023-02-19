from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Location
from ..serializers import LocationSerializer
from django.db import connection

class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

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
