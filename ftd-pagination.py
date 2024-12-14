import requests
import json
from rich import print

#Disable Warnings for insecure access
requests.packages.urllib3.disable_warnings()

# Create access Token for further action
url = "https://10.1.10.17/api/fdm/v6/fdm/token"

payload = {"grant_type": "password", "username": "admin", "password": "1234QWer!"}
headers = {"Accept": "application/json", "Content-Type": "application/json"}

token_response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
token_response.raise_for_status()


if token_response.status_code == 200:
    print("[green]Token Successfully Received..\n")
    

#Store the previously created token as "token"
token = token_response.json()["access_token"]

#Create a new network object

get_url = "https://10.1.10.17/api/fdm/v6/object/networks"

headers_get = {
    "Accept": "application/json",
    "Authorization": f"Bearer {token}"
}

response_get = requests.get(get_url, headers=headers_get, verify=False).json()
print(response_get)

while get_url:
    response = requests.get(get_url, headers=headers_get, params={f"limit": 10}, verify=False)
    response.raise_for_status()
    data = response.json()
    items = data["items"]
    print("\n")
    for item in items:
        name = item["name"]
        subType = item["subType"]
        value = item["value"]
        print(f"{name} is a {subType} object with a value of {value}")
    try:
        get_url = data['paging']['next'][0]
        if not get_url:
            break
    except IndexError:
        break