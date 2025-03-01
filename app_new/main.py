import os
from dotenv import load_dotenv
from extract_powerbi_api import get_powerbi_access_token, extract_workspaces_ids, extract_workspaces_data, extract_datasets_data, extract_reports_data, extract_reports_pages
from extract_dax_info_tables import extract_datasets_dax_info
from transformer import transform_workspaces, transform_reports, transform_report_pages, transform_datasets, resolve_workspaces_datasets_list, unpack_dax_info_data, transform_tables
from loader import get_sharepoint_access_token, load_csv_to_sharepoint, export_dataframes_to_excel

# Load variables from .env file
load_dotenv()

# Read variables from .env file
PBI_TENANT_ID = os.getenv("PBI_TENANT_ID")
PBI_CLIENT_ID = os.getenv("PBI_CLIENT_ID")
PBI_CLIENT_SECRET = os.getenv("PBI_CLIENT_SECRET")
SHAREPOINT_SITE_URL = os.getenv("SHAREPOINT_SITE_URL")
SHAREPOINT_RELATIVE_URL = os.getenv("SHAREPOINT_RELATIVE_URL")

def main():  
    # Get access token for Power BI Rest API
    pbi_token = get_powerbi_access_token(PBI_TENANT_ID, PBI_CLIENT_ID, PBI_CLIENT_SECRET)

    # Extract list of workspaces ids from Power BI Rest API
    workspaces_ids = extract_workspaces_ids(pbi_token)
    
    # Extract data from Power BI Rest API
    workspaces_data = extract_workspaces_data(pbi_token, workspaces_ids)
    reports_data = extract_reports_data(pbi_token, workspaces_ids)
    reports_pages_data = extract_reports_pages(pbi_token, reports_data)
    datasets_data = extract_datasets_data(pbi_token, workspaces_ids)    
    # Extract data from Dax Studio CDM
    workspaces_datasets_list = resolve_workspaces_datasets_list(datasets_data, workspaces_data)
    datasets_info_data = extract_datasets_dax_info(PBI_TENANT_ID, PBI_CLIENT_ID, PBI_CLIENT_SECRET, workspaces_datasets_list)
    
    import json
    from datetime import datetime

    def datetime_converter(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO 8601 string
        raise TypeError("Type not serializable")
    
    with open("output.json", 'w') as json_file:
        json.dump(datasets_info_data, json_file, indent=4, default=datetime_converter)

    # # Transform data and prepare for load
    # workspaces_df = transform_workspaces(workspaces_data)    
    # reports_df = transform_reports(reports_data, datasets_data, workspaces_data)
    # reports_pages_df = transform_report_pages(reports_pages_data, reports_data, workspaces_data)
    # datasets_df = transform_datasets(datasets_data, workspaces_data)
    # tables_df = transform_tables(datasets_info_data)
    # # columns_df = None
    # # measures_df = None
    # # relationships_df = None

    # # Load prepared data to Sharepoint
    # dataframes = [workspaces_df, reports_df, reports_pages_df, datasets_df, tables_df]
    # sheet_names = ["Workspaces", "Reports", "Reports Pages", "Semantic Models", "Tables"]
    # file_name = "PowerBI_Docs.xlsx"
    
    # export_dataframes_to_excel(file_name, dataframes, sheet_names)
    # sp_token = get_sharepoint_access_token(PBI_TENANT_ID, PBI_CLIENT_ID, PBI_CLIENT_SECRET)
    # load_csv_to_sharepoint(sp_token, SHAREPOINT_SITE_URL, SHAREPOINT_RELATIVE_URL, file_name, dataframes, sheet_names)

if __name__ == "__main__":
    main()