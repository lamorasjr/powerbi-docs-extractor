import os
import requests

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
    

def upload_file(access_token:str, drive_id:str, sharepoint_folder:str, file_path:str):
    
    file_name = os.path.basename(file_path)

    url = f'https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{sharepoint_folder}/{file_name}:/content'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/octet-stream',
    }

    with open(file_path, 'rb') as file_content:
        response = requests.put(url, headers=headers, data=file_content)

    if response.status_code in [200, 201]:
        print(f'[{response.status_code}] File uploaded to Sharepoint successfully: {file_name}')
    else:
        raise Exception(f'File upload to Sharepoint failed: {response.status_code} - {response.text}')
    

def upload_to_sharepoint(access_token:str, sharepoint_url:str, sharepoint_folder:str, file_path:str):
    try:
        site_name = os.path.basename(sharepoint_url)
        site_id = get_sharepoint_site_id(access_token, site_name)
        drive_id = get_sharepoint_drive_id(access_token, site_id)
        return upload_file(access_token, drive_id, sharepoint_folder, file_path)
    except Exception as e:
        print(f'Sharepoint upload error: {e}')