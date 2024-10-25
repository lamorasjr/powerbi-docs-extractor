import os
import requests
import pandas as pd

PBI_API_TOKEN = os.getenv('PBI_API_TOKEN')
PBI_WORKSPACE_ID = os.getenv('PBI_WORKSPACE_ID')
BASE_URL = 'https://api.powerbi.com/v1.0/myorg/'
ENDPOINT = f'groups/{PBI_WORKSPACE_ID}/datasets'

api_headers = {
        'Authorization' : f'Bearer {PBI_API_TOKEN}'
    }

api_url = BASE_URL + ENDPOINT

def get_api_data(url, headers):
    response = requests.get(url, headers=headers)
    json_data = response.json()
    data = json_data['value']
    return data

def load_to_df(data):
    df = pd.DataFrame(data)
    return df

def export_csv(df):
    df.to_csv('data/datasets.csv', index=False)


def pipeline_datasets():
    datasets = get_api_data(api_url, api_headers)
    df = load_to_df(datasets)
    export_csv(df)
    print('The datasets pipeline is successfully completed.')