import os
import pandas as pd
from extract_powerbi_api import get_all_reports, get_all_datasets, get_all_datasets_info

def export_data(df: pd.DataFrame, file_name:str, output_path: str, output_format: str):
    if output_format == 'csv':
        df.to_csv(f'{output_path}/{file_name}.csv', index=False, sep=';', encoding='utf-8')
        print(f'The data for {file_name} has been sucessfully exported')
    elif output_format == 'parquet':
        df.to_parquet(f'{output_path}/{file_name}.parquet', index=False)
        print(f'The data for {file_name} has been sucessfully exported')
    else:
        print('Wrong output format, select between "csv" or "parquet"')

def extract_data_catalog_tables(workspaces_ids:list, output_path:str, output_format: str):
    all_reports = get_all_reports(workspaces_ids)
    df_reports = pd.json_normalize(all_reports, record_path='response', meta='workspace_id')
    export_data(df_reports, 'pbi_reports_info', output_path, output_format)

    all_datasets = get_all_datasets(workspaces_ids)
    df_datasets = pd.json_normalize(all_datasets, record_path='response', meta='workspace_id')
    export_data(df_datasets, 'pbi_datasets_info', output_path, output_format)

    query_list = os.listdir('dax_queries')
    for q in query_list:
        file_name = q.split(".")[0]
        all_dax_info = get_all_datasets_info(workspaces_ids, q)
        df_dax_info = pd.json_normalize(all_dax_info, record_path='response', meta=['workspace_id', 'dataset_id'])
        export_data(df_dax_info, f'pbi_{file_name}', output_path, output_format)

if __name__ == '__main__':
    workspaces_ids = os.getenv('PBI_WORKSPACES_IDS').split(",")
    output_path = os.getenv('OUTPUT_DIR')

    extract_data_catalog_tables(workspaces_ids, output_path, 'parquet')