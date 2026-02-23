import time
from requests import request

def api_call(headers, api_url, raw=False, session=None, method='GET', body=None, max_retries=6):
    logs = []

    while api_url:
        for attempt in range(max_retries):
            if session:
                response = session.request(method, api_url, json=body)
            else:
                response = request(method, api_url, headers=headers, json=body)

            status = response.status_code

            if status in (502, 503, 504):
                time.sleep(min(2 ** attempt, 20))
                continue

            if status == 429:
                retry_after = int(response.headers.get("Retry-After", 5))
                time.sleep(retry_after)
                continue

            break
        else:
            raise Exception(f"Max retries exceeded ({status}): {response.text}")

        if status in (200, 201):
            try:
                data = response.json()
            except Exception:
                raise Exception(f"Invalid JSON response: {response.text}")

            if raw:
                return data

            logs.extend(data.get('value', []))
            api_url = data.get('@odata.nextLink')
            body = None  # body uniquement sur le premier call (POST typiquement)

        else:
            try:
                err = response.json()
            except Exception:
                err = response.text
            raise Exception(f"Error: {status}, {err}")

    return logs