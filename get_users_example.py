from auth import get_access_token
from api import api_call
# from pdb import set_trace as st

# Obtain the access token
try:
    access_token = get_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # API Documentation
    # https://learn.microsoft.com/en-us/graph/api/user-get?view=graph-rest-1.0&tabs=http
    logs = api_call(headers, 'https://graph.microsoft.com/beta/users')
    for user in logs:
        print(user['mail'])
except Exception as e:
    print(e)
