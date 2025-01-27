import os
import requests
import pandas as pd
from io import BytesIO

def get_sharepoint_site_id(access_token:str, site_name:str)->str:
    url = f'https://graph.microsoft.com/v1.0/sites?search={site_name}'
    headers = {
        'Authorization' : f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        site_id = response.json()['value'][0]['id']
        return site_id
    else:
        raise Exception(f'Error to get Sharepoint site id: {response.status_code} - {response.text}')
    

def get_sharepoint_drive_id(access_token:str, site_id:str)->str:
    url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        drive_id = response.json()['value'][0]['id']
        return drive_id
    else:
        raise Exception(f'Error to get Sharepoint drive id: {response.status_code} - {response.text}')
    

def load_to_sharepoint(access_token:str, sharepoint_site:str, sharepoint_folder:str, input_df:pd.DataFrame, file_name:str):
    
    site_id = get_sharepoint_site_id(access_token, os.path.basename(sharepoint_site))
    drive_id = get_sharepoint_drive_id(access_token, site_id)

    csv_buffer = BytesIO()
    input_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    url = f'https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{sharepoint_folder}/{file_name}:/content'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/octet-stream',
    }

    response = requests.put(url, headers=headers, data=csv_buffer)

    if response.status_code in [200, 201]:
        print(f'- Upload succeeded: {file_name} - status code: {response.status_code}.')
    else:
        raise Exception(f'- Upload failed: {response.status_code} - {response.text}')