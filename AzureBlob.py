from queue import Empty
from typing import Container
from azure.storage.blob import BlobServiceClient
from urllib.parse import urlparse



# Your code using BlobServiceClient...


# connect to Azure Blob storage and to specific container

def connect(connection_string, container_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container=container_name)
    return container_client

# uploading the pdf to Azure Blob Storage

def upload(file_path,file_stream, container_client, connection_string,container_name):
    if not file_path:
         #uploaded file
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container = container_name, blob="ScannedLease.pdf")
        blob_client.upload_blob(file_stream, blob_type="BlockBlob", overwrite=True)
         
    else:
        url_parsed = urlparse(file_path)
        # if url is local
        if url_parsed.scheme in ('file', ''):
            with open( file_path, "rb") as data:
                    return container_client.upload_blob(name="ScannedLease.pdf", data=data , overwrite=True)
        #if url is remote 
        else:
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            blob = blob_service_client.get_blob_client(container=container_name, blob="ScannedLease.pdf")
            return blob.upload_blob_from_url(file_path, overwrite=True)
     
   
        

