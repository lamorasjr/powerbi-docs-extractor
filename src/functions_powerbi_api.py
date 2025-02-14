import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_powerbi_token():
    """
    Generate an access token for power bi rest api
    """
    tenant_id = os.getenv("PBI_TENANT_ID")
    client_id = os.getenv("PBI_CLIENT_ID")
    client_secret = os.getenv("PBI_CLIENT_SECRET")

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
        raise KeyError(f'Failed to obtain token: {response.status_code} - {response.text}')
    

def get_powerbi_api_data(endpoint):
    """
    Generic function to extract data from power bi rest api
    """
    access_token = get_powerbi_token()

    url = f'https://api.powerbi.com/v1.0/myorg/groups/{endpoint}'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'  
    }

    response = requests.get(url=url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        raise KeyError(f'Failed request - error: {response.status_code} - {response.text}')
    

def extract_workspaces(workspaces_ids):
    """
    Extracts data about workspaces.
    """
    all_data = []

    for ws_id in workspaces_ids:
        endpoint = ws_id
        response = get_powerbi_api_data(endpoint)
        data = {
            "WORKSPACE_ID" : ws_id,
            "WORKSPACE_NAME" : response.get("name"),
            "TYPE" : response.get("type"),
            "DEDICATED_CAPACITY": response.get("isOnDedicatedCapacity"),
            "CAPACITY_ID" : response.get("capacityId"),
            "DATASET_STORAGE_FORMAT" : response.get("defaultDatasetStorageFormat")
        }
        all_data.append(data)

    df = pd.json_normalize(all_data)
    return df


def extract_datasets(workspaces_ids):
    """
    Extracts data about datasets contained in the workspaces list.
    """
    all_data = []

    for ws_id in workspaces_ids:
        endpoint = f'{ws_id}/datasets'
        response = get_powerbi_api_data(endpoint).get('value')

        for i in response:
            data = {
                "WORKSPACE_ID" : ws_id,
                "DATASET_ID" : i.get("id"),
                "DATASET_NAME" : i.get("name"),
                "CONFIGURED_BY": i.get("configuredBy"),
                "CREATED_AT" : i.get("createdDate"),
                "WEB_URL" : i.get("webUrl")
            }
            all_data.append(data)
    
    df = pd.json_normalize(all_data)
    df['CREATED_AT'] = pd.to_datetime(df['CREATED_AT']).dt.date
    return df


def extract_reports(workspaces_ids):
    """
    Extracts data about reports contained in the workspaces list.
    """
    all_data = []

    for ws_id in workspaces_ids:
        endpoint = f'{ws_id}/reports'
        response = get_powerbi_api_data(endpoint).get('value')

        for i in response:
            data = {
                "WORKSPACE_ID" : ws_id,
                "REPORT_ID" : i.get("id"),
                "REPORT_NAME" : i.get("name"),
                "REPORT_TYPE" : i.get("reportType"),
                "DATASET_ID": i.get("datasetId"),
                "WEB_URL" : i.get("webUrl")
            }
            all_data.append(data)
    
    df = pd.json_normalize(all_data)
    df = df[df['REPORT_TYPE'] == 'PowerBIReport']
    return df


def extract_reports_pages(df_reports):
    """
    Extracts data about pages contained in power bi reports.
    """
    workspaces_reports_ids = df_reports[['WORKSPACE_ID', 'REPORT_ID']].to_dict(orient='records')

    all_data = []

    for x in workspaces_reports_ids:
        ws_id = x.get('WORKSPACE_ID')
        rp_id = x.get('REPORT_ID')

        endpoint = f'{ws_id}/reports/{rp_id}/pages'
        response = get_powerbi_api_data(endpoint).get("value")
        
        for i in response:
            data = {
                "WORKSPACE_ID" : ws_id,
                "REPORT_ID" : rp_id,
                "PAGE_ID" : i.get("name"),
                "PAGE_NAME" : i.get("displayName"),
                "ORDER" : i.get("order")
            }
            all_data.append(data)
    
    df = pd.json_normalize(all_data)
    return df


    
if __name__ == "__main__":
    workspaces_ids = [ i.strip() for i in os.getenv('PBI_WORKSPACES_IDS').split(",") ]
    
    df_workspaces = extract_workspaces(workspaces_ids)
    print(df_workspaces.head())

    df_datasets = extract_datasets(workspaces_ids)
    print(df_datasets.head())

    df_reports = extract_reports(workspaces_ids)
    print(df_reports.head())

    df_reports_pages = extract_reports_pages(df_reports)
    print(df_reports_pages.head())