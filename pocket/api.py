import requests
from requests.exceptions import HTTPError
import json

class PocketException(Exception):
    
    def __init__(self, errCode, errMessage):
        self.errCode = int(errCode)
        self.errMessage = errMessage
        
    def __str__(self):
        return repr('[%d] %s' % (self.errCode, self.errMessage))
        
class PocketInvalidRequestException(PocketException):
    pass
        
class PocketUserAuthenticationException(PocketException):
    pass
        
class PocketAccessDeniedException(PocketException):
    pass
        
class PocketServerDownException(PocketException):
    pass

def get_request_token(consumer_key, redirect_uri):
    data = {'consumer_key': consumer_key, 'redirect_uri': redirect_uri}
    headers = {'Content-Type': 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}
    
    response = requests.post('https://getpocket.com/v3/oauth/request', data=json.dumps(data), headers=headers)
    try:
        response.raise_for_status()
        return response.json()['code']
    except HTTPError:
        if response.status_code == 400:
            raise PocketInvalidRequestException(response.headers['x-error-code'], response.headers['x-error'])
        elif response.status_code == 401:
            raise PocketUserAuthenticationException(response.headers['x-error-code'], response.headers['x-error'])
        elif response.status_code == 403:
            raise PocketAccessDeniedException(response.headers['x-error-code'], response.headers['x-error'])
        elif response.status_code == 503:
            raise PocketServerDownException(response.headers['x-error-code'], response.headers['x-error'])
        else:
            raise PocketException(response.headers['x-error-code'], response.headers['x-error'])
            
    
