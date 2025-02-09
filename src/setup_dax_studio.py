import os
import logging
import requests
import zipfile
from io import BytesIO


logging.basicConfig(
    level=logging.INFO,
    format='{asctime} - {levelname} - {message}',
    style='{',
    datefmt='%Y-%m-%d %H:%M'
)


def check_dax_studio_setup():
    tool_dir = os.path.join(os.getcwd(), 'tools')
    tool_path = os.path.join(tool_dir, 'dax_studio' ,'dscmd.exe')
    
    logging.info('Checking if Dax Studio is ready...')
    
    if os.path.exists(tool_path):
        return logging.info('Check completed. Dax Studio is ready!')
    else:

        logging.warning("DAX Studio not found. Installing requirements...")

        download_url = 'https://github.com/DaxStudio/DaxStudio/releases/download/v3.2.1/DaxStudio_3_2_1_portable.zip'
    
        try:
            response = requests.get(download_url, stream=True)
            response.raise_for_status()

            with zipfile.ZipFile(BytesIO(response.content), 'r') as zip_content:
                extract_path = os.path.join(tool_dir, "dax_studio")
                zip_content.extractall(extract_path)

            return logging.info("Downloaded completed. Dax Studio is ready!")
        
        except requests.RequestException as e:
            logging.error(f"Failed to download DAX Studio: {e}")


if __name__ == '__main__':
    check_dax_studio_setup()