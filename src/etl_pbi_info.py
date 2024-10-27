import os
import requests
import pandas as pd
from etl_pbi import get_datasets_ids

PBI_API_TOKEN = os.getenv('PBI_API_TOKEN')

def get_pbi_info(api_token: str, dataset_id:str, dax_query:str):
    url = f'https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/executeQueries'
    headers = { 
        'Authorization' : f'Bearer {api_token}',
        'Content-type' : 'application/json'
    }
    body = {
        'queries': [{'query': f'{dax_query}'}],
        'serializerSettings': {'includeNulls': 'true'}
    }
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    return data

def load_df_info(dataset_id:str, dax_query:str):
    data = get_pbi_info(PBI_API_TOKEN, dataset_id, dax_query)
    df = pd.json_normalize(data, record_path=['results', 'tables', 'rows'])
    return df

def etl_pbi_info(dataset_ids:list, dax_query:str, file_name:str):
    df_list = []
    for id in dataset_ids:
        df = load_df_info(id, dax_query)
        df_list.append(df)
    df_total = pd.concat(df_list, ignore_index=True)
    df_total.to_csv(f'data/{file_name}.csv', index=False, sep=';')
    print(f"the {file_name}.csv file has been extracted succesfully.")


# Use case example:
if __name__ == "__main__":
    dataset_ids = get_datasets_ids()
    dax_query = 'EVALUATE INFO.MEASURES()'
    file_name = 'measures_info'

    etl_pbi_info(dataset_ids, dax_query, file_name)
