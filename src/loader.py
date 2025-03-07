import os
import requests
import logging
import pandas as pd
from io import BytesIO

logging.basicConfig(
    level=logging.INFO,
    format='{asctime} - {levelname} - {message}',
    style='{',
    datefmt='%Y-%m-%d %H:%M'
)

def export_dataframes_to_excel(file_name, dataframes, sheet_names):
    """
    Exports multiple dataframes to an Excel file, each dataframe on a different sheet.
    """
    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
        for df, sheet_name in zip(dataframes, sheet_names):
            df.to_excel(writer, sheet_name=sheet_name, index=False)


def get_sharepoint_access_token(tenant_id, client_id, client_secret):
    """
    Generate Bearer token for Sharepoint via Microsoft Graph API with service principal.
    """
    url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    response = requests.post(url=url, data=payload)
    if response.status_code == 200:
        response_json = response.json()
        data = response_json['access_token']
        return data
    else:
        raise KeyError(f'Error to get Sharepoint access token: {response.status_code} - {response.text}')
    

def resolve_sharepoint_site_name(access_token, site_name):
    """
    Resolves Sharepoint drive id based on a given site name.
    """

    headers = {
        'Authorization' : f'Bearer {access_token}'
    }
    
    url = f'https://graph.microsoft.com/v1.0/sites?search={site_name}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        site_id = response.json()['value'][0]['id']
        
        url2 = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives'
        
        response2 = requests.get(url2, headers=headers)

        if response2.status_code == 200:
            drive_id = response2.json()['value'][0]['id']
            return drive_id
        
        raise KeyError(f'Error to get Sharepoint Drive Id: {response.status_code} - {response.text}')

    raise KeyError(f'Error to get Sharepoint Site Id: {response.status_code} - {response.text}')


def load_csv_to_sharepoint(access_token, site_url, site_relative_url, file_name, dataframes, sheet_names):
    """
    Convert Pandas DataFrame to binary and upload it as csv to a Sharepoint Folder.
    """
    site_name = os.path.basename(site_url)

    drive_id = resolve_sharepoint_site_name(access_token, site_name)

    file_buffer = BytesIO()
    
    export_dataframes_to_excel(file_buffer, dataframes, sheet_names)
        
    file_buffer.seek(0)

    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{site_relative_url}/{file_name}:/content"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream",
    }

    response = requests.put(url, headers=headers, data=file_buffer)

    if response.status_code in [200, 201]:
        logging.info(f'Sharepoint sucessfully uploaded - file: "{file_name}". Status code: {response.status_code}.')
    else:
        logging.error(f'Sharepoint upload failed - file: "{file_name}". Status code: {response.status_code} - {response.text}.')
        raise requests.HTTPError(f'Sharepoint upload failed - file: "{file_name}". Status code: {response.status_code} - {response.text}.')