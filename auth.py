import requests
from settings import client_id, client_secret, tenant_id

def get_access_token():
    scope = 'https://graph.microsoft.com/.default'
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope
    }

    # Obtain the access token
    response = requests.post(token_url, data=data)
    access_token = response.json().get('access_token')

    # Check if the token was obtained successfully
    if access_token:
        return access_token
    else:
        raise Exception(f"Failed to obtain access token: {response.json()}")

