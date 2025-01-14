import requests
import boto3
from urllib.parse import urlparse
from os.path import basename
import os
import json
import urllib.parse
from django.conf import settings


s3 = boto3.client('s3', 
                  aws_access_key_id= settings.AWS_ACCESS_KEY_ID, 
                  aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY, 
                  region_name= settings.AWS_S3_REGION_NAME)

BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME


def encode_metadata_value(value):
    encoded_value = urllib.parse.quote(value)
    return encoded_value

def get_file_name_with_query(url):
    parsed_url = urlparse(url)
    path = parsed_url.path.strip('/')  
    query = parsed_url.query         
    if query:
        return f"{path}?{query}"  
    return path  

# Function to download PDF from URL and upload to S3
def download_and_upload_pdf(pdf_url, state_name, scheme_url, title, scheme_id):
    try:
        # Download PDF
        response = requests.get(pdf_url, stream=True)
        response.raise_for_status()  # Ensure the request was successful

        # Get the file name from the URL
        file_name = get_file_name_with_query(pdf_url)
        s3_directory = f"pdfs/{state_name}/"
        encoded_title = encode_metadata_value(title)
        metadata = {
            'schemeUrl': scheme_url,
            'title': encoded_title,
            'pdfUrl': pdf_url,
            'id': scheme_id
        }
        # Upload to S3
        s3.upload_fileobj(response.raw, BUCKET_NAME, f"{s3_directory}{file_name}", ExtraArgs={'ContentType': 'application/pdf', 'Metadata': metadata})
        print(f"Successfully uploaded {file_name} to S3.")
    
    except Exception as e:
        print(f"Error downloading or uploading PDF: {e}")



def main(input_file_path):
    with open(input_file_path, "r") as file:
        stateData = json.load(file)
    for pdf_url in stateData:
        download_and_upload_pdf(pdf_url["pdf_link"],'goa', pdf_url["schemeUrl"], pdf_url["title"], pdf_url["id"])

pdfStates = [
    "goa",
    "jharkhand",
    "tripura",
    "rajasthan"
]

for state_name in pdfStates:
    base_file_path = os.path.join(os.path.dirname(__file__),'..', 'scrapedData', 'scrapedPdfs', f'{state_name}Pdf.json')
    input_file_path = os.path.abspath(base_file_path)
    main(input_file_path)