import os
from mimetypes import MimeTypes

import boto3
from boto3.s3.transfer import S3Transfer

AWS_REGION = os.environ.get('AWS_REGION')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
S3_BASE_URL = os.environ.get('S3_BASE_URL')
BASE_URL = 'http://static.overcart.com/'


def get_mime_type(filename):
    mime = MimeTypes()
    mime_type = mime.guess_type(filename)
    return mime_type[0]


def upload_to_s3_bucket(bucket_name, source_file_path, destination_file_path):
    print('s3 called')
    transfer = S3Transfer(
        boto3.client('s3', AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY,
                     aws_secret_access_key=AWS_SECRET_KEY))
    transfer.upload_file(source_file_path, bucket_name, destination_file_path,
                         extra_args={
                             'ContentType': str(
                                 get_mime_type(source_file_path))})
    return BASE_URL + destination_file_path
