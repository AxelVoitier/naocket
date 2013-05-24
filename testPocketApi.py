from pocket import api as pocket
import pocketConsumerKey

if 'accessToken' not in dir(pocketConsumerKey):
    api = pocket.PocketAPI(pocketConsumerKey.key)
    redirectUri = 'pocketapp1234:authorizationFinished'
    reqCode = api.getRequestToken(redirectUri)

    print 'https://getpocket.com/auth/authorize?request_token=%s&redirect_uri=%s' % (reqCode, redirectUri)

    raw_input('Press enter')

    pocketConsumerKey.accessToken = api.getAccessToken(reqCode)
    print pocketConsumerKey.accessToken
else:
    api = pocket.PocketAPI(pocketConsumerKey.key, pocketConsumerKey.accessToken[0], pocketConsumerKey.accessToken[1])
    
print api.retrieve()
