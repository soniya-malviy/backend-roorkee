import boto3
import io
from pdfminer.high_level import extract_text
import json
from django.conf import settings

# AWS S3 Configuration
s3 = boto3.client('s3', 
                  aws_access_key_id= settings.AWS_ACCESS_KEY_ID, 
                  aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY, 
                  region_name= settings.AWS_S3_REGION_NAME)

BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME

def list_pdfs_in_directory(state_name):
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"pdfs/{state_name}/")
        
        pdf_files = []
        
        if 'Contents' in response:
            for obj in response['Contents']:
                metadata_response = s3.head_object(Bucket=BUCKET_NAME, Key=obj['Key'])
                
                metadata = metadata_response.get('Metadata', {})
                pdf_key = obj['Key']
                pdf_url = f'https://{BUCKET_NAME}.s3.amazonaws.com/{pdf_key}'

                pdf_files.append({
                    'pdf_key': obj['Key'],   # S3 key (path)
                    'pdfUrl': pdf_url,
                    'last_modified': obj['LastModified'],  # Last modified date
                    'size': obj['Size'],  # File size
                    'metadata': metadata  # Metadata dictionary
                })
        
        return pdf_files
    
    except Exception as e:
        # print(f"Error listing PDFs from S3: {e}")
        return []

def download_pdf_from_s3(pdf_key):
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=pdf_key)
        pdf_data = response['Body'].read()
        return pdf_data
    except Exception as e:
        # print(f"Error downloading PDF from S3: {e}")
        return None
    

def process_pdfs_for_state(state_name):
    # List all PDFs in the specified state folder
    pdf_files = list_pdfs_in_directory(state_name)
    
    if not pdf_files:
        # print(f"No PDFs found for {state_name} in S3.")
        return
    
    # Process each PDF file
    lst = []
    for pdf_data in pdf_files:
        pdf_file = pdf_data["pdf_key"]
        pdfUrl = pdf_data["pdfUrl"]
        title = pdf_data["metadata"]["title"]
        jsonData = {
            'title': title,
            'pdfUrl': pdfUrl,
            'pdfFile': pdf_file
        }
    return lst
        

# process_pdfs_for_state('goa')

