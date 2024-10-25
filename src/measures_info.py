import os
import requests
import pandas as pd

PBI_API_TOKEN = os.getenv('PBI_API_TOKEN')
PBI_WORKSPACE_ID = os.getenv('PBI_WORKSPACE_ID')
BASE_URL = 'https://api.powerbi.com/v1.0/myorg/'

dax_query = 'EVALUATE INFO.MEASURES()'

api_headers = { 
    'Authorization' : f'Bearer {PBI_API_TOKEN}',
    'Content-Type' :  'application/json'
}
api_body = {
    "queries": [ 
        {
            "query": f"{dax_query}"
        }
    ],
    "serializerSettings": { 
        "includeNulls": "true"
    }
}

def extract_datasets_id(file_path):
    df = pd.read_csv(file_path, sep=';', encoding='utf-8')
    data_list = [  i for i in df['id'] ]
    return data_list

def get_pbi_measures(dataset_id):
    endpoint = f'datasets/{dataset_id}/executeQueries'
    response = requests.post(BASE_URL + endpoint, headers=api_headers,json=api_body)
    data = response.json()
    return data

def load_measures_df(datasets_list):
    df_list = []
    for id in datasets_list:
        measures_data = get_pbi_measures(id)
        df_raw = pd.json_normalize(measures_data, record_path=['results', 'tables', 'rows'])
        df_raw['[DatasetId]'] = id
        df_list.append(df_raw)
    df_total = pd.concat(df_list, ignore_index=True)
    return df_total

def pipeline_measures_info(file_path):
    datasets_list = extract_datasets_id(file_path)
    df = load_measures_df(datasets_list)
    df.to_csv('data/measures_info.csv', index=False, sep=';')
    print('The measures info pipeline has been completed successfully.')