import os
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


def export_csv_or_parquet(df: pd.DataFrame, file_name:str, output_format:str, output_path:str):
    """
    Custom function to export the api data to csv or parquet
    """
    if output_format == 'csv':
        df.to_csv(f'{output_path}/{file_name}.csv', index=False, sep=';', encoding='utf-8')
        print(f'- Successfully exported: {file_name}.{output_format}.')
        
    elif output_format == 'parquet':
        df.to_parquet(f'{output_path}/{file_name}.parquet', index=False)
        print(f'- Successfully exported: {file_name}.{output_format}.')

    else:
        raise ValueError('Wrong output format, select between "csv" or "parquet".')


def etl_powerbi_data(access_token:str, workspaces_ids:list, output_format:str, output_path):
    try:
        workspaces = extract_workspaces(access_token, workspaces_ids)
        export_csv_or_parquet(workspaces, 'workspaces', output_format, output_path)

        reports = extract_reports(access_token, workspaces_ids)
        export_csv_or_parquet(reports, 'reports', output_format, output_path)

        reports_pages = extract_reports_pages(access_token, workspaces_ids)
        export_csv_or_parquet(reports_pages, 'reports_pages', output_format, output_path)

        datasets = extract_datasets(access_token, workspaces_ids)
        export_csv_or_parquet(datasets, 'datasets', output_format, output_path)

        dax_queries_dir = os.path.join(os.getcwd(), 'src', 'dax_queries')

        for file in os.listdir(dax_queries_dir):
            if file.endswith('.txt'):
                file_name = file.split(".")[0] 
                file_dir = os.path.join(dax_queries_dir, file)

                with open(file_dir, 'r') as file:
                    dax_query = file.read()
                
                df_query_temp = extract_datasets_info_queries(access_token, workspaces_ids, dax_query)
                export_csv_or_parquet(df_query_temp, file_name, output_format, output_path)

    except Exception as e:
        print(f'Power BI ETL error: {e}')




