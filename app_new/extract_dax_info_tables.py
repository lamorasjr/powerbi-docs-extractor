import os
import json
import subprocess
from urllib.parse import quote
from datetime import datetime

def dscmd_export_to_json(tenant_id, client_id, client_secret, server, dataset_name, file_name):
    """
    Outputs a json file based on the results of a DAX query with Dax Studio Portable.
    """
    dscmd_exe = os.path.join(os.getcwd(), "tools", "dax_studio", "dscmd.exe")

    dax_query = """
    EVALUATE INFO.TABLES()
    EVALUATE INFO.PARTITIONS()
    EVALUATE INFO.COLUMNS()
    EVALUATE INFO.MEASURES()
    EVALUATE INFO.RELATIONSHIPS()
    EVALUATE INFO.CALCULATIONGROUPS()
    EVALUATE INFO.CALCULATIONITEMS()
    """

    prompt = [
        dscmd_exe,
        "csv", file_name,
        "-s", server,
        "-d", dataset_name,
        "-u", f"app:{client_id}@{tenant_id}", 
        "-p", client_secret,
        "-q", dax_query,
        "-t", "JSON"
    ]

    subprocess.run(prompt, capture_output=True, text=True, check=True)
    

def extract_datasets_dax_info(tenant_id, client_id, client_secret, workspaces_datasets_list):
    """
    Query data from dax info functions from workspaces and datasets with Dax Studio Portable.
    """
    timestamp = datetime.now()
    temp_file = os.path.join(os.getcwd(), "tools", "temp.json")

    data = []

    for i in workspaces_datasets_list:
        workspace_id = i.get("workspace_id")
        workspace_name = i.get("workspace_name")
        dataset_id = i.get("dataset_id")
        dataset_name = i.get("dataset_name")
        
        server = f"powerbi://api.powerbi.com/v1.0/myorg/{quote(workspace_name)}"

        try: 
            dscmd_export_to_json(tenant_id, client_id, client_secret, server, dataset_name, temp_file)

            with open(temp_file, "r", encoding="utf-8") as file:
                dscmd_data = json.load(file)
        
            response = dscmd_data.get("results")[0]["tables"]

            response_data = {
                "workspace_id": workspace_id,
                "workspace_name": workspace_name,
                "dataset_id" : dataset_id,
                "dataset_name" : dataset_name,
                "extract_timestamp" : timestamp
            }

            for i, v in enumerate(response):
                
                if i == 0:
                    response_data["info_tables"] = v.get("rows")
                if i == 1:
                    response_data["info_partitions"] = v.get("rows")
                if i == 2:
                    response_data["info_columns"] = v.get("rows")
                if i == 3:
                    response_data["info_measures"] = v.get("rows")
                if i == 4:
                    response_data["info_relationships"] = v.get("rows")
                if i == 5:
                    response_data["info_calculationgroups"] = v.get("rows")
                if i == 6:
                    response_data["info_calculationitems"] = v.get("rows")

            data.append(response_data)
                    
            print(f"Sucessfully exported data from {server} - {dataset_name}")
        
        except subprocess.CalledProcessError as e:
            print(f"Export error: {e.stdout} {e.stderr}.")

    os.remove(temp_file)
    return data