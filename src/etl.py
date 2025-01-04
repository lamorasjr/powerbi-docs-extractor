import os
import pandas as pd
from powerbi_api_functions import get_datasets_in_workspace #, get_datasets_dax_info

PBI_WORKSPACE_ID = os.getenv('PBI_WORKSPACE_ID')
PBI_ACCESS_TOKEN = os.getenv('PBI_ACCESS_TOKEN')

# ETL function for pbi datasets
def etl_pbi_datasets():
    data = get_datasets_in_workspace(access_token=PBI_ACCESS_TOKEN, workspace_id=PBI_WORKSPACE_ID)
    df = pd.json_normalize(data)
    df_etl = df[['id', 'name', 'webUrl', 'createdDate']]
    df_etl = df_etl.rename(columns={'id':'DATASET_ID',
                                    'name':'DATASET_NAME',
                                    'webUrl':'WEB_URL',
                                    'createdDate':'CREATED_AT'})
    df_etl['CREATED_AT'] = pd.to_datetime(df_etl['CREATED_AT']).dt.date
    df_etl['SYS_TIMESTAMP'] = pd.to_datetime(pd.Timestamp('now'))
    return df_etl

# ETL function for pbi dataset tables
# ETL function for pbi dataset columns
# ETL function for pbi dataset measures
# ETL function for pbi dataset relationships

if __name__ == '__main__':
    df_datasets = etl_pbi_datasets()
    df_datasets.to_csv('raw_data/pbi_datasets_raw.csv', index=False, sep=';', encoding='utf-8')
    print('Datasets exported successfully')