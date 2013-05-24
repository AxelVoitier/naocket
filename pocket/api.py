# Copyright Axel Voitier (May 2013)
# 
# axel.voitier@gmail.com
# 
# This software is a computer program whose purpose is to have NAO,
# the humanoid robot, read aloud articles saved in Pocket.
# 
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software.  You can  use, 
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info". 
# 
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability. 
# 
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and,  more generally, to use and operate it in the 
# same conditions as regards security. 
# 
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

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
