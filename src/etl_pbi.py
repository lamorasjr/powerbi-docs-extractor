import os
import requests
import pandas as pd

PBI_API_TOKEN = os.getenv('PBI_API_TOKEN')
PBI_WORKSPACE_ID = os.getenv('PBI_WORKSPACE_ID')

def get_pbi_in_group(api_token: str, workspace_id: str, api_endpoint:str):
    url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/{api_endpoint}'
    headers = { 'Authorization' : f'Bearer {api_token}'}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def export_pbi_in_group(endpoint):
    data = get_pbi_in_group(PBI_API_TOKEN, PBI_WORKSPACE_ID, endpoint)
    df = pd.json_normalize(data, record_path=['value'])
    df.to_csv(f'data/{endpoint}.csv', index=False, sep=';')
    print(f"the {endpoint}.csv file has been extracted succesfully.")

def get_datasets_ids():
    data = get_pbi_in_group(PBI_API_TOKEN, PBI_WORKSPACE_ID, "datasets")
    df = pd.json_normalize(data, record_path=['value'])
    return df['id']

# Use case example:
if __name__ == "__main__":
    pbi_list = ["datasets", "dataflows", "dashboards", "reports"]

    for i in pbi_list:
        export_pbi_in_group(i)

    dataset_list = get_datasets_ids()
    print(dataset_list)