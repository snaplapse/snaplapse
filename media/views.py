import json
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import boto3
import logging
from botocore.exceptions import ClientError

# Create your views here.
@api_view(['POST'])
def create_bucket(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    bucket_name = body['bucket_name']
    try:
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket=bucket_name)
        return Response({'success': True, 'message': "Bucket has been created"}, status=status.HTTP_200_OK)
    except ClientError as e:
        logging.error(e)
        return Response({'success': False, 'message': "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_bucket(request, bucket_name):
    try:
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.Bucket(bucket_name)
        if bucket.creation_date:
            return Response({'success': True, 'message': f'{bucket.name}'}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': "Bucket not found"}, status=status.HTTP_404_NOT_FOUND)
        
    except ClientError as e:
        logging.error(e)
        return Response({'success': False, 'message': "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_buckets(request):
    try:
        client = boto3.client('s3')
        response = client.list_buckets()
        buckets = response['Buckets']
        return Response({'success': True, 'message': f'{buckets}'}, status=status.HTTP_200_OK)
    except ClientError as e:
        logging.error(e)
        return Response({'success': False, 'message': "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_objects(request, bucket_name):
    try:
        client = boto3.client('s3')
        response = client.list_objects(Bucket=bucket_name)
        objects = response['Contents']
        return Response({'success': True, 'message': f'{objects}'}, status=status.HTTP_200_OK)
    except ClientError as e:
        logging.error(e)
        return Response({'success': False, 'message': "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def upload_file(request, bucket_name):
    object_name = request.FILES['image']
    file_name = request.POST.get('file_name')

    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_fileobj(object_name, bucket_name, file_name)
        return Response({'success': True, 'message': 'File uploaded successfully'}, status=status.HTTP_200_OK)
    except ClientError as e:
        logging.error(e)
        return Response({'success': False, 'message': "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def delete_objects(request, bucket_name):
    delete_objects = []
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    object_keys = body['object_keys']
    for i in object_keys:
        delete_objects.append({'Key': i})
    try:
        client = boto3.client('s3')
        response = client.delete_objects(
            Bucket=bucket_name,
            Delete={
                'Objects': delete_objects
            }
        )
        deleted = response['Deleted']
        return Response({'success': True, 'message': f'{deleted}'}, status=status.HTTP_200_OK)
    except ClientError as e:
        logging.error(e)
        return Response({'success': False, 'message': "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
