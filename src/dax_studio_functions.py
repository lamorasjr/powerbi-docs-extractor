import os
import logging
import requests
import zipfile
import subprocess
import pandas as pd
from io import BytesIO
from urllib.parse import quote


logging.basicConfig(
    level=logging.INFO,
    format='{asctime} - {levelname} - {message}',
    style='{',
    datefmt='%Y-%m-%d %H:%M'
)


def check_dax_studio_setup()->str:

    tool_dir = os.path.join(os.getcwd(), 'tools')
    tool_path = os.path.join(tool_dir, 'dax_studio' ,'dscmd.exe')
    
    logging.info('Check if Dax Studio setup is ready ...')
    
    if os.path.exists(tool_path):
        
        logging.info('Success - Required setup is ready!')
        
        return tool_path

    logging.warning("DAX Studio not found. Installing requirements...")

    download_url = 'https://github.com/DaxStudio/DaxStudio/releases/download/v3.2.1/DaxStudio_3_2_1_portable.zip'
    
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        with zipfile.ZipFile(BytesIO(response.content), 'r') as zip_content:
            extract_path = os.path.join(tool_dir, "dax_studio")
            zip_content.extractall(extract_path)

        logging.info("Installation completed successfully.")
        return tool_path
    
    except requests.RequestException as e:
        logging.error(f"Failed to download DAX Studio: {e}")


def execute_query_dscmd(tenant_id:str, client_id:str, client_secret:str, workspace_name, dataset_name, query_file)->pd.DataFrame:

    DSCMD = check_dax_studio_setup()
    output_file = os.path.join(os.getcwd(), "tools", "temp.csv")

    prompt = [
        DSCMD,
        "csv", output_file,
        "-s", f"powerbi://api.powerbi.com/v1.0/myorg/{quote(workspace_name)}",
        "-d", dataset_name,
        "-u", f"app:{client_id}@{tenant_id}", 
        "-p", client_secret,
        "-f", query_file,
        "-t", "UTF8CSV"
    ]

    try:
        result = subprocess.run(prompt, capture_output=True, text=True, check=True)

        logging.info('Json exported successfully.')

    except subprocess.CalledProcessError as e:
        logging.error(f'Command failed: {e.stderr or e.stdout}')

    df = pd.read_csv(output_file, encoding='utf-8', sep=';')

    os.remove(output_file)

    return df