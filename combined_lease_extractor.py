"""
This code is a lease info extractor. It extracts the key fields from lease documents

To learn more, please visit the documentation - Quickstart: Document Intelligence (formerly Form Recognizer) SDKs
https://learn.microsoft.com/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?pivots=programming-language-python

"""

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import json
from dotenv import load_dotenv
import os


load_dotenv(dotenv_path='info.env')

ENDPOINT = os.getenv("ENDPOINT")
API_KEY = os.getenv("API_KEY")

model_id = "CombinedLeaseExtractor"

document_analysis_client = DocumentAnalysisClient(
    endpoint=ENDPOINT, credential=AzureKeyCredential(API_KEY)
)

# Make sure your document's type is included in the list of document types the custom model can analyze

def get_results(file):
        poller = document_analysis_client.begin_analyze_document(model_id, file)
        result = poller.result()

        for idx, document in enumerate(result.documents):
            print("--------Analyzing document #{}--------".format(idx + 1))
            print("Document has type {}".format(document.doc_type))
            print("Document has confidence {}".format(document.confidence))
            print("Document was analyzed by model with ID {}".format(result.model_id))
            
            # Initialize a dictionary for this document's fields
            document_fields = {}
            
            # Serialize the data into a dict
            for name, field in document.fields.items():
                document_fields[name] = serialize_field_data(field)

        return document_fields

def serialize_field_data(field):
    field_value = field.value if field.value else field.content
    field_data = {
        "type": field.value_type,
        "value": field_value,
        "confidence": field.confidence,
    }
    if hasattr(field, "bounding_regions"):
        field_data["bounding_box"] = [serialize_bounding_box(region) for region in field.bounding_regions]
    return field_data


def serialize_bounding_box(bounding_box):
    # Convert BoundingRegion to a dictionary with x and y coordinates
    return {
        "page_number": bounding_box.page_number,
        "polygon": [
            {"x": point.x, "y": point.y} for point in bounding_box.polygon
        ]
    }
