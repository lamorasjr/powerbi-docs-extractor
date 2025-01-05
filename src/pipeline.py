import pandas as pd
from etl import etl_pbi_datasets, etl_dataset_tables, etl_dataset_columns, etl_dataset_measures, etl_dataset_relationships

def generate_datasets_ids():
    """
    Returns a list with ids of all datasets in the workspace
    """
    df_datasets = etl_pbi_datasets()
    datasets_ids = list(df_datasets['DATASET_ID'])
    return datasets_ids

def build_pbi_tables_info():
    """
    Extract, transform and combine all tables from all datasets to a Pandas dataframe.
    """
    datasets_ids = generate_datasets_ids()
    df_list = [ etl_dataset_tables(dataset_id=id) for id in datasets_ids ]
    df_total = pd.concat(df_list, ignore_index=True)
    return df_total

def build_pbi_columns_info():
    """
    Extract, transform and combine all columns from all datasets to a Pandas dataframe.
    """
    datasets_ids = generate_datasets_ids()
    df_list = [ etl_dataset_columns(dataset_id=id) for id in datasets_ids ]
    df_total = pd.concat(df_list, ignore_index=True)
    return df_total



print(build_pbi_columns_info())



# df_tables.to_csv('data_raw/pbi_tables_raw.csv', index=False, sep=';', encoding='utf-8')

# df_columns = etl_pbi_columns(dataset_id=test_dataset)
# print(df_columns.info())
# df_columns.to_csv('data_raw/pbi_columns_raw.csv', index=False, sep=';', encoding='utf-8')

# df_measures = etl_pbi_measures(dataset_id=test_dataset)
# print(df_measures.info())
# df_measures.to_csv('data_raw/pbi_measures_raw.csv', index=False, sep=';', encoding='utf-8')

# df_relationships = etl_pbi_relationships(dataset_id=test_dataset)
# print(df_relationships.iloc[0])
# df_relationships.to_csv('data_raw/pbi_relationships_raw.csv', index=False, sep=';', encoding='utf-8')

