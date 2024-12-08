#File will implement the FDM client. This code will handle all communication with FDM.

import requests
import time
import datetime
from rich import print


class FDMClient:
    def __init__(self, host, port=443, username='admin', password='1234QWer!', log=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.log = log
        if not log:
            raise Exception('The logger should not be None.')
        self.token = None
        self.base_headers = {'Content-Type': 'application/json', 'Accept': 'application/json',}
        self.base_url = f'https://{self.host}:{self.port}/api/fdm/v6' #make sure about the version v2 or v6
        requests.packages.urllib3.disable_warnings()
        self.log.debug('FDMClient class initialization finished.')
    
    def _send_request(self, url, method='get', headers=None, body=None, params=None):
        self.log.debug('Sending request to FDM.')
        requests_method = getattr(requests, method)
        if not headers:
            headers = self.base_headers
            
        self.log.debug(f'Using URL: {url}')
        self.log.debug(f'Using method: {method}')
        self.log.debug(f'Using headers: {str(headers)}')
        self.log.debug(f'Using body: {str(body)}')
        self.log.debug(f'Using query strings: {str(params)}')
        
        response = requests_method(url, verify=False, headers=headers, json=body, params=params)
        status_code =response.status_code
        response_body = response.json()
        self.log.debug(f'Got status code: {str(status_code)}')
        self.log.debug(f'Got response body: {str(response_body)}')
        if status_code != 200:
            msg = response_body.get('message', 'Request to FDM unsuccessful.')
            raise Exception(msg)
        return response_body
    
    
    def _get_auth_headers(self):
        headers = self.base_headers.copy()
        if self.token:headers['Authorization'] = f'Bearer {self.token}'
        else:
            msg = 'No token exists, use login method to get the token.'
            raise Exception(msg)    
        return headers
    
    def login(self):
        self.log.debug('Login to FDM.')
        url = self.base_url+ '/fdm/token'
        body = {
            'grant_type': 'password', 'username': f'{self.username}', 'password': f'{self.password}',
        }
        self.log.debug('Sending the login request to FDM.')
        response = self._send_request(url, method='post', body=body)
        self.token = response.get('access_token')
        self.log.debug(f'Access token: {self.token}')
        
        
    def logout(self):
        self.log.debug('Logout from FDM.')
        url = self.base_url + '/fdm/token'
        body = {
            'grant_type': 'revoke_token','access_token': self.token,'token_to_revoke': self.token,
        }
        self.log.debug('Sending the logout request to FDM.')
        self._send_request(url, method='post', body=body)    
        self.log.debug('Logout successful.')
        
    # def get_access_policy_id(self):
        
        
    # def get_access_rule_by_name(self, name):
        
        
    # def put_access_rule(self, data):
        
        
    # def get_url_categories(self):
        
        
    # def deploy(self, timeout=180):