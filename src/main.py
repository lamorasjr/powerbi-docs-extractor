import os
import logging
from azure_app_token import get_access_token
from sharepoint_loader import upload_to_sharepoint
from extractor_powerbi_api import etl_powerbi_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    try:
        logging.info("Loading and checking enviroments variables.")

        tenant_id = os.getenv('AZURE_APP_TENANT_ID')
        client_id = os.getenv('AZURE_APP_CLIENT_ID')
        client_secret = os.getenv('AZURE_APP_CLIENT_SECRET')
        workspaces_ids = [ i.strip() for i in os.getenv('PBI_WORKSPACES_IDS').split(",") ]
        output_format = os.getenv('OUTPUT_FILE_FORMAT')
        sharepoint_site = os.getenv('SHAREPOINT_URL')
        sharepoint_folder = os.getenv('SHAREPOINT_FOLDER')
            
        if None in [tenant_id, client_id, client_secret, workspaces_ids, output_format, sharepoint_site, sharepoint_folder]:
            raise ValueError('One or more required variables are missing, review .env file.')
            
        if output_format not in ['csv', 'parquet']:
            raise ValueError('Wrong input for output format, must be "csv" or "parquet", review .env file.')


        logging.info("Requesting API access tokens API endpoints.")
        pbi_access_token = get_access_token(tenant_id, client_id, client_secret, scope_app='powerbi')
        sp_access_token = get_access_token(tenant_id, client_id, client_secret, scope_app='sharepoint')


        logging.info("Starting ETL process...")

        temp_dir = os.path.join(os.getcwd(), 'temp')

        etl_powerbi_data(pbi_access_token, workspaces_ids, output_format, temp_dir)

        logging.info("Power BI data extraction completed.")


        logging.info("Initiating files upload to Sharepoint...")

        for file_name in os.listdir(temp_dir):
            if file_name.endswith(('.csv', '.parquet')):
                file_path = os.path.join(temp_dir, file_name)
                upload_to_sharepoint(sp_access_token, sharepoint_site, sharepoint_folder, file_path)

        logging.info("ETL process succesfully completed.")
    
    except Exception as e:
        logging.error(f"Critical error: {e}", exc_info=True)

if __name__ == '__main__':
    main()