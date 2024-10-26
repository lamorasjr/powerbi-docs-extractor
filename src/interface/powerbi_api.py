import os
import requests
import pandas as pd

class PowerBiApi:
    def __init__(self, auth_token: str, workspace_id: str):
        self.api_headers = { 'Authorization' : f'Bearer {auth_token}'}
        self.workspace_id = workspace_id
        self.base_url = 'https://api.powerbi.com/v1.0/'
        self.data = None
        self.df = None

    def get_datasets(self):
        api_endpoint = f'myorg/groups/{self.workspace_id}/datasets'
        response = requests.get(self.base_url + api_endpoint, headers=self.api_headers)
        return response.json()

# Use case example
if __name__ == "__main__":
    PBI_API_TOKEN = os.getenv('PBI_API_TOKEN')
    PBI_WORKSPACE_ID = os.getenv('PBI_WORKSPACE_ID')
    
    pbi_conn = PowerBiApi(PBI_API_TOKEN, PBI_WORKSPACE_ID)
    pbi_datasets = pbi_conn.get_datasets()
    df_dataset = pd.json_normalize(pbi_datasets, record_path=['value'])

    print(df_dataset)