from etl_pbi import export_pbi_in_group, get_datasets_ids
from etl_pbi_info import etl_pbi_info

pbi_objects = ["datasets", "dataflows", "dashboards", "reports"]
dataset_ids = get_datasets_ids()
dax_query = 'EVALUATE INFO.MEASURES()'
file_name = 'measures_info'

for i in pbi_objects:
    export_pbi_in_group(i)

etl_pbi_info(dataset_ids, dax_query, file_name)
