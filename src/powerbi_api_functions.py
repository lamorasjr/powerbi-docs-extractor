import os
import requests

PBI_WORKSPACE_ID = os.getenv('PBI_WORKSPACE_ID')
PBI_ACCESS_TOKEN = os.getenv('PBI_ACCESS_TOKEN')

# Extract list of datasets contained in the Power BI Workspace
def get_datasets_in_workspace():
    """
    Function to extract all datasets in the Power BI workspace set in the env.
    """
    url = f'https://api.powerbi.com/v1.0/myorg/groups/{PBI_WORKSPACE_ID}/datasets'
    headers = { 'Authorization' : f'Bearer {PBI_ACCESS_TOKEN}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        data = response_json['value']
        return data
    else:
        raise Exception(f'Non-success status code: {response.status_code}')


def get_datasets_dax_info(dataset_id:str, dax_query:str):
    """
    Function to execute a given DAX query into a given Power BI dataset in a specific workspace.
    """
    url = f'https://api.powerbi.com/v1.0/myorg/groups/{PBI_WORKSPACE_ID}/datasets/{dataset_id}/executeQueries'

    headers = { 
        'Authorization' : f'Bearer {PBI_ACCESS_TOKEN}',
        'Content-type' : 'application/json'
    }

    body = {
        'queries': [{'query': f'{dax_query}'}],
        'serializerSettings': {'includeNulls': 'true'}
    }

    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code == 200:
        response_json = response.json()
        data = response_json['results'][0]['tables'][0]['rows']
        return data
    else:
        raise Exception(f'Non-sucess status code: {response.status_code}')
        


if __name__ == '__main__':
    test_dax_query = 'EVALUATE INFO.TABLES()'

    pbi_datasets = get_datasets_in_workspace()
    # print(pbi_datasets)

    test_dataset = pbi_datasets[0]['id']
    pbi_tables = get_datasets_dax_info(dataset_id=test_dataset, dax_query=test_dax_query)
    # print(pbi_tables)