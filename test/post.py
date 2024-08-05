import requests
import json

# Read the payload from the JSON file
with open('payload_queue.json', 'r') as file:
    payload = json.load(file)

# Read the headers from the text file
with open('header_queue.txt', 'r') as file:
    headers = file.read()

# Make the POST request
response = requests.post('http://127.0.0.1:8000/webhook', json=payload)

# Check the response status code
if response.status_code == 201:
    print('Message posted successfully.')
else:
    print('Failed to post message.')