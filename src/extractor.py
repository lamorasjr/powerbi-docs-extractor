import os
import re
import pandas as pd
from src.loader import load_data
from src.powerbi_rest_api import (
    get_workspaces_info, 
    get_workspace_reports,
    get_workspace_datasets, 
    execute_dataset_query, 
    get_report_pages 
)

# Extract, transform and load powerbi workspaces
def etl_powerbi_workspaces(access_token:str, workspaces_ids:list, output_path:str, output_format:str):
    all_data = []

    for ws_id in workspaces_ids:
        response = get_workspaces_info(access_token, ws_id)
        all_data.append(response)

    df_raw = pd.json_normalize(all_data)
    df = df_raw.copy()
    df = df[['id', 'name', 'type']]
    df = df.rename(columns={
        'id': 'WORKSPACE_ID',
        'name': 'WORKSPACE_NAME',
        'type': 'TYPE'
    })
    load_data(df, 'powerbi_workspaces', output_path, output_format)


# Extract, transform and load powerbi reports
def etl_powerbi_reports(access_token:str, workspaces_ids:list, output_path:str, output_format:str):
    all_data = []

    for ws_id in workspaces_ids:
        response = get_workspace_reports(access_token, ws_id)
        all_data.append(response)

    df_raw = pd.json_normalize(all_data, meta='WORKSPACE_ID', record_path='response')
    df = df_raw.copy()
    df = df[['id', 'name', 'reportType', 'webUrl', 'WORKSPACE_ID']]
    df = df.rename(columns={
        'id':'REPORT_ID', 
        'name':'REPORT_NAME', 
        'reportType':'REPORT_TYPE', 
        'webUrl':'WEB_URL'
    })
    load_data(df, 'powerbi_reports', output_path, output_format)


# Extract, transform and load powerbi reports pages
def etl_powerbi_reports_pages(access_token:str, workspaces_ids:list, output_path:str, output_format:str):
    all_data = []

    for ws_id in workspaces_ids:
        response = get_workspace_reports(access_token, ws_id)
        for i in response['response']:
            rp_id = i['id']
            reponse_data = get_report_pages(access_token, ws_id, rp_id)
            all_data.append(reponse_data)

    df_raw = pd.json_normalize(all_data, meta=['WORKSPACE_ID', 'REPORT_ID'], record_path='response')
    df = df_raw.copy()
    df = df.rename(columns={
        'name':'PAGE_SECTION', 
        'displayName':'PAGE_NAME', 
        'order':'ORDER'
    })
    load_data(df, 'powerbi_reports_pages', output_path, output_format)


# Extract, transform and load powerbi datasets
def etl_powerbi_datasets(access_token:str, workspaces_ids:list, output_path:str, output_format:str):
    all_data = []

    for ws_id in workspaces_ids:
        response = get_workspace_datasets(access_token, ws_id)
        all_data.append(response)

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
    load_data(df, 'powerbi_datasets', output_path, output_format)


# Extract, transform and load powerbi dataset dax info queries
def etl_datasets_dax_queries(access_token:str, workspaces_ids:list, output_path:str, output_format:str):
    dax_queries_dir = os.path.join(os.getcwd(), 'dax_queries')

    for q in os.listdir(dax_queries_dir):
        file_name = q.split(".")[0]
        file_dir = os.path.join(dax_queries_dir, f'{file_name}.txt')

        with open(file_dir, 'r') as file:
            file_content = file.read()

        all_data = []

        for ws_id in workspaces_ids:    
            ds_response = get_workspace_datasets(access_token, ws_id)
            for i in ds_response['response']:
                ds_id = i['id']
                response = execute_dataset_query(access_token, ws_id, ds_id, file_content)
                all_data.append(response)

        df_raw = pd.json_normalize(all_data, meta=['WORKSPACE_ID', 'DATASET_ID'], record_path='response')
        df = df_raw.copy()
        old_columns_name = df.columns
        new_columns_name = {i: re.sub(r'\[([^\]]+)\]', r'\1', i) for i in old_columns_name}
        df = df.rename(columns=new_columns_name)
        load_data(df, f'powerbi_datasets_{file_name}', output_path, output_format)