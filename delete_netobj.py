import os
import requests
import json
from rich import print 

requests.packages.urllib3.disable_warnings()

target = input("Enter the object you wish to delete:  ")
clear_screen = 'clear'
os.system(clear_screen)


#Create  a Token and store it
url = "https://10.1.10.17/api/fdm/v6/fdm/token"

payload = {"grant_type": "password", "username": "admin", "password": "1234QWer!"}
headers = {"Accept": "application/json", "Content-Type": "application/json"}

token_response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
token_response.raise_for_status()


if token_response.status_code == 200:
    print("[green]Token Successfully Received..\n")
    

#Store the previously created token as "token"
token = token_response.json()["access_token"]

url_obj = "https://10.1.10.17/api/fdm/v6/object/networks"
headers = {
  'Accept': 'application/json',
  'Authorization': f"Bearer {token}"
}


get_response = requests.get(url_obj, headers=headers, verify=False).json()
items = get_response["items"]
name_list = []
for item in items:
    addname = item['name']
    name_list.append(addname)
    if item["name"] == target:
        targetname = item["name"]
        objectid = item["id"]
        url = f"https://10.1.10.17/api/fdm/v6/object/networks/{objectid}"
        del_response = requests.delete(url, headers=headers, verify=False)
        if del_response.status_code == 204:
            print(f"[green]SUCCESS: DELETED {targetname} OBJECT")
if target not in name_list:
    print(f"[red]ERROR! {target} OBJECT DOES NOT EXIST")
