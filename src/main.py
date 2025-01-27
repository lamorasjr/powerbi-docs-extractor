import os
import logging
from dotenv import load_dotenv
from azure_app_token import get_access_token
from sharepoint_loader import load_to_sharepoint
from extractor_powerbi_api import (
    extract_workspaces,
    extract_reports,
    extract_reports_pages,
    extract_datasets
)

logging.basicConfig(
    level=logging.INFO,
    format='{asctime} - {levelname} - {message}',
    style='{',
    datefmt='%Y-%m-%d %H:%M'
)

def main():
    try:
        logging.info("Build enviroment for Power BI Data Catalog Extractor.")

        # Load .env
        load_dotenv()
        
        tenant_id = os.getenv('AZURE_APP_TENANT_ID')
        client_id = os.getenv('AZURE_APP_CLIENT_ID')
        client_secret = os.getenv('AZURE_APP_CLIENT_SECRET')
        workspaces_ids = [ i.strip() for i in os.getenv('PBI_WORKSPACES_IDS').split(",") ]
        sharepoint_site = os.getenv('SHAREPOINT_SITE')
        sharepoint_folder = os.getenv('SHAREPOINT_FOLDER')
            
        # Check if all required inputs were given
        logging.info("Check enviroments variables inputs.")

        if None in [tenant_id, client_id, client_secret, workspaces_ids, sharepoint_site, sharepoint_folder]:
            raise ValueError('One or more required variables are missing, review .env file.')

        # Request api tokens
        logging.info("Request API access tokens.")

        pbi_access_token = get_access_token('powerbi', tenant_id, client_id, client_secret, )
        sp_access_token = get_access_token('sharepoint', tenant_id, client_id, client_secret)

        # Run ETL process
        logging.info("Start ETL process: ")
        
        df_workspaces = extract_workspaces(pbi_access_token, workspaces_ids)
        load_to_sharepoint(sp_access_token, sharepoint_site, sharepoint_folder, df_workspaces, 'workspaces.csv')

        df_reports = extract_reports(pbi_access_token, workspaces_ids)
        load_to_sharepoint(sp_access_token, sharepoint_site, sharepoint_folder, df_reports, 'reports.csv')
        
        df_reports_pages = extract_reports_pages(pbi_access_token, workspaces_ids)
        load_to_sharepoint(sp_access_token, sharepoint_site, sharepoint_folder, df_reports_pages, 'reports_pages.csv')

        df_datasets = extract_datasets(pbi_access_token, workspaces_ids)
        load_to_sharepoint(sp_access_token, sharepoint_site, sharepoint_folder, df_datasets, 'datasets.csv')

        logging.info("ETL process completed succesfully.")

    except Exception as e:
        logging.error(f"Critical error: {e}", exc_info=True)

if __name__ == '__main__':
    main()

    