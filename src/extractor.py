import os
import re
import pandas as pd
from powerbi_rest_api import (
    get_workspaces_info, 
    get_workspace_reports,
    get_workspace_datasets, 
    execute_dataset_query, 
    get_report_pages 
)


def export_to_csv_or_parquet(df: pd.DataFrame, file_name:str, output_path: str, output_format: str):
    """
    Custom function to export the api data to csv or parquet
    """
    if output_format == 'csv':
        df.to_csv(f'{output_path}/{file_name}.csv', index=False, sep=';', encoding='utf-8')
        print(f'File exported sucessfully: {file_name}.csv')
    elif output_format == 'parquet':
        df.to_parquet(f'{output_path}/{file_name}.parquet', index=False)
        print(f'File exported sucessfully: {file_name}.parquet')
    else:
        print('Wrong output format, select between "csv" or "parquet"')


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
    export_to_csv_or_parquet(df, 'workspaces', output_path, output_format)


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
    export_to_csv_or_parquet(df, 'reports', output_path, output_format)


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
    export_to_csv_or_parquet(df, 'reports_pages', output_path, output_format)


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
    export_to_csv_or_parquet(df, 'datasets', output_path, output_format)


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
        export_to_csv_or_parquet(df, f'datasets_{file_name}', output_path, output_format)