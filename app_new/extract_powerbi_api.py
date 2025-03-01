import requests
from datetime import datetime

def get_powerbi_access_token(tenant_id, client_id, client_secret):
    """
    Generate Bearer token for Power BI Rest API with service principal.
    """
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://analysis.windows.net/powerbi/api/.default"
    }

    response = requests.post(url=url, data=payload)
        
    if response.status_code == 200:
        response_json = response.json()
        data = response_json["access_token"]
        return data

    else:
        raise KeyError(f"Error to get Power BI access token: {response.status_code} - {response}")
    
    
def extract_powerbi_data(access_token, endpoint):
    """
    Extract data from Power BI Rest API.
    """
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"  
    }

    response = requests.get(url=url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        raise KeyError(f"Failed request for {endpoint}. Status code: {response.status_code}. Error message: {response.text}")
    

def extract_workspaces_ids(access_token):
    """
    Extracts workspaces ids which the user has access.
    """
    endpoint = ""
    response = extract_powerbi_data(access_token, endpoint).get("value")

    all_data = []

    for i in response:
        workspace_id = i.get("id")
        all_data.append(workspace_id)

    return all_data


def extract_workspaces_data(access_token, workspaces_ids):
    """
    Extracts workspaces data for a given list of workspaces ids.
    """
    timestamp = datetime.now()
    data = []

    for workspace_id in workspaces_ids:
        endpoint = workspace_id
        response = extract_powerbi_data(access_token, endpoint)
        response_data = {
            "workspace_id" : workspace_id,
            "workspace_name" : response.get("name"),
            "type" : response.get("type"),
            "is_dedicated_capacity": response.get("isOnDedicatedCapacity"),
            "capacity_id" : response.get("capacityId"),
            "dataset_storage_format" : response.get("defaultDatasetStorageFormat"),
            "extract_timestamp" : timestamp
        }

        data.append(response_data)

    return data


def extract_datasets_data(access_token, workspaces_ids):
    """
    Extracts datasets data for a given list of workspaces ids.
    """
    timestamp = datetime.now()
    data = []

    for workspace_id in workspaces_ids:
        endpoint = f"{workspace_id}/datasets"
        response = extract_powerbi_data(access_token, endpoint).get("value")

        for i in response:
            response_data = {
                "workspace_id" : workspace_id,
                "dataset_id" : i.get("id"),
                "dataset_name" : i.get("name"),
                "configured_by": i.get("configuredBy"),
                "created_at" : i.get("createdDate"),
                "web_url" : i.get("webUrl"),
                "extract_timestamp" : timestamp
            }

            data.append(response_data)
    
    return data


def extract_reports_data(access_token, workspaces_ids):
    """
    Extracts reports data for a given list of workspaces ids.
    """
    timestamp = datetime.now()
    data = []

    for workspace_id in workspaces_ids:
        endpoint = f"{workspace_id}/reports"
        response = extract_powerbi_data(access_token, endpoint).get("value")

        for i in response:
            response_data = {
                "workspace_id" : workspace_id,
                "report_id" : i.get("id"),
                "report_name" : i.get("name"),
                "report_type" : i.get("reportType"),
                "dataset_id": i.get("datasetId"),
                "web_url" : i.get("webUrl"),
                "extract_timestamp" : timestamp
            }

            data.append(response_data)
    
    return data


def extract_reports_pages(access_token, reports_data):
    """
    Extracts reports pages data for a given list[dict] of reports data.
    """
    timestamp = datetime.now()
    data = []

    for i in reports_data:
        workspace_id = i.get("workspace_id")
        report_id = i.get("report_id")
        report_type = i.get("report_type")

        if report_type == "PowerBIReport":

            endpoint = f"{workspace_id}/reports/{report_id}/pages"

            response = extract_powerbi_data(access_token, endpoint).get("value")

            for i in response:
                response_data = {
                    "workspace_id" : workspace_id,
                    "report_id" : report_id,
                    "page_id" : i.get("name"),
                    "page_name" : i.get("displayName"),
                    "order" : i.get("order"),
                    "extract_timestamp" : timestamp
                }

                data.append(response_data)

    return data
