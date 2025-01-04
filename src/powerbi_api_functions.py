import os
import requests
import pandas as pd

# Extract list of datasets contained in the Power BI Workspace
def get_datasets_in_workspace(access_token:str, workspace_id:str):
    """
    Function to extract all datasets contained in a given Power BI workspace.
    """
    url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets'
    headers = { 'Authorization' : f'Bearer {access_token}'}

    try:
        response = requests.get(url, headers=headers)

        data = response.json()
        df = pd.json_normalize(data, record_path=['value'])
        df['Semantic Model Id'] = workspace_id
        return df
    
    except Exception as err:
        print(f'Non-success status code: {err}')


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

    try:
        response = requests.post(url, headers=headers, json=body)

        data = response.json()
        df = pd.json_normalize(data, record_path=['results', 'tables', 'rows'])
        return df
    
    except Exception as err :
        print(f'Non-success status code: {err}')


if __name__ == '__main__':
    pbi_workspace_id = os.getenv('PBI_WORKSPACE_ID')
    pbi_access_token = os.getenv('PBI_ACCESS_TOKEN')
    pbi_sample_dataset_id = os.getenv('SAMPLE_DATASET_ID')
    pbi_sample_dax_query = 'EVALUATE INFO.TABLES()'

    df_datasets = get_datasets_in_workspace(access_token=pbi_access_token, workspace_id=pbi_workspace_id)
    # print(df_datasets.head())
    # df_datasets.to_csv('data/pbi_datasets.csv', index=False)
    print('Datasets successfully extracted.')
    

    df_dataset_tables = get_datasets_dax_info(access_token=pbi_access_token, 
                                      workspace_id=pbi_workspace_id, 
                                      dataset_id = pbi_sample_dataset_id, 
                                      dax_query=pbi_sample_dax_query)
    # print(df_dataset_tables.head())
    # df_dataset_tables.to_csv('data/pbi_dataset_tables.csv', index=False)
    print('Dataset tables successfully extracted.')