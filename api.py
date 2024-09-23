import requests

def api_call(headers, api_url):
    logs = []
    while api_url:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            logs.extend(data.get('value', []))
            api_url = data.get('@odata.nextLink', None)  # Get the next page URL if it exists
        else:
            print(f"Error: {response.status_code}, {response.json()}")
            api_url = None
    return logs

