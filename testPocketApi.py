from pocket import api as pocket
import pocketConsumerKey

if 'accessToken' not in dir(pocketConsumerKey):
    redirectUri = 'pocketapp1234:authorizationFinished'
    reqCode = pocket.getRequestToken(pocketConsumerKey.key, redirectUri)

    print 'https://getpocket.com/auth/authorize?request_token=%s&redirect_uri=%s' % (reqCode, redirectUri)

    raw_input('Press enter')

    pocketConsumerKey.accessToken = pocket.getAccessToken(pocketConsumerKey.key, reqCode)
    print pocketConsumerKey.accessToken
    
print pocket.retrieve(pocketConsumerKey.key, pocketConsumerKey.accessToken[0])
