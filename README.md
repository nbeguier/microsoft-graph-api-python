# Microsoft-Graph-API-Python

## Setup

You can integrate **Microsoft Azure AD®** (Active Directory) with your scripts and build policies based on user identity and group membership. Users will authenticate to your script using their client secret.

### 1. Obtain Azure AD Settings

The following **Azure AD** values are required to set up the integration:

- **Application (client) ID**
- **Directory (tenant) ID**
- **Client secret**

To retrieve those values:

1. Log in to the **Azure dashboard**.
2. Go to **All services > Azure Active Directory**.
3. In the **Azure Active Directory** menu, go to [Enterprise applications](https://entra.microsoft.com/#view/Microsoft_AAD_IAM/StartboardApplicationsMenuBlade/~/AppAppsPreview).
4. Select **New application > Create your own application**.
5. Name your application.
6. Select **Register an application to integrate with Azure AD (App you're developing)** and then select **Create**.
7. Select **Register**.
8. Return to the **Azure Active Directory** menu and go to [App registrations](https://entra.microsoft.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade/quickStartType~/null/sourceType/Microsoft_AAD_IAM).
9. Select the app you just created. Copy the **Application (client) ID** and **Directory (tenant) ID**.
10. Go to **Certificates & secrets** and select **New client secret**.
11. Name the client secret and choose an expiration period.
12. After the client secret is created, copy its **Value** field. Store the client secret in a safe place, as it can only be viewed immediately after creation.

### 2. Configure API Permissions in Azure

1. From the **App registrations** page for your application, go to **API permissions**.
2. Select **Add a permission**.
3. Select **Microsoft Graph**.
4. Select **Delegated permissions** and enable the following permissions:
- `email`
- `offline_access`
- `openid`
- `profile`
- `User.Read`
- `Directory.Read.All`
- `GroupMember.Read.All`

> **Note:** Those are some example right. If you are blocked, you may need to add more. Go to the [API documentation](https://learn.microsoft.com/en-us/graph/api/overview?view=graph-rest-1.0) to know which rights to add.

5. Once all seven permissions are enabled, select **Add permissions**.
6. Select **Grant admin consent**.

### 3. Add secrets in settings.py

```
cp settings.py.sample settings.py
vim settings.py # Add secrets inside
```

---

## Usage

Take inspiration in the following example. Roughly, you need to use:

```python
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
    # https://learn.microsoft.com/en-us/graph/api/overview?view=graph-rest-1.0
    logs = api_call(headers, 'https://graph.microsoft.com/XXXXXXXXXXXX')
    print(logs)
except Exception as e:
    print(e)

```

and then:
```bash
pip install -U -r requirements.txt
python get_users_example.py
```
