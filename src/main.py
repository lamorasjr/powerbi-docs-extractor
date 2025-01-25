import os
import logging
from azure_app_token import get_access_token
from sharepoint_loader import upload_to_sharepoint
from extractor_powerbi_api import (
    extract_workspaces,
    extract_reports,
    extract_reports_pages,
    extract_datasets,
    export_csv_or_parquet,
    extract_datasets_info_queries
)

logging.basicConfig(
    level=logging.INFO,
    format='{asctime} - {levelname} - {message}',
    style='{',
    datefmt='%Y-%m-%d %H:%M'
)


def etl_powerbi_data(access_token:str, workspaces_ids:list, output_format:str, output_path):
    try:
        logging.info('Starting Power BI data extraction process:')

        workspaces = extract_workspaces(access_token, workspaces_ids)
        export_csv_or_parquet(workspaces, 'workspaces', output_format, output_path)

        reports = extract_reports(access_token, workspaces_ids)
        export_csv_or_parquet(reports, 'reports', output_format, output_path)

        reports_pages = extract_reports_pages(access_token, workspaces_ids)
        export_csv_or_parquet(reports_pages, 'reports_pages', output_format, output_path)

        datasets = extract_datasets(access_token, workspaces_ids)
        export_csv_or_parquet(datasets, 'datasets', output_format, output_path)

        # dax_queries_dir = os.path.join(os.getcwd(), 'src', 'dax_queries')

        # for file in os.listdir(dax_queries_dir):
        #     if file.endswith('.txt'):
        #         file_name = file.split(".")[0] 
        #         file_dir = os.path.join(dax_queries_dir, file)

        #         with open(file_dir, 'r') as file:
        #             dax_query = str(file.read())
                
        #         df_query_temp = extract_datasets_info_queries(access_token, workspaces_ids, dax_query)
        #         export_csv_or_parquet(df_query_temp, file_name, output_format, output_path)
        
        logging.info('Power BI successfully completed.')

    except KeyError as e:
        logging.error(f'ETL error: {e}')


def load_to_sharepoint(access_token:str, sharepoint_site:str, sharepoint_folder:str, input_path:str):
    try:
        logging.info('Starting upload to Sharepoint process:')

        for file_name in os.listdir(input_path):
            if file_name.endswith(('.csv', '.parquet')):
                file_path = os.path.join(input_path, file_name)
                upload_to_sharepoint(access_token, sharepoint_site, sharepoint_folder, file_path)
        
        logging.info('Upload to Sharepoint completed.')
    
    except ValueError as e:
        logging.error(f'Upload error: {e}')


def main():
    try:
        logging.info("Starting ETL process.")

        tenant_id = os.getenv('AZURE_APP_TENANT_ID')
        client_id = os.getenv('AZURE_APP_CLIENT_ID')
        client_secret = os.getenv('AZURE_APP_CLIENT_SECRET')
        workspaces_ids = [ i.strip() for i in os.getenv('PBI_WORKSPACES_IDS').split(",") ]
        output_format = os.getenv('OUTPUT_FILE_FORMAT')
        sharepoint_site = os.getenv('SHAREPOINT_URL')
        sharepoint_folder = os.getenv('SHAREPOINT_FOLDER')
            
        logging.info("Check enviroments variables inputs.")

        if None in [tenant_id, client_id, client_secret, workspaces_ids, output_format, sharepoint_site, sharepoint_folder]:
            raise ValueError('One or more required variables are missing, review .env file.')
            
        if output_format not in ['csv', 'parquet']:
            raise ValueError('Wrong input for output format, must be "csv" or "parquet", review .env file.')


        logging.info("Request API access tokens.")

        pbi_access_token = get_access_token(tenant_id, client_id, client_secret, scope_app='powerbi')
        sp_access_token = get_access_token(tenant_id, client_id, client_secret, scope_app='sharepoint')

        temp_dir = os.path.join(os.getcwd(), 'temp')

        etl_powerbi_data(pbi_access_token, workspaces_ids, output_format, temp_dir)
        load_to_sharepoint(sp_access_token, sharepoint_site, sharepoint_folder, temp_dir)

        logging.info("ETL process succesfully completed.")

    except Exception as e:
        logging.error(f"Critical error: {e}", exc_info=True)

if __name__ == '__main__':
    main()

    