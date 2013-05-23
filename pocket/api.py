import requests
import json

def get_request_token(consumer_key, redirect_uri):
    data = {'consumer_key': consumer_key, 'redirect_uri': redirect_uri}
    headers = {'content-type': 'application/json; charset=UTF-8'}
    response = requests.post('https://getpocket.com/v3/oauth/request', data=json.dumps(data), headers=headers)
    return response
