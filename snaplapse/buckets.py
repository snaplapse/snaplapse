import boto3
import logging
import os
from botocore.exceptions import ClientError

def create_bucket(bucket_name, region=None):
    try:
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        logging.error(e)
        return False

def get_bucket(bucket_name):
    try:
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.Bucket(bucket_name)
        if bucket.creation_date:
            return True
        return False
    except ClientError as e:
        logging.error(e)
        return False

def list_buckets():
    try:
        client = boto3.client('s3')
        return client.list_buckets()
    except ClientError as e:
        logging.error(e)
        return None

def list_objects(bucket_name):
    try:
        client = boto3.client('s3')
        return client.list_objects(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return None

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    if not get_bucket(bucket):
        return False
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_objects(bucket_name, objects):
    return

print(get_bucket('snaplapse-1222233'))