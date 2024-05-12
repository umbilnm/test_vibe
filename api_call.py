import os
import requests
import base64
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('YANDEX_API_KEY')

def encode_file(file):
    with open(file, 'rb') as file:
        file_content = file.read()
    content = base64.b64encode(file_content)
    
    return content.decode('utf-8')


def ocr_yandex(file):
    url = 'https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Api-Key {api_key}',    
    }

    image_data = {
        "mimeType": "JPEG",
        "languageCodes": ["ru"],
        "model": "page",
        "content": file
    }
    json_data = json.dumps(image_data)
    response = requests.post(url, headers=headers, data=json_data)
    
    if response.status_code == 200:
        result = response.json()
        return result

