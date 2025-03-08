import os
import requests
import zipfile
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

def setup_dax_studio():
    """
    Checks if Dax Studio CMD (Portable) is avaliable in the local directory, otherwise it downloads from the source Github.
    """
    logging.info("Checking requirements for Dax Studio CMD (Portable)...")

    tool_dir = os.path.join(os.getcwd(), "tools")
    os.makedirs(tool_dir, exist_ok=True)
    
    tool_path = os.path.join(tool_dir, "dax_studio" ,"dscmd.exe")

    if os.path.exists(tool_path):
        logging.info("Dax Studio CMD (Portable) setup is ready!")
    else:
        logging.warning("Dax Studio CMD (Portable) setup is not ready. Downloading it from the source...")
        
        tool_url = "https://github.com/DaxStudio/DaxStudio/releases/download/v3.2.1/DaxStudio_3_2_1_portable.zip"

        response = requests.get(tool_url, stream=True)
        
        if response.status_code == 200:
            with zipfile.ZipFile(BytesIO(response.content), "r") as zip_content:
                extract_path = os.path.join(tool_dir, "dax_studio")
                zip_content.extractall(extract_path)

            logging.info("Download and setup completed.")
            logging.info("Dax Studio CMD (Portable) setup is ready!")
        
        else:
            raise requests.RequestException(f"Failed to download DAX Studio: {response.status_code} - {response.text}")
        
if __name__ == "__main__":
    setup_dax_studio()