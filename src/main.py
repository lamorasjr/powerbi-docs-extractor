import os
import logging
from dotenv import load_dotenv
from setup_dax_studio import check_dax_studio_setup
from sharepoint_loader import load_to_sharepoint
from extractor_powerbi import (
    extract_workspaces,
    extract_reports,
    extract_reports_pages,
    extract_datasets,
    dscmd_extract_datasets_info
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

        # Check if Dax Studio is setup
        check_dax_studio_setup()

        # Load .env
        load_dotenv()
        
        workspaces_ids = [ i.strip() for i in os.getenv('PBI_WORKSPACES_IDS').split(",") ]
        sharepoint_site = os.getenv('SHAREPOINT_SITE')
        sharepoint_folder = os.getenv('SHAREPOINT_FOLDER')
            
        # Check if all required inputs were given
        logging.info("Check enviroment variables.")

        if None in [workspaces_ids, sharepoint_site, sharepoint_folder]:
            raise ValueError('One or more required variables are missing, review .env file.')

        # Request api tokens
        logging.info("Request API access tokens.")

        # Run ETL process
        logging.info("Start ETL process...")
        
        logging.info("Extracting workspaces...")
        df_workspaces = extract_workspaces(workspaces_ids)
        load_to_sharepoint(sharepoint_site, sharepoint_folder, df_workspaces, 'workspaces.csv')

        logging.info("Extracting reports...")
        df_reports = extract_reports(workspaces_ids)
        load_to_sharepoint(sharepoint_site, sharepoint_folder, df_reports, 'reports.csv')
        
        logging.info("Extracting reports_pages...")
        df_reports_pages = extract_reports_pages(workspaces_ids)
        load_to_sharepoint(sharepoint_site, sharepoint_folder, df_reports_pages, 'reports_pages.csv')

        logging.info("Extracting datasets...")
        df_datasets = extract_datasets(workspaces_ids)
        load_to_sharepoint(sharepoint_site, sharepoint_folder, df_datasets, 'datasets.csv')

        dax_queries_dir = os.path.join(os.getcwd(), 'src', 'dax_queries')
        
        for file in os.listdir(dax_queries_dir):
            
            if file.endswith('.txt'):
                file_name = file.split(".")[0] 
                file_dir = os.path.join(dax_queries_dir, file)

            logging.info(f"Extracting {file_name}...")
            df_query = dscmd_extract_datasets_info(workspaces_ids, file_dir)
            load_to_sharepoint(sharepoint_site, sharepoint_folder, df_query, f'{file_name}.csv')

        logging.info("ETL process completed succesfully.")

    except Exception as e:
        logging.error(f"Critical error: {e}", exc_info=True)

if __name__ == '__main__':
    main()