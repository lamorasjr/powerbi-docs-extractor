import os
from dotenv import load_dotenv
from transformer import transform_workspaces, transform_reports, transform_report_pages
from loader import get_sharepoint_access_token, load_csv_to_sharepoint
from extract_powerbi_api import ( 
    get_powerbi_access_token,       
    extract_workspaces_ids,      
    extract_workspaces_data,       
    extract_datasets_data,         
    extract_reports_data,       
    extract_reports_pages 
)

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
    datasets_data = extract_datasets_data(pbi_token, workspaces_ids)
    reports_data = extract_reports_data(pbi_token, workspaces_ids)
    reports_pages_data = extract_reports_pages(pbi_token, reports_data)
    tables_data = None
    columns_data = None
    measures_data = None
    relationships_data = None

    # Transform data and prepare for load
    workspaces_df = transform_workspaces(workspaces_data)    
    reports_df = transform_reports(reports_data, datasets_data, workspaces_data)
    reports_pages_df = transform_report_pages(reports_pages_data, reports_data, workspaces_data)
    tables_df = None
    columns_df = None
    measures_df = None
    relationships_df = None

    # Load prepared data to Sharepoint
    dataframes = [workspaces_df, reports_df, reports_pages_df]
    sheet_names = ["Workspaces", "Reports", "Reports Pages"]
    file_name = "PowerBI_Docs.xlsx"
    
    sp_token = get_sharepoint_access_token(PBI_TENANT_ID, PBI_CLIENT_ID, PBI_CLIENT_SECRET)
    load_csv_to_sharepoint(sp_token, SHAREPOINT_SITE_URL, SHAREPOINT_RELATIVE_URL, file_name, dataframes, sheet_names)

if __name__ == "__main__":
    main()