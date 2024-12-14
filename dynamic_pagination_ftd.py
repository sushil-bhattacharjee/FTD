import requests
import json
from rich import print

# Disable Warnings for insecure access
requests.packages.urllib3.disable_warnings()

# Create access Token for further action
url = "https://10.1.10.17/api/fdm/v6/fdm/token"

payload = {"grant_type": "password", "username": "admin", "password": "1234QWer!"}
headers = {"Accept": "application/json", "Content-Type": "application/json"}

# Request the token
token_response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
token_response.raise_for_status()

if token_response.status_code == 200:
    print("[green]Token Successfully Received..\n")

# Store the token
token = token_response.json()["access_token"]

# Fetch network objects
get_url = "https://10.1.10.17/api/fdm/v6/object/networks"
headers_get = {
    "Accept": "application/json",
    "Authorization": f"Bearer {token}"
}

# Track page number
page_number = 1

# Initial request
response_get = requests.get(get_url, headers=headers_get, verify=False)
response_get.raise_for_status()  # Ensure the initial request is successful
response_get_json = response_get.json()

# Print the first page
print(f"[blue]Page {page_number}:[/blue]")
print(response_get_json['items'])

# Handle pagination
while 'paging' in response_get_json and response_get_json['paging']['next']:
    page_number += 1  # Increment the page number
    url_next = response_get_json['paging']['next'][0]  # Get the next URL
    response_next = requests.get(url_next, headers=headers_get, verify=False)
    response_next.raise_for_status()  # Ensure the pagination request is successful
    response_get_json = response_next.json()
    
    # Print the current page
    print(f"[blue]Page {page_number}:[/blue]")
    print(response_get_json['items'])


