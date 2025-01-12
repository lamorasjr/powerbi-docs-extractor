import os
import pandas as pd
from extract_powerbi_api import get_all_reports, get_all_datasets, get_all_datasets_info

def extract_powerbi_data_catalog_info():
    workspace_ids = os.getenv('PBI_WORKSPACES_IDS').split(",")

    all_reports = get_all_reports(workspace_ids)
    df_reports = pd.json_normalize(all_reports, record_path='response', meta='workspace_id')
    df_reports.to_csv('data/pbi_reports_info.csv', index=False, sep=';', encoding='utf-8')
    print('Power BI reports info has been sucessefully exported')

    all_datasets = get_all_datasets(workspace_ids)
    df_datasets = pd.json_normalize(all_datasets, record_path='response', meta='workspace_id')
    df_datasets.to_csv('data/pbi_datasets_info.csv', index=False, sep=';', encoding='utf-8')
    print('Power BI datasets info has been sucessefully exported')

    all_tables = get_all_datasets_info(workspace_ids, 'tables_info.txt')
    df_tables = pd.json_normalize(all_tables ,record_path='response', meta=['workspace_id', 'dataset_id'])
    df_tables.to_csv('data/pbi_tables_info.csv', index=False, sep=';', encoding='utf-8')
    print('Power BI tables info has been sucessefully exported')

if __name__ == '__main__':
    extract_powerbi_data_catalog_info()