import logging
import os
import sys
import threading
from typing import Optional

from django.conf import settings

import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError

# Constant variables
KB = 1024
MB = KB * KB
GB = MB * KB

class ProgressPercentage:
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._size = float(os.path.getsize(file_path))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        """
        To simplify, assume this is hooked up to a single file_path

        :param bytes_amount: uploaded bytes
        """
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (self._file_path, self._seen_so_far, self._size, percentage)
            )
            sys.stdout.flush()
            
class Bucket:
    """CDN Bucket manager
    init method creates connection.
    """

    def __init__(self):
        s3_resource = boto3.resource(
            settings.AWS_SERVICE_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.bucket = s3_resource.Bucket(settings.AWS_STORAGE_BUCKET_NAME)


    def get_objects(self):
        return self.bucket.objects.all()

    def delete_object(self,object_name):
        object = self.bucket.Object(object_name)
        object.delete()
        return True
    
    def download_object(self,object_name):
        download_path =  settings.AWS_LOCAL_STORAGE +  object_name
        self.bucket.download_file(
            object_name,
            download_path
        )
        return True
    
    def upload_file(self,file_path: str, object_name: Optional[str] = None):
        file_path = 'the/abs/path/to/file.txt'
        object_name = 'file.txt'

        with open(file_path, "rb") as file:
            self.bucket.put_object(
                ACL='private',
                Body=file,
                Key=object_name
            )

    
    def upload_multipart_file(self,file_path: str, bucket: str, object_name: Optional[str] = None):
        """
        Upload a file to an S3 bucket

        :param file_path: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_path is used
        :return: True if file was uploaded, else False
        """
        # If S3 object_name was not specified, use file_path
        if object_name is None:
            object_name = file_path

        # Upload the file
        try:
            s3_client = boto3.client(
                settings.AWS_SERVICE_NAME,
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            # Set the desired multipart threshold value (400 MB)
            config = TransferConfig(multipart_threshold=400 * MB, max_concurrency=5)
            s3_client.upload_file(
                file_path,
                bucket,
                object_name,
                ExtraArgs={'ACL': 'public-read'},
                Callback=ProgressPercentage(file_path),
                Config=config
            )
        except ClientError as e:
            logging.error(e)
            return False

        return True

bucket = Bucket()