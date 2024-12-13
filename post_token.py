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

url = "https://10.1.10.17/api/fdm/v6/object/networks"

payload_obj = json.dumps({
  "name": "SushilBond4",
  "description": "FTD141224Practice4",
  "subType": "NETWORK",
  "value": "54.54.54.0/24",
  "dnsResolution": "IPV4_ONLY",
  "type": "networkobject"
})
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': f"Bearer {token}"
}

response = requests.request("POST", url, headers=headers, data=payload_obj, verify=False)

print(response.text)


