import os
import requests

# Extract list of datasets contained in the Power BI Workspace
def get_datasets_in_workspace(access_token:str, workspace_id:str):
    """
    Function to extract all datasets contained in a given Power BI workspace.
    """
    url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets'
    headers = { 'Authorization' : f'Bearer {access_token}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        data = response_json['value']
        return data
    else:
        raise Exception(f'Non-success status code: {response.status_code}')


def get_datasets_dax_info(access_token:str, workspace_id:str, dataset_id:str, dax_query:str):
    """
    Function to execute a given DAX query into a given Power BI dataset in a specific workspace.
    """
    url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/executeQueries'

    headers = { 
        'Authorization' : f'Bearer {access_token}',
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
    pbi_workspace_id = os.getenv('PBI_WORKSPACE_ID')
    pbi_access_token = os.getenv('PBI_ACCESS_TOKEN')
    pbi_sample_dataset_id = os.getenv('SAMPLE_DATASET_ID')
    pbi_sample_dax_query = 'EVALUATE INFO.TABLES()'

    pbi_datasets = get_datasets_in_workspace(access_token=pbi_access_token, workspace_id=pbi_workspace_id)
    # print(pbi_datasets)
    

    pbi_tables = get_datasets_dax_info(access_token=pbi_access_token, 
                                      workspace_id=pbi_workspace_id, 
                                      dataset_id = pbi_sample_dataset_id, 
                                      dax_query=pbi_sample_dax_query)
    # print(pbi_tables)