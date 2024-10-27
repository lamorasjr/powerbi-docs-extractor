import os
import requests
import pandas as pd

def get_pbi_object_in_group(api_endpoint:str):
    PBI_API_TOKEN = os.getenv('PBI_API_TOKEN')
    PBI_WORKSPACE_ID = os.getenv('PBI_WORKSPACE_ID')

    url = f'https://api.powerbi.com/v1.0/myorg/groups/{PBI_WORKSPACE_ID}/{api_endpoint}'
    headers = { 'Authorization' : f'Bearer {PBI_API_TOKEN}'}
    response = requests.get(url, headers=headers)

    data = response.json()
    df = pd.json_normalize(data, record_path=['value'])
    df['Semantic Model Id'] = PBI_WORKSPACE_ID
    return df

def get_datasets_ids():
    df = get_pbi_object_in_group('datasets')
    return df['id']

# Use case example:
if __name__ == '__main__':
    dataset_list = get_datasets_ids()
    print(dataset_list)