import os
import requests
import pandas as pd
import logging
from io import BytesIO
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='{asctime} - {levelname} - {message}',
    style='{',
    datefmt='%Y-%m-%d %H:%M'
)

load_dotenv()

def get_sharepoint_token()->str:
    TENANT_ID = os.getenv('AZURE_APP_TENANT_ID')
    CLIENT_ID = os.getenv('AZURE_APP_CLIENT_ID')
    CLIENT_SECRET = os.getenv('AZURE_APP_CLIENT_SECRET')

    url = f'https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token'

    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'https://graph.microsoft.com/.default'
    }
    response = requests.post(url=url, data=payload)
    if response.status_code == 200:
        response_json = response.json()
        data = response_json['access_token']
        return data
    else:
        raise Exception(f'Failed to obtain token: {response.status_code} - {response.text}')



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
    

def load_to_sharepoint(sharepoint_site:str, sharepoint_folder:str, input_df:pd.DataFrame, file_name:str):
    access_token = get_sharepoint_token()

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
        logging.info(f'Sharepoint upload completed for {file_name}. Status code: {response.status_code}.')
    else:
        raise Exception(f'Sharepoint upload failed for {file_name}. Status code: {response.status_code} - {response.text}.')