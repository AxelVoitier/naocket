from pocket import api as pocket
import pocketConsumerKey

print pocket.get_request_token(pocketConsumerKey.key, 'pocketapp1234:authorizationFinished')
