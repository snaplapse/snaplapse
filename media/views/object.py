import json
import logging

import boto3
from botocore.exceptions import ClientError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def list_objects(_, bucket_name):
    try:
        client = boto3.client('s3')
        response = client.list_objects(Bucket=bucket_name)
        objects = response['Contents']
        return Response(
            {'success': True, 'message': f'{objects}'},
            status=status.HTTP_200_OK
        )
    except ClientError as error:
        logging.error(error)
        return Response(
            {'success': False, 'message': "Bad request"},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def upload_file(request, bucket_name):
    object_name = request.FILES['image']
    file_name = request.POST.get('file_name')
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_fileobj(object_name, bucket_name, file_name)
        return Response(
            {'success': True, 'message': 'File uploaded successfully'},
            status=status.HTTP_200_OK
        )
    except ClientError as error:
        logging.error(error)
        return Response(
            {'success': False, 'message': "Bad request"},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PUT'])
def delete_objects(request, bucket_name):
    delete_objects_list = []
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    object_keys = body['object_keys']
    for i in object_keys:
        delete_objects_list.append({'Key': i})
    try:
        client = boto3.client('s3')
        response = client.delete_objects(
            Bucket=bucket_name,
            Delete={
                'Objects': delete_objects_list
            }
        )
        deleted = response['Deleted']
        return Response(
            {'success': True, 'message': f'{deleted}'},
            status=status.HTTP_200_OK
        )
    except ClientError as error:
        logging.error(error)
        return Response(
            {'success': False, 'message': "Bad request"},
            status=status.HTTP_400_BAD_REQUEST
        )
