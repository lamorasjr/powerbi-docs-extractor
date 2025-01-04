import os
import glob
from get_pbi_objects import get_pbi_object_in_group
from get_pbi_dataset_info import query_pbi_dataset_info

def get_dax_queries(folder_path:str):
    files_list = glob.glob(os.path.join(folder_path, '*.txt'))
    dax_queries_dict = {}
    for f in files_list:
        with open(f, mode='r') as file:
            file_content = file.read()
        file_name = f.split('/')[-1].split('.txt')[0]
        dax_queries_dict[file_name] = file_content
    return dax_queries_dict

def etl_pbi_dataset_info():
    dax_queries = get_dax_queries(os.getenv('DAX_QUERIES_FOLDER'))
    dfs_dict = {}
    for query_name, query_code in dax_queries.items():
        dfs_dict[query_name] = query_pbi_dataset_info(query_code)
    return dfs_dict

# Power BI objects: 'datasets', 'dataflows', 'dashboards', 'reports'
def etl_datasets():
    df = get_pbi_object_in_group('datasets')
    return df

def etl_dataflows():
    df = get_pbi_object_in_group('dataflows')
    return df

def etl_dashboards():
    df = get_pbi_object_in_group('dashboards')
    return df

def etl_reports():
    df = get_pbi_object_in_group('reports')
    return df

def merge_etl_pbi_objects():
    dfs_dict = {
        'datasets' : etl_datasets(),
        'dataflows' : etl_dataflows(),
        'dashboards' : etl_dashboards(),
        'reports' : etl_reports(),
    }
    return dfs_dict

def etl_pbi_tables():
    dfs_pbi_object = merge_etl_pbi_objects()
    dfs_pbi_info = etl_pbi_dataset_info()
    return {**dfs_pbi_object, **dfs_pbi_info}

# Use case example:
if __name__ == '__main__':
    print(etl_pbi_tables())

    
