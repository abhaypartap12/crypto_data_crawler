import boto3
from google.cloud import storage

class Uploader:
    def upload_to_s3(self, file_path):
        s3_client = boto3.client('s3')
        bucket_name = 'crypto_data'
        s3_key = 'xxxx'

        try:
            s3_client.upload_file(file_path, bucket_name, s3_key)
            print(f'Successfully uploaded {file_path} to {bucket_name}/{s3_key}')
        except Exception as e:
            print(f'Error uploading {file_path} to {bucket_name}/{s3_key}: {str(e)}')

    def upload_to_gcs(self, file_path):
        storage_client = storage.Client()

        try:
            file_name = file_path
            bucket_name = "crypto_data"
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(file_name)

            blob.upload_from_filename(file_name)
            print(f'Successfully uploaded {file_path} to {bucket_name}')
        except Exception as e:
            print(f'Error uploading {file_path} to {bucket_name}: {str(e)}')

