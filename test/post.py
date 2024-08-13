#!/usr/bin/env python

import requests
import json

# Read the payload from the JSON file
with open('payload_queue.json', 'r') as file:
    payload = json.load(file)

# Make the POST request
response = requests.post('http://127.0.0.1:8000/webhook', json=payload)

# Check the response status code
print(f"response code: {response.status_code}")
if response.status_code == 201:
    print('Message posted successfully.')
else:
    print('Failed to post message.')
