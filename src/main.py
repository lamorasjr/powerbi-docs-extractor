import os
import logging
from dotenv import load_dotenv
from sharepoint_loader import load_to_sharepoint
from functions_dax_studio import  setup_dax_studio, extract_dataset_info
from functions_powerbi_api import (
    extract_workspaces,
    extract_datasets,
    extract_reports,
    extract_reports_pages,
    generate_workspaces_datasets_list
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

        # Check if Dax Studio is setup
        setup_dax_studio()
        
        workspaces_ids = [ i.strip() for i in os.getenv('PBI_WORKSPACES_IDS').split(",") ]
        sharepoint_site = os.getenv('SHAREPOINT_SITE')
        sharepoint_folder = os.getenv('SHAREPOINT_FOLDER')
            
        # Check if all required inputs were given
        logging.info("Check enviroment variables.")

        if None in [workspaces_ids, sharepoint_site, sharepoint_folder]:
            raise ValueError('One or more of the required variables is missing. Review the .env file.')

        # Request api tokens
        logging.info("Request API access tokens.")

        # Run ETL process
        logging.info("Start ETL process...")
        
        output_dir = os.path.join(os.getcwd(), "data")
        os.makedirs(output_dir, exist_ok=True)

        logging.info("Extracting workspaces...")
        df_workspaces = extract_workspaces(workspaces_ids)
        df_workspaces.to_csv(f"{output_dir}/workspace.csv", index=False, encoding="utf-8", sep=";")
        # load_to_sharepoint(sharepoint_site, sharepoint_folder, df_workspaces, 'workspaces.csv')

        logging.info("Extracting datasets...")
        df_datasets = extract_datasets(workspaces_ids)
        df_datasets.to_csv(f"{output_dir}/datasets.csv", index=False, encoding="utf-8", sep=";")
        # load_to_sharepoint(sharepoint_site, sharepoint_folder, df_datasets, 'datasets.csv')

        logging.info("Extracting reports...")
        df_reports = extract_reports(workspaces_ids)
        df_reports.to_csv(f"{output_dir}/reports.csv", index=False, encoding="utf-8", sep=";")
        # load_to_sharepoint(sharepoint_site, sharepoint_folder, df_reports, 'reports.csv')
        
        logging.info("Extracting reports_pages...")
        df_reports_pages = extract_reports_pages(df_reports)
        df_reports_pages.to_csv(f"{output_dir}/reports_pages.csv", index=False, encoding="utf-8", sep=";")
        # load_to_sharepoint(sharepoint_site, sharepoint_folder, df_reports_pages, 'reports_pages.csv')

        workspaces_datasets = generate_workspaces_datasets_list(workspaces_ids)

        logging.info("Extracting datasets_info...")
        queries_dir = os.path.join(os.getcwd(), "dax_queries")
        
        for file in os.listdir(queries_dir):
            if file.endswith('.txt'):
                file_name = file.split(".")[0]
                file_dir = os.path.join(queries_dir, file)
                
                logging.info(f"Extracting {file_name}...")

                df_query = extract_dataset_info(workspaces_datasets, file_dir)
                df_query.to_csv(f"{output_dir}/{file_name}.csv", index=False, encoding="utf-8", sep=";")
                
            # load_to_sharepoint(sharepoint_site, sharepoint_folder, df_query, f'{file_name}.csv')

        logging.info("ETL process completed succesfully.")

    except Exception as e:
        logging.error(f"Critical error: {e}", exc_info=True)

if __name__ == '__main__':
    main()