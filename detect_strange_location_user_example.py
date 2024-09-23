from auth import get_access_token
from api import api_call
from collections import defaultdict
from datetime import datetime, timedelta, timezone
# from pdb import set_trace as st

# Get last month of logs in learning phase
history_days = 60 # 30 is better

# Put 1 to get only last day login issues in detection phase
period_days = 365 # 365 is better

# The country and device id occurs in logs, below this percent there is an alert
country_ceil = 33
device_id_ceil = 33

# Countries that will be ignored in detection phase
country_whitelist = ['FR']

def display_logs(logs):
    user_logs = defaultdict(list)
    user_country_count = defaultdict(lambda: defaultdict(int))
    user_os_count = defaultdict(lambda: defaultdict(int))

    # LEARNING PHASE
    # Group logs by user, only for successful logins
    for log in logs:
        if log['status']['errorCode'] == 0:
            username = log['userDisplayName']
            country_code = log['location']['countryOrRegion']
            os_type = log['deviceDetail']['operatingSystem']
            user_logs[username].append(log)
            user_country_count[username][country_code] += 1
            user_os_count[username][os_type] += 1

    # DETECTION PHASE
    # Display logs with the percentage of logs containing the country code
    for log in logs:
        if log['status']['errorCode'] == 0 and \
        log['location']['countryOrRegion'] not in country_whitelist and \
        datetime.fromisoformat(log['createdDateTime'].replace('Z', '+00:00')) >= \
        (datetime.now(timezone.utc) - timedelta(days=period_days)) and \
        not log['deviceDetail']['deviceId']:  # If it doesn't exist, it means it's not trusted 
            username = log['userDisplayName']
            country_code = log['location']['countryOrRegion']
            os_type = log['deviceDetail']['operatingSystem']
            total_logs = len(user_logs[username])
            country_logs = user_country_count[username][country_code]
            country_percentage = (country_logs / total_logs) * 100
            os_logs = user_os_count[username][os_type]
            os_percentage = (os_logs / total_logs) * 100
            if (country_percentage < country_ceil and os_percentage < device_id_ceil) or (not os_type and not log['deviceDetail']['browser']):
                print(f'[{log["createdDateTime"]}] {username} from {country_code} '
                      f'({country_percentage:.2f}%), OS: {os_type} ({os_percentage:.2f}%)')


# Obtain the access token
try:
    access_token = get_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Define the time period for the logs
    start_date = (datetime.now(timezone.utc) - timedelta(days=history_days)).strftime('%Y-%m-%dT%H:%M:%SZ')
    end_date = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    # API Documentation
    # https://learn.microsoft.com/en-us/graph/api/resources/azure-ad-auditlog-overview?view=graph-rest-1.0
    print('Can be quite long...')
    logs = api_call(
        headers,
        f'https://graph.microsoft.com/v1.0/auditLogs/signIns?$filter=createdDateTime ge {start_date} and createdDateTime le {end_date}')
    display_logs(logs)
except Exception as e:
    print(e)
