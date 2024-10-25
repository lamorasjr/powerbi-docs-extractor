import os
import requests
import pandas as pd

PBI_API_TOKEN = os.getenv('PBI_API_TOKEN')
PBI_WORKSPACE_ID = os.getenv('PBI_WORKSPACE_ID')
BASE_URL = 'https://api.powerbi.com/v1.0/myorg/'
ENDPOINT = f'groups/{PBI_WORKSPACE_ID}/datasets'

api_headers = { 'Authorization' : f'Bearer {PBI_API_TOKEN}'}
api_url = BASE_URL + ENDPOINT

def get_api_data(url, headers):
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def pipeline_datasets():
    datasets = get_api_data(api_url, api_headers)
    df = pd.json_normalize(datasets, record_path=['value'])
    df.to_csv('data/datasets.csv', index=False, sep=';')
    print('The datasets pipeline has been completed successfully.')