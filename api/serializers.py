from rest_framework import serializers

from django.contrib.auth.hashers import make_password

from .models import Category, Like, Location, Photo, Tag, User


class CategorySerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'tags', 'created']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'photo', 'created']


class LocationSerializer(serializers.ModelSerializer):
    photos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Location
        fields = ['id', 'name', 'longitude', 'latitude', 'photos', 'tags', 'created']


class PhotoSerializer(serializers.ModelSerializer):
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Photo
        fields = ['id', 'user', 'location', 'description', 'likes', 'visible']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'location', 'category']


class UserSerializer(serializers.ModelSerializer):
    photos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    secret = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'photos', 'likes', 'secret', 'created']

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            secret = make_password(validated_data['secret'])
        )
        user.save()
        return user
