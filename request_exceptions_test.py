import requests
import json
from rich import print
from requests.exceptions import Timeout

#Disable Warnings for insecure access
requests.packages.urllib3.disable_warnings()

# Create access Token for further action
url = "https://10.1.10.17/api/fdm/v6/fdm/token"

payload = {"grant_type": "password", "username": "admin", "password": "1234QWer!"}
headers = {"Accept": "application/json", "Content-Type": "application/json"}

# token_response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
# token_response.raise_for_status()

sess =requests.session()
try:
    rc = sess.request('POST', url, data=payload, verify=False, timeout=1)
    
except Timeout:
    print('Timeout Error: Unable to access FTD!!')
    exit(-1)
    
if rc.status_code == requests.codes.ok :
    print('The request was successful')
else:
    print(f'Error Code: {rc.status_code}:{rc.reason}')