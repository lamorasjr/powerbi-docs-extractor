import os
import requests
import zipfile
import subprocess
import json
import re
import pandas as pd
from io import BytesIO
from urllib.parse import quote
from functions_powerbi_api import generate_workspaces_datasets_list


def setup_dax_studio():
    """
    Check if Dax Studio portable is avaliable, otherwise download it from Github.
    """
    tool_dir = os.path.join(os.getcwd(), "tools")
    os.makedirs(tool_dir, exist_ok=True)
    
    tool_path = os.path.join(tool_dir, "dax_studio" ,"dscmd.exe")

    if os.path.exists(tool_path):
        print("Dax Studio is ready!")
    else:
        print("Dax Studio is not ready. Installing requirements...")
        
        tool_url = "https://github.com/DaxStudio/DaxStudio/releases/download/v3.2.1/DaxStudio_3_2_1_portable.zip"

        response = requests.get(tool_url, stream=True)
        
        if response.status_code == 200:
            with zipfile.ZipFile(BytesIO(response.content), "r") as zip_content:
                extract_path = os.path.join(tool_dir, "dax_studio")
                zip_content.extractall(extract_path)

            print("Downloaded completed. Dax Studio is ready!")
        
        else:
            raise requests.RequestException(f"Failed to download DAX Studio: {response.status_code} - {response.text}")


def extract_dax_query_dscmd(workspace_name, dataset_name, dax_query_file):
    """
    Excecute a dax query in Power BI workspaces with Dax Studio Portable.
    """
    DSCMD = os.path.join(os.getcwd(), "tools", "dax_studio", "dscmd.exe")
    temp_file = "C:/Users/lamoras/workspace/powerbi-catalog-extractor/tools/temp.json"    

    tenant_id = os.getenv("PBI_TENANT_ID")
    client_id = os.getenv("PBI_CLIENT_ID")
    client_secret = os.getenv("PBI_CLIENT_SECRET")

    prompt = [
        DSCMD,
        "csv", temp_file,
        "-s", f"powerbi://api.powerbi.com/v1.0/myorg/{quote(workspace_name)}",
        "-d", dataset_name,
        "-u", f"app:{client_id}@{tenant_id}", 
        "-p", client_secret,
        "-f", dax_query_file,
        "-t", "JSON"
    ]

    try:
        result = subprocess.run(prompt, capture_output=True, text=True, check=True)

        result_output = result.stdout.split("\n")
        for line in result_output:
            if "Exporting to file" not in line :
                print(line)
        
        with open(temp_file, "r") as file:
            json_data = json.load(file)
        
        data = json_data["results"][0]["tables"][0]["rows"]
        os.remove(temp_file)
        return data
    
    except subprocess.CalledProcessError as e:
        print(f"Dax Studio extraction failed for {os.path.basename(dax_query_file)}/{workspace_name}/{dataset_name} - Error details: {e.stdout} {e.stderr}.")


def extract_dataset_info(workspaces_datasets_list, dax_query_file):
    all_data = []

    for i in workspaces_datasets_list:
        workspace_name = i.get("WORKSPACE_NAME")
        dataset_name = i.get("DATASET_NAME")

        response = extract_dax_query_dscmd(workspace_name, dataset_name, dax_query_file)

        data = {
            'WORKSPACE_ID': i.get("WORKSPACE_ID"),
            'DATASET_ID' : i.get('DATASET_ID'),
            'response' : response
        }

        all_data.append(data)

    df_raw = pd.json_normalize(all_data, meta=['WORKSPACE_ID', 'DATASET_ID'], record_path='response')
    df = df_raw.copy()
    old_columns_name = df.columns
    new_columns_name = {i: re.sub(r'\[([^\]]+)\]', r'\1', i) for i in old_columns_name}
    df = df.rename(columns=new_columns_name)
    return df


if __name__ == "__main__":
    setup_dax_studio()
    
    output_dir = os.path.join(os.getcwd(), "test")
    os.makedirs(output_dir, exist_ok=True)
    
    workspaces_ids = [ i.strip() for i in os.getenv('PBI_WORKSPACES_IDS').split(",") ]
    workspaces_datasets = generate_workspaces_datasets_list(workspaces_ids)

    queries_dir = os.path.join(os.getcwd(), "dax_queries")
    
    for file in os.listdir(queries_dir):
        if file.endswith('.txt'):
            file_name = file.split(".")[0]
            file_dir = os.path.join(queries_dir, file)

            df_query = extract_dataset_info(workspaces_datasets, file_dir)
            df_query.to_csv(f"{output_dir}/{file_name}.csv", index=False, encoding="utf-8", sep=";")
            