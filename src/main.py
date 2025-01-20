import os
import logging
from microsoft_access_token import get_access_token
from sharepoint_loader import upload_to_sharepoint
from extractor import (
    etl_powerbi_workspaces,
    etl_powerbi_reports,
    etl_powerbi_reports_pages,
    etl_powerbi_datasets,
    etl_datasets_dax_queries
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_config():
    tenant_id = os.getenv('AZURE_APP_TENANT_ID')
    client_id = os.getenv('AZURE_APP_CLIENT_ID')
    client_secret = os.getenv('AZURE_APP_CLIENT_SECRET')
    workspaces_ids = os.getenv('PBI_WORKSPACES_IDS').split(",")
    output_format = os.getenv('OUTPUT_FILE_FORMAT')
    
    if None in [tenant_id, client_id, client_secret, workspaces_ids]:
        raise ValueError('One or more required variables are missing, review .env file.')
        
    if output_format not in ['csv', 'parquet']:
        raise ValueError('Wrong input for output format, must be "csv" or "parquet", review .env file.')
    
    env_vars = {
        'tenant_id': os.getenv('AZURE_APP_TENANT_ID'),
        'client_id': os.getenv('AZURE_APP_CLIENT_ID'),
        'client_secret': os.getenv('AZURE_APP_CLIENT_SECRET'),
        'workspaces_ids': os.getenv('PBI_WORKSPACES_IDS').split(","),
        'output_format': os.getenv('OUTPUT_FILE_FORMAT').lower(),
        'sharepoint_site': os.getenv('SHAREPOINT_URL'),
        'sharepoint_folder': os.getenv('SHAREPOINT_FOLDER'),
        'output_path': 'data/'
    }
    return env_vars


def run_etl_process(access_token:str, workspaces_ids:list, output_path:str, output_format:str):
    logging.info("Starting ETL process...")
    etl_powerbi_workspaces(access_token, workspaces_ids, output_path, output_format)
    etl_powerbi_reports(access_token, workspaces_ids, output_path, output_format)
    etl_powerbi_reports_pages(access_token, workspaces_ids, output_path, output_format)
    etl_powerbi_datasets(access_token, workspaces_ids, output_path, output_format)
    etl_datasets_dax_queries(access_token, workspaces_ids, output_path, output_format)
    logging.info("ETL process completed successfully.")

def upload_files_to_sharepoint(sp_access_token:str, sharepoint_site:str, sharepoint_folder:str, folder_path:str):
    logging.info("Uploading files to SharePoint...")
    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.csv', '.parquet')):
            file_path = os.path.join(folder_path, file_name)
            upload_to_sharepoint(sp_access_token, sharepoint_site, sharepoint_folder, file_path)
            logging.info(f"Uploaded: {file_name}")


def main():
    try:
        # Load and validate configuration
        config = get_config()
        
        # Generate access tokens
        logging.info("Generating Power BI access token...")

        pbi_access_token = get_access_token(config['tenant_id'], 
                                            config['client_id'], 
                                            config['client_secret'],
                                            scope_app='powerbi')
        # Run ETL process
        run_etl_process(pbi_access_token, 
                        config['workspaces_ids'], 
                        config['output_path'], 
                        config['output_format'])
        
        # Generate SharePoint access token
        logging.info("Generating SharePoint access token...")

        sp_access_token = get_access_token(config['tenant_id'],
                                           config['client_id'],
                                           config['client_secret'],
                                           scope_app='sharepoint')
        
        # Upload files to SharePoint
        upload_files_to_sharepoint(sp_access_token,
                                   config['sharepoint_site'],
                                   config['sharepoint_folder'],
                                   os.path.abspath(config['output_path']))

    except ValueError as ve:
        logging.error(f"Configuration error: {ve}")
    except Exception as e:
        logging.error(f"Critical error: {e}", exc_info=True)

    except Exception as e:
        print(f"Critical error: {e}")

if __name__ == '__main__':
    main()