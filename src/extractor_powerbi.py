import json
import requests
import pandas as pd
import re
import os
import subprocess
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

def get_powerbi_token():
    TENANT_ID = os.getenv('AZURE_APP_TENANT_ID')
    CLIENT_ID = os.getenv('AZURE_APP_CLIENT_ID')
    CLIENT_SECRET = os.getenv('AZURE_APP_CLIENT_SECRET')

    url = f'https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token'
    
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'https://analysis.windows.net/powerbi/api/.default'
    }

    response = requests.post(url=url, data=payload)
    if response.status_code == 200:
        response_json = response.json()
        data = response_json['access_token']
        return data
    
    else:
        raise Exception(f'Failed to obtain token: {response.status_code} - {response.text}')


def get_powerbi_data(endpoint:str)->json:

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
        raise Exception(f'Failed request - error: {response.status_code} - {response.text}')
    
    
def execute_powerbi_dataset_query(workspace_id:str, dataset_id:str, dax_query:str)->dict:

    access_token = get_powerbi_token()

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


def extract_workspaces(workspaces_ids:list)->pd.DataFrame:

    all_data = []

    for ws_id in workspaces_ids:
        endpoint = ws_id
        data = get_powerbi_data(endpoint)
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


def extract_reports(workspaces_ids:list)->pd.DataFrame:  

    all_data = []

    for ws_id in workspaces_ids:
        endpoint = f'{ws_id}/reports'
        response = get_powerbi_data(endpoint)
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


def extract_reports_pages(workspaces_ids:list)->pd.DataFrame:

    df_reports = extract_reports(workspaces_ids)
    
    df_reports = df_reports[df_reports['REPORT_TYPE'] == 'PowerBIReport']

    workspaces_reports_ids = df_reports[['WORKSPACE_ID', 'REPORT_ID']].to_dict(orient='records')

    all_data = []

    for i in workspaces_reports_ids:
        ws_id = i.get('WORKSPACE_ID')
        rp_id = i.get('REPORT_ID')

        endpoint = f'{ws_id}/reports/{rp_id}/pages'
        response = get_powerbi_data(endpoint)
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


def extract_datasets(workspaces_ids:list)->pd.DataFrame:
    all_data = []

    for ws_id in workspaces_ids:
        endpoint = f'{ws_id}/datasets'
        response = get_powerbi_data(endpoint)
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


def extract_datasets_info_queries(workspaces_ids:list, dax_query:str)->pd.DataFrame:
    
    df_datasets = extract_datasets(workspaces_ids)
    
    workspaces_reports_ids = df_datasets[['WORKSPACE_ID', 'DATASET_ID']].to_dict(orient='records')

    all_data = []

    for i in workspaces_reports_ids:
        ws_id = i.get('WORKSPACE_ID')
        ds_id = i.get('DATASET_ID')
        
        data = execute_powerbi_dataset_query(ws_id, ds_id, dax_query)

        all_data.append(data)

    df_raw = pd.json_normalize(all_data, meta=['WORKSPACE_ID', 'DATASET_ID'], record_path='response')
    df = df_raw.copy()
    old_columns_name = df.columns
    new_columns_name = {i: re.sub(r'\[([^\]]+)\]', r'\1', i) for i in old_columns_name}
    df = df.rename(columns=new_columns_name)
    
    return df


def dscmd_execute_query(workspace_name, dataset_name, query_file)->pd.DataFrame:

    output_file = os.path.join(os.getcwd(), 'tools', 'temp.csv')
    
    DSCMD = os.path.join(os.getcwd(), 'tools', 'dax_studio', 'dscmd.exe')

    if os.path.exists(DSCMD):
        TENANT_ID = os.getenv('AZURE_APP_TENANT_ID')
        CLIENT_ID = os.getenv('AZURE_APP_CLIENT_ID')
        CLIENT_SECRET = os.getenv('AZURE_APP_CLIENT_SECRET')

        prompt = [
            DSCMD,
            "csv", output_file,
            "-s", f"powerbi://api.powerbi.com/v1.0/myorg/{quote(workspace_name)}",
            "-d", dataset_name,
            "-u", f"app:{CLIENT_ID}@{TENANT_ID}", 
            "-p", CLIENT_SECRET,
            "-f", query_file,
            "-t", "UTF8CSV"
        ]

        try:
            subprocess.run(prompt, capture_output=True, text=True, check=True)
            df = pd.read_csv(output_file, encoding='utf-8', sep=';')
            data = df.to_dict('records')
            os.remove(output_file)
            return data

        except subprocess.CalledProcessError as e:
            print(f"[WARNING][DaxStudio] Error to export {os.path.basename(query_file)} - return code: {e.returncode} - item: {workspace_name}/{dataset_name}.")
    else:
        raise FileNotFoundError('DaxStudio was not found. Check if all requirements have been installted.')
    

def dscmd_extract_datasets_info(workspaces_ids:list, query_file)->pd.DataFrame:

        df_ds = extract_datasets(workspaces_ids)
        df_ds = df_ds[['DATASET_ID', 'DATASET_NAME', 'WORKSPACE_ID']]

        df_ws = extract_workspaces(workspaces_ids)
        df_ws = df_ws[['WORKSPACE_ID', 'WORKSPACE_NAME']]
        
        df_ids = pd.merge(df_ds, df_ws, on='WORKSPACE_ID', how='left')
        wsds_ids = df_ids.to_dict(orient='records')
        
        all_data = []

        for i in wsds_ids:
            ds_name = i.get('DATASET_NAME')
            ws_name = i.get('WORKSPACE_NAME')

            response = dscmd_execute_query(ws_name, ds_name, query_file)

            data = {
                'WORKSPACE_ID': i.get('WORKSPACE_ID'),
                'DATASET_ID' : i.get('DATASET_ID'),
                'response' : response
            }

            all_data.append(data)

        df_raw = pd.json_normalize(all_data, meta=['WORKSPACE_ID', 'DATASET_ID'], record_path='response')
        df = df_raw.copy()
        return df       