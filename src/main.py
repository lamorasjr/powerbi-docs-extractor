import os
import pandas as pd
from powerbi_rest_api import get_auth_token, get_workspaces_info, get_workspace_reports, get_workspace_datasets, execute_dataset_query
from utils import load_data

TENANT_ID = os.getenv('PBI_TENANT_ID')
CLIENT_ID = os.getenv('PBI_CLIENT_ID')
CLIENT_SECRET = os.getenv('PBI_CLIENT_SECRET')
WORKSPACES_IDS = os.getenv('PBI_WORKSPACES_IDS').split(",")
output_path = 'data/'

access_token = get_auth_token(TENANT_ID, CLIENT_ID, CLIENT_SECRET)

def etl_pbi_workspaces(access_token:str, workspaces_list:str, output_path:str, output_format:str):
    all_data = [] 
    for ws_id in WORKSPACES_IDS:
        data = get_workspaces_info(access_token, ws_id)
        all_data.append(data)
    df = pd.json_normalize(all_data)
    load_data(df, 'pbi_workspaces_info', output_path, output_format)


def etl_pbi_reports():
    pass


def etl_pbi_datasets():
    pass


def etl_pbi_datasets_info():
    pass


if __name__ == '__main__':
    etl_pbi_workspaces(access_token, WORKSPACES_IDS, output_path, 'csv')

# pbi_reports = get_workspace_reports(access_token, WORKSPACES_IDS)
# # print(pbi_reports)

# pbi_datasets = get_workspace_datasets(access_token, WORKSPACES_IDS)
# # print(pbi_datasets)

# dataset_id = pbi_datasets['response'][0]['id']
# dax_query = 'EVALUATE INFO.TABLES()'

# pbi_tables = execute_dataset_query(access_token, WORKSPACES_IDS, dataset_id, dax_query)
# print(pbi_tables)






# def extract_data_catalog_tables(workspaces_ids:list, output_path:str, output_format: str):
#     all_reports = get_all_reports(workspaces_ids)
#     df_reports = pd.json_normalize(all_reports, record_path='response', meta='workspace_id')
#     export_data(df_reports, 'pbi_reports_info', output_path, output_format)

#     all_datasets = get_all_datasets(workspaces_ids)
#     df_datasets = pd.json_normalize(all_datasets, record_path='response', meta='workspace_id')
#     export_data(df_datasets, 'pbi_datasets_info', output_path, output_format)

#     query_list = os.listdir('dax_queries')
#     for q in query_list:
#         file_name = q.split(".")[0]
#         all_dax_info = get_all_datasets_info(workspaces_ids, q)
#         df_dax_info = pd.json_normalize(all_dax_info, record_path='response', meta=['workspace_id', 'dataset_id'])
#         export_data(df_dax_info, f'pbi_{file_name}', output_path, output_format)

# if __name__ == '__main__':
#     workspaces_ids = os.getenv('PBI_WORKSPACES_IDS').split(",")
#     output_path = os.getenv('OUTPUT_DIR')

#     extract_data_catalog_tables(workspaces_ids, output_path, 'parquet')