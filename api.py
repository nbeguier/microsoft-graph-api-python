import requests

def api_call(headers, api_url, raw=False, session=None):
    logs = []
    while api_url:
        if session:
            response = session.get(api_url)
        else:
            response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if raw:
                return data
            logs.extend(data.get('value', []))
            api_url = data.get('@odata.nextLink', None)  # Get the next page URL if it exists
        else:
            raise Exception(f"Error: {response.status_code}, {response.json()}")

    return logs
