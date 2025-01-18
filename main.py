import os
import logging
from src.powerbi_rest_api import get_auth_token
from src.extractor import (
    etl_powerbi_workspaces,
    etl_powerbi_reports,
    etl_powerbi_reports_pages,
    etl_powerbi_datasets,
    etl_datasets_dax_queries
)

def main(output_path='sample_data/', output_format='csv'):

    logging.info("Starting Power BI ETL process...")
    try:

        tenant_id = os.getenv('PBI_TENANT_ID')
        client_id = os.getenv('PBI_CLIENT_ID')
        client_secret = os.getenv('PBI_CLIENT_SECRET')
        workspaces_ids = os.getenv('PBI_WORKSPACES_IDS').split(",")

        # Check if the variables were given
        if None in [tenant_id, client_id, client_secret, workspaces_ids]:
            raise ValueError("One or more required variables are missing, review .env file.")

        # Generate access token
        access_token = get_auth_token(tenant_id, client_id, client_secret)
        logging.info("Successfully authenticated with Power BI API.")

        # Run ETL of Power BI data
        etl_powerbi_workspaces(access_token, workspaces_ids, output_path, output_format)
        etl_powerbi_reports(access_token, workspaces_ids, output_path, output_format)
        etl_powerbi_reports_pages(access_token, workspaces_ids, output_path, output_format)
        etl_powerbi_datasets(access_token, workspaces_ids, output_path, output_format)
        etl_datasets_dax_queries(access_token, workspaces_ids, output_path, output_format)
        logging.info("ETL process completed successfully.")

    except Exception as e:
        logging.error(f"Critical error: {e}")

if __name__ == '__main__':
    main()