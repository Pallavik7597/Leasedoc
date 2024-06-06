import os
from openai import AzureOpenAI


def connect(endpoint, api_key, api_version):

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version
    )
    return client

def askGPT(client, prompt, model, search_client):
    if prompt == "":
        prompt = "Could you please list all the filled in information in the lease? for example, Date of the agreement, Lessor, Lessee, Address, Lessor Address, Lessee Address, Rent per year, Security Deposit, Lease Start date, lease end date. Please output in Json format. for example, for lessor use the following structure: {\"lessor\":[{\"name\":\"\",\"lessor_address\":\"\"}]}. Do not provide code or explanation and structure it in proper JSON. Remove '''json from the beginning of the response if it is there."
   
    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
        extra_body={
            "data_sources": [
                {
                    "type": "AzureCognitiveSearch",
                    "parameters": {
                        "endpoint": search_client._endpoint,
                        "key": search_client._credential._key,
                        "indexName": search_client._index_name,
                        "inScope": True
                    }
                }
            ]
        }
    )
    if response.choices[0].message.content == "The requested information is not available in the retrieved data. Please try another query or topic.":
        print(".")
        askGPT(client, "The information is available in the lease. Could you please list all the filled in information in the lease? for example, Date of the agreement, Lessor, Lessee, where the property is located at, Lessor Address, Lessee Address, Rent per year or per month, Security Deposit, Lease Start date, lease end date. Please output in Json format. for example, for lessor use the following structure: {\"lessor\":[{\"name\":\"\",\"lessor_address\":\"\"}]}. Do not provide code or explanation and structure it in proper JSON. Remove '''json from the beginning of the response if it is there.", model, search_client)
    else:
        return response.choices[0].message.content

