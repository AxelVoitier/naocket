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
    
def callToPocketAPI(url, data):
    headers = {'Content-Type': 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    try:
        response.raise_for_status()
        return response.json()
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
    

def getRequestToken(consumerKey, redirectUri):
    data = {'consumer_key': consumerKey, 'redirect_uri': redirectUri}
    return callToPocketAPI('https://getpocket.com/v3/oauth/request', data)['code']
            
def getAccessToken(consumerKey, code):
    data = {'consumer_key': consumerKey, 'code': code}
    response = callToPocketAPI('https://getpocket.com/v3/oauth/authorize', data)
    return (response['access_token'], response['username'])
    
def retrieve(consumerKey, accessToken):
    data = {'consumer_key': consumerKey, 'access_token': accessToken}
    response = callToPocketAPI('https://getpocket.com/v3/get', data)
    return response
