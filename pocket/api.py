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
    
class PocketAPI(object):

    def __init__(self, consumerKey, accessToken=None, username=None):
        self.consumerKey = consumerKey
        self.accessToken = accessToken
        self.username = username
        self.limits = None
        
    def _rawCallToPocketAPI(self, url, data):
        headers = {'Content-Type': 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        try:
            response.raise_for_status()
            limits = filter(lambda x: x[0].startswith('x-limit-'), response.headers.items())
            if (limits is not None) and (len(limits) > 0):
                self.limits = limits
                
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
    
    def _authCallToPocketAPI(self, url, data):
        data['consumer_key'] = self.consumerKey
        data['access_token'] = self.accessToken
        return self._rawCallToPocketAPI(url, data)

    def getRequestToken(self, redirectUri):
        data = {'consumer_key': self.consumerKey, 'redirect_uri': redirectUri}
        return self._rawCallToPocketAPI('https://getpocket.com/v3/oauth/request', data)['code']
            
    def getAccessToken(self, code):
        data = {'consumer_key': self.consumerKey, 'code': code}
        response = self._rawCallToPocketAPI('https://getpocket.com/v3/oauth/authorize', data)
        self.accessToken = response['access_token']
        self.username = response['username']
        return (self.accessToken, self.username)
    
    def retrieve(self, data = {}):
        response = self._authCallToPocketAPI('https://getpocket.com/v3/get', data)
        return response
