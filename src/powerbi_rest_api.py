import json
import requests

def get_auth_token(tenant_id:str, client_id:str, client_secret:str)->json:
    url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://analysis.windows.net/powerbi/api/.default'
    }
    response = requests.post(url=url, data=payload)
    if response.status_code == 200:
        response_json = response.json()
        data = response_json['access_token']
        return data
    else:
        raise Exception(f'Failed to obtain token: {response.status_code} - {response.text}')


def get_workspaces_info(access_token:str, workspace_id:str)->json:
    url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        data = response_json
        return data
    else:
        raise Exception(f'Failed request - error: {response.status_code} - {response.text}')


def get_workspace_reports(access_token:str, workspace_id:str)->json:
    url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        data = { 
            'WORKSPACE_ID' : workspace_id,
            'response' : response_json['value']
        }
        return data
    else:
        raise Exception(f'Failed request - error: {response.status_code} - {response.text}')


def get_workspace_datasets(access_token:str, workspace_id:str)->json:
    url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        data = { 
            'WORKSPACE_ID' : workspace_id,
            'response' : response_json['value']
        }
        return data
    else:
        raise Exception(f'Failed request - error: {response.status_code} - {response.text}')


def execute_dataset_query(access_token:str, workspace_id:str, dataset_id:str, dax_query:str)->json:
    url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/executeQueries'
    headers = { 
        'Authorization' : f'Bearer {access_token}',
        'Content-type' : 'application/json'
    }
    body = {
        'queries': [{'query': f'{dax_query}'}],
        'serializerSettings': {'includeNulls': 'true'}
    }
    response = requests.post(url=url, headers=headers, json=body)
    if response.status_code == 200:
        response_json = response.json()
        data = {
            "WORKSPACE_ID": workspace_id,
            "DATASET_ID": dataset_id,
            "response" : response_json['results'][0]['tables'][0]['rows']
        }
        return data
    else:
        raise Exception(f'Non-sucess status code: {response.status_code} - {response.text}')
    

def get_report_pages(access_token:str, workspace_id:str, report_id:str)->json:
    url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}/pages'
    headers = { 
        'Authorization' : f'Bearer {access_token}',
        'Content-type' : 'application/json'
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        data = {
            "WORKSPACE_ID": workspace_id,
            "REPORT_ID": report_id,
            "response" : response_json['value']
        }
        return data
    else:
        raise Exception(f'Non-sucess status code: {response.status_code} - {response.text}')