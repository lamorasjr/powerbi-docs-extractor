import requests

def get_access_token(scope_app, tenant_id, client_id, client_secret):
    if scope_app == 'powerbi':
        scope = 'https://analysis.windows.net/powerbi/api/.default'
    elif scope_app == 'sharepoint':
        scope = 'https://graph.microsoft.com/.default'
    else:
        raise ValueError(f'"{scope_app}" is an invalid scope value. Use "powerbi" or "sharepoint".')

    url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope
    }
    response = requests.post(url=url, data=payload)
    if response.status_code == 200:
        response_json = response.json()
        data = response_json['access_token']
        return data
    else:
        raise Exception(f'Failed to obtain token: {response.status_code} - {response.text}')