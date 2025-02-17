import os
import requests
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

def get_sharepoint_token():
    """
    Generate an access token for sharepoint
    """
    TENANT_ID = os.getenv('PBI_TENANT_ID')
    CLIENT_ID = os.getenv('PBI_CLIENT_ID')
    CLIENT_SECRET = os.getenv('PBI_CLIENT_SECRET')

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
        raise KeyError(f'Failed to obtain token: {response.status_code} - {response.text}')


def get_sharepoint_site_id(site_name):
    """
    For a given sharepoint site, returns the site id.
    """
    access_token = get_sharepoint_token()

    url = f'https://graph.microsoft.com/v1.0/sites?search={site_name}'
    
    headers = {
        'Authorization' : f'Bearer {access_token}'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        site_id = response.json()['value'][0]['id']
        return site_id
    
    else:
        raise KeyError(f'Error to get Sharepoint Site Id: {response.status_code} - {response.text}')
    

def get_sharepoint_drive_id(site_id):
    """
    For a given sharepoint site id, returns the drive id.
    """
    access_token = get_sharepoint_token()

    url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives'
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        drive_id = response.json()['value'][0]['id']
        return drive_id
    
    else:
        raise KeyError(f'Error to get Sharepoint Drive Id: {response.status_code} - {response.text}')
    

def load_to_sharepoint(sharepoint_site, sharepoint_folder, input_df:pd.DataFrame, file_name):
    """
    Convert and upload a Pandas DataFrame in a given Sharepoint Site and Folder.
    """
    access_token = get_sharepoint_token()

    site_id = get_sharepoint_site_id(os.path.basename(sharepoint_site))

    drive_id = get_sharepoint_drive_id(site_id)

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
        print(f'Sharepoint: Success to upload "{file_name}". Status code: {response.status_code}.')
    else:
        raise requests.HTTPError(f'Sharepoint: Failed to "{file_name}". Status code: {response.status_code} - {response.text}.')