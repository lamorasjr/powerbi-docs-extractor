import os
import logging
from dotenv import load_dotenv
from src.extract_dax_info_tables import extract_datasets_dax_info
from src.extract_powerbi_api import (
    get_powerbi_access_token, 
    extract_workspaces_ids, 
    extract_workspaces_data, 
    extract_datasets_data, 
    extract_reports_data, 
    extract_reports_pages
)
from src.transformer import (
    transform_workspaces, 
    transform_reports, 
    transform_report_pages, 
    transform_datasets, 
    resolve_workspaces_datasets_list, 
    transform_relationships_info, 
    transform_tables_info,
    transform_columns_info,
    transform_measures_info,
    transform_calc_groups
)
from src.loader import get_sharepoint_access_token, load_csv_to_sharepoint, export_dataframes_to_excel

logging.basicConfig(
    level=logging.INFO,
    format='{asctime} - {levelname} - {message}',
    style='{',
    datefmt='%Y-%m-%d %H:%M'
)

# Load variables from .env file
load_dotenv()

# Read variables from .env file
PBI_TENANT_ID = os.getenv("PBI_TENANT_ID")
PBI_CLIENT_ID = os.getenv("PBI_CLIENT_ID")
PBI_CLIENT_SECRET = os.getenv("PBI_CLIENT_SECRET")
SHAREPOINT_SITE_URL = os.getenv("SHAREPOINT_SITE_URL")
SHAREPOINT_RELATIVE_URL = os.getenv("SHAREPOINT_RELATIVE_URL")
LOCAL_EXTRACT = os.getenv("LOCAL_EXTRACT")
LOCAL_OUTPUT_DIR = os.getenv("LOCAL_OUTPUT_DIR")

def main():  
    try:
        logging.info("Starting Power BI Docs extractor...")

        # Get access token for Power BI Rest API
        pbi_token = get_powerbi_access_token(PBI_TENANT_ID, PBI_CLIENT_ID, PBI_CLIENT_SECRET)

        # Extract list of workspaces ids from Power BI Rest API
        workspaces_ids = extract_workspaces_ids(pbi_token)
        
        # Extract data from Power BI Rest API
        logging.info("Extracting workspaces data...")
        workspaces_data = extract_workspaces_data(pbi_token, workspaces_ids)
        
        logging.info("Extracting report data...")
        reports_data = extract_reports_data(pbi_token, workspaces_ids)
        reports_pages_data = extract_reports_pages(pbi_token, reports_data)

        logging.info("Extracting semantic models data...")
        datasets_data = extract_datasets_data(pbi_token, workspaces_ids)    

        # Extract data from Dax Studio CDM
        workspaces_datasets_list = resolve_workspaces_datasets_list(datasets_data, workspaces_data)
        datasets_info_data = extract_datasets_dax_info(PBI_TENANT_ID, PBI_CLIENT_ID, PBI_CLIENT_SECRET, workspaces_datasets_list)

        # # Transform data and prepare for load
        logging.info("Transforming and preparing data for load...")
        workspaces_df = transform_workspaces(workspaces_data)    
        reports_df = transform_reports(reports_data, datasets_data, workspaces_data)
        reports_pages_df = transform_report_pages(reports_pages_data, reports_data, workspaces_data)
        datasets_df = transform_datasets(datasets_data, workspaces_data)
        tables_df = transform_tables_info(datasets_info_data)
        columns_df = transform_columns_info(datasets_info_data)
        measures_df = transform_measures_info(datasets_info_data)
        calc_groups_df = transform_calc_groups(datasets_info_data)
        relationships_df = transform_relationships_info(datasets_info_data)

        # Load prepared data to Sharepoint
        logging.info("Loading data to target object storage...")
        dataframes = [workspaces_df, reports_df, reports_pages_df, datasets_df, tables_df, columns_df, measures_df, calc_groups_df, relationships_df]
        sheet_names = ["Workspaces", "Reports", "Reports Pages", "Semantic Models", "Tables", "Columns", "Measures", "Calculation Groups", "Relationships"]
        file_name = "PowerBI_Docs.xlsx"
        
        if LOCAL_EXTRACT == "Y":
            file_name = os.path.join(LOCAL_OUTPUT_DIR, "PowerBI_Docs.xlsx")
            export_dataframes_to_excel(file_name, dataframes, sheet_names)
            logging.info("Succesfully completed the Power BI Docs extraction.")
        else:
            sp_token = get_sharepoint_access_token(PBI_TENANT_ID, PBI_CLIENT_ID, PBI_CLIENT_SECRET)
            load_csv_to_sharepoint(sp_token, SHAREPOINT_SITE_URL, SHAREPOINT_RELATIVE_URL, file_name, dataframes, sheet_names)

            logging.info("Succesfully completed the Power BI Docs extraction.")
    
    except Exception as e:
        logging.error(f"Critical error: {e}")

if __name__ == "__main__":
    main()