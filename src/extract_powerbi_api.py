import os
import requests

PBI_ACCESS_TOKEN = os.getenv('PBI_ACCESS_TOKEN')

def get_datasets_in_workspace(workspace_id):
    url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets'
    headers = { 'Authorization' : f'Bearer {PBI_ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        data = response_json['value']
        return data
    else:
        raise Exception(f'Non-success status code: {response.status_code} - {response.text}')

def get_reports_in_workspace(workspace_id):
    url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports'
    headers = { 'Authorization' : f'Bearer {PBI_ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        data = response_json['value']
        return data
    else:
        raise Exception(f'Non-success status code: {response.status_code} - {response.text}')

def excute_dax_query(workspace_id:str, dataset_id:str, dax_query:str):
    url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/executeQueries'
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
        raise Exception(f'Non-sucess status code: {response.status_code} - {response.text}')
    
def get_all_reports(workspace_list:list):
    all_reports = []
    for ws_id in workspace_list:
        pbi_reports = { 
            'workspace_id' : ws_id,
            'response' : get_reports_in_workspace(workspace_id=ws_id)
        }
        all_reports.append(pbi_reports)
    return all_reports

def get_all_datasets(workspace_list:list):
    all_datasets = []
    for ws_id in workspace_list:
        pbi_datasets = { 
            'workspace_id' : ws_id,
            'response' : get_datasets_in_workspace(workspace_id=ws_id)
        }
        all_datasets.append(pbi_datasets)
    return all_datasets

def get_all_datasets_info(workspace_list:list, file_name:str):
    file_path = f'dax_queries/{file_name}'
    
    with open(file_path, 'r') as f:
        dax_query = f.read()
    
    all_dataset_info = []

    for ws_id in workspace_list:
        
        datasets = get_datasets_in_workspace(ws_id)
        
        datasets_ids = [  i['id'] for i in datasets ]
        
        for ds_id in datasets_ids:
        
            response = excute_dax_query(workspace_id=ws_id, dataset_id=ds_id, dax_query=dax_query)

            dataset_info = {
                "workspace_id": ws_id,
                "dataset_id": ds_id,
                "response" : response,
            }

            all_dataset_info.append(dataset_info)
    
    return all_dataset_info