import os
# import pandas as pd
from powerbi_api_functions import get_datasets_in_workspace #, get_datasets_dax_info

PBI_WORKSPACE_ID = os.getenv('PBI_WORKSPACE_ID')
PBI_ACCESS_TOKEN = os.getenv('PBI_ACCESS_TOKEN')

# ETL function for pbi datasets
def etl_pbi_datasets():
    df = get_datasets_in_workspace(access_token=PBI_ACCESS_TOKEN, workspace_id=PBI_WORKSPACE_ID)
    return df

# ETL function for pbi dataset tables
# ETL function for pbi dataset columns
# ETL function for pbi dataset measures
# ETL function for pbi dataset relationships

if __name__ == '__main__':
    df_datasets = etl_pbi_datasets()
    print(df_datasets.head())