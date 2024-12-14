import boto3
from django.conf import settings

s3 = boto3.client('s3', 
                  aws_access_key_id= settings.AWS_ACCESS_KEY_ID, 
                  aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY, 
                  region_name= settings.AWS_S3_REGION_NAME)

BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME 
PREFIX = 'pdfs/goa'

def delete_pdfs_from_directory():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
        
        if 'Contents' not in response:
            # print(f"No PDFs found in {PREFIX}")
            return
        
        delete_objects = {
            'Objects': [{'Key': obj['Key']} for obj in response['Contents']]
        }
        
        s3.delete_objects(Bucket=BUCKET_NAME, Delete=delete_objects)
        # print(f"All PDFs in {PREFIX} deleted.")
    
    except Exception as e:
        print(f"Error deleting PDFs: {e}")

delete_pdfs_from_directory()