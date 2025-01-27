import json
import requests
import pandas as pd
import re

def get_powerbi_data(access_token:str, endpoint:str)->json:
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
        raise Exception(f'Failed request - error: {response.status_code} - {response.text}')
    
    
def execute_powerbi_dataset_query(access_token:str, workspace_id:str, dataset_id:str, dax_query:str)->dict:
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


def extract_workspaces(access_token:str, workspaces_ids:list)->pd.DataFrame:
    all_data = []

    for ws_id in workspaces_ids:
        endpoint = ws_id
        data = get_powerbi_data(access_token, endpoint)
        all_data.append(data)

    df_raw = pd.json_normalize(all_data)
    df = df_raw.copy()
    df = df[['id', 'name', 'type']]
    df = df.rename(columns={
        'id': 'WORKSPACE_ID',
        'name': 'WORKSPACE_NAME',
        'type': 'TYPE'
    })
    return df


def extract_reports(access_token:str, workspaces_ids:list)->pd.DataFrame:
    all_data = []

    for ws_id in workspaces_ids:
        endpoint = f'{ws_id}/reports'
        response = get_powerbi_data(access_token, endpoint)
        data = {
            'WORKSPACE_ID' : ws_id,
            'response' : response.get('value')
        }
        all_data.append(data)

    df_raw = pd.json_normalize(all_data, meta='WORKSPACE_ID', record_path='response')
    df = df_raw.copy()
    df = df[['id', 'name', 'reportType', 'webUrl', 'WORKSPACE_ID']]
    df = df.rename(columns={
        'id':'REPORT_ID', 
        'name':'REPORT_NAME', 
        'reportType':'REPORT_TYPE', 
        'webUrl':'WEB_URL'
    })
    return df


def extract_reports_pages(access_token:str, workspaces_ids:list)->pd.DataFrame:
    df_reports = extract_reports(access_token, workspaces_ids)
    df_reports = df_reports[df_reports['REPORT_TYPE'] == 'PowerBIReport']

    workspaces_reports_ids = df_reports[['WORKSPACE_ID', 'REPORT_ID']].to_dict(orient='records')

    all_data = []

    for i in workspaces_reports_ids:
        ws_id = i.get('WORKSPACE_ID')
        rp_id = i.get('REPORT_ID')

        endpoint = f'{ws_id}/reports/{rp_id}/pages'
        response = get_powerbi_data(access_token, endpoint)
        data = {
            'WORKSPACE_ID' : ws_id,
            'REPORT_ID' : rp_id,
            'response' : response.get('value')
        }
        all_data.append(data)
    
    df_raw = pd.json_normalize(all_data, meta=['WORKSPACE_ID', 'REPORT_ID'], record_path='response')
    df = df_raw.copy()
    df = df.rename(columns={
        'name':'PAGE_SECTION', 
        'displayName':'PAGE_NAME', 
        'order':'ORDER'
    })
    return df


def extract_datasets(access_token:str, workspaces_ids:list)->pd.DataFrame:
    all_data = []

    for ws_id in workspaces_ids:
        endpoint = f'{ws_id}/datasets'
        response = get_powerbi_data(access_token, endpoint)
        data = {
            'WORKSPACE_ID' : ws_id,
            'response' : response.get('value')
        }
        all_data.append(data)

    df_raw = pd.json_normalize(all_data, meta='WORKSPACE_ID', record_path='response')
    df = df_raw.copy()
    df = df[['id', 'name', 'webUrl', 'createdDate', 'WORKSPACE_ID']]
    df = df.rename(columns={
        'id':'DATASET_ID', 
        'name':'DATASET_NAME', 
        'createdDate':'CREATED_DATE',
        'webUrl':'WEB_URL'
    })
    df['CREATED_DATE'] = pd.to_datetime(df['CREATED_DATE']).dt.date
    return df


def extract_datasets_info_queries(access_token:str, workspaces_ids:list, dax_query:str)->pd.DataFrame:
    
    df_datasets = extract_datasets(access_token, workspaces_ids)
    
    workspaces_reports_ids = df_datasets[['WORKSPACE_ID', 'DATASET_ID']].to_dict(orient='records')

    all_data = []

    for i in workspaces_reports_ids:
        ws_id = i.get('WORKSPACE_ID')
        ds_id = i.get('DATASET_ID')
        
        data = execute_powerbi_dataset_query(access_token, ws_id, ds_id, dax_query)

        all_data.append(data)

    df_raw = pd.json_normalize(all_data, meta=['WORKSPACE_ID', 'DATASET_ID'], record_path='response')
    df = df_raw.copy()
    old_columns_name = df.columns
    new_columns_name = {i: re.sub(r'\[([^\]]+)\]', r'\1', i) for i in old_columns_name}
    df = df.rename(columns=new_columns_name)
    return df