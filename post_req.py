import requests
import json

url = "http://127.0.0.1:8000/api/data"
payload = {
    "filepath": "C:\\Users\\chapman.beaird\\Documents\\LeaseExtractor\\MicrosoftDataCenterLeaseExamples\\TrainingLeases\\TripleNLeases\\Triple-Net-NNN-Lease-Agreement(test).pdf",
    "form_recognizer": False
}
headers = {
    "Content-Type" : "application/json"
}


response = requests.post(url, data=json.dumps(payload), headers=headers)

# Check if the request was successful
if response.status_code == 200:
    try:
        # Attempt to parse response as JSON
        data = response.json()
    except json.JSONDecodeError as e:
        print("Response is not in JSON format:", e)
        print("Response content:", response.text)
else:
    print("Request failed with status code:", response.status_code)