# TODO: upload file or give remote url (how to open and upload to blob), work on prompt to make it output json, test and deploy API?

# This program Takes a pdf files, uploades it to blob storage, runs an already existing indexer on it and uses this index to ask GPT-4o model to extract the information out of it
#C:\Users\shreya.aj.sharma\Downloads\ScannedLease3.pdf

import time
import os 
import AzureOpenAI 
import AzureBlob
import AzureSearch
from flask import Flask, flash, request, redirect, url_for
from dotenv import load_dotenv, dotenv_values

load_dotenv()

ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/leasepdfextractor/', methods = ['POST','GET'])

# if file is uploaded
def upload_file(filepath, file_stream):
           
    # connecring to Asure Blob Storage

    container_name = "shreyacontainer"
    container_client = AzureBlob.connect(os.getenv("AZURE_STORAGE_CONNECTION_STRING"), container_name)
    print(file_stream)

    # uploading the pdf to Azure Blob Storage
    AzureBlob.upload(filepath,file_stream, container_client, os.getenv("AZURE_STORAGE_CONNECTION_STRING"),container_name)

    # connecting to Azure search service and indexer

    index_name = "azureblob-index"
    indexers_client, search_client = AzureSearch.connect(os.getenv("AZURE_SEARCH_ENDPOINT"),os.getenv("AZURE_SEARCH_KEY"), index_name)
    AzureSearch.delete(search_client,os.getenv("METADATA_STORAGE_PATH"))

    indexer_name = "shreya-indexer"
    AzureSearch.run(indexers_client,indexer_name)

    time.sleep(30)

    # connecting to AzureOpenAI
    client = AzureOpenAI.connect(os.getenv("AZURE_OPENAI_ENDPOINT"), os.getenv("AZURE_OPENAI_API_KEY"), "2024-03-01-preview" ) 

    # using Prompt to ask GPT-4o model to extract relevent information out of the pdf
    prompt = "The information is available in the lease. Could you please list all the filled in infromation in the lease? for example, Date of the agreement, Lessor, Lessee, where the property is located at, Lessor Address, Lessee Address, Rent per year or per month, Security Deposit, Lease Start date, lease end date. Please output in Json format. for example, for lessor use the following structure: {\"lessor\":[{\"name\":\"\",\"lessor_address\":\"\"}]}.Do not provide code or explanation and structure it in proper JSON. Remove '''json from the beginning of the response if it is there."     # prompt = "who is the landlord?"
    model = "gpt-4o-PDF-Extractions"

    result = AzureOpenAI.askGPT(client,prompt,model,search_client)
    
    return result
   
if __name__ == "__main__":
    app.secret_key = 'shreyapdfextractor'
    app.run(debug=True)




