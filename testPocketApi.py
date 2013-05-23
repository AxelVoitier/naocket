from pocket import api as pocket

POCKET_PLATFORM_CONSUMER_KEY = ''

print pocket.get_request_token(POCKET_PLATFORM_CONSUMER_KEY, 'pocketapp1234:authorizationFinished')
