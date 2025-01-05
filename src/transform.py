import pandas as pd
from powerbi_api_functions import get_datasets_in_workspace, get_datasets_dax_info

# ETL function for pbi datasets
def etl_pbi_datasets():
    """
    Extract all Power BI datasets from a workspace, transform and load in a Pandas DataFrame.
    """
    data = get_datasets_in_workspace()
    df = pd.json_normalize(data)
    df_etl = df.copy()
    df_etl['SYS_TIMESTAMP'] = pd.to_datetime(pd.Timestamp('now'))
    df_etl = df[['id', 'name', 'webUrl', 'createdDate']]
    df_etl = df_etl.rename(columns={'id':'DATASET_ID',
                                    'name':'DATASET_NAME',
                                    'webUrl':'WEB_URL',
                                    'createdDate':'CREATED_AT'})
    df_etl['CREATED_AT'] = pd.to_datetime(df_etl['CREATED_AT']).dt.date
    return df_etl

# ETL function for pbi dataset tables
def etl_pbi_tables(dataset_id:str):
    """
    Extract all tables from a Power BI dataset, transform and load in a Pandas DataFrame.
    """
    with open(f'dax_queries/tables_info.txt', 'r') as f:
        dax_query = f.read()

    data = get_datasets_dax_info(dataset_id=dataset_id, dax_query=dax_query)
    df = pd.json_normalize(data)
    df_etl = df.copy()
    df_etl['SYS_TIMESTAMP'] = pd.to_datetime(pd.Timestamp('now'))
    df_etl['DATASET_ID'] = dataset_id
    df_etl = df_etl.rename(columns={'[Table Id]':'TABLE_ID',
                                    '[Table Name]':'TABLE_NAME',
                                    '[Data Category]':'DATA_CATEGORY',
                                    '[Description]':'DESCRIPTION',
                                    '[Is Hidden]':'IS_HIDDEN',
                                    '[Modified Time]':'MODIFIED_AT',
                                    '[Table Type]':'TABLE_TYPE',
                                    '[Calculation Group Flag]':'CALCULATION_GROUP_FLAG',
                                    '[Query Definition]':'QUERY_DEFINITION'})
    df_etl['MODIFIED_AT'] = pd.to_datetime(df_etl['MODIFIED_AT']).dt.date
    df_etl = df_etl[['DATASET_ID', 
                     'TABLE_ID',
                     'TABLE_NAME',
                     'DESCRIPTION',
                     'DATA_CATEGORY',
                     'TABLE_TYPE',
                     'CALCULATION_GROUP_FLAG',
                     'QUERY_DEFINITION',
                     'IS_HIDDEN',
                     'MODIFIED_AT',
                     'SYS_TIMESTAMP']]
    return df_etl


# ETL function for pbi dataset columns
def etl_pbi_columns(dataset_id:str):
    """
    Extract all columns from a Power BI dataset, transform and load in a Pandas DataFrame.
    """
    with open(f'dax_queries/columns_info.txt', 'r') as f:
        dax_query = f.read()

    data = get_datasets_dax_info(dataset_id=dataset_id, dax_query=dax_query)
    df = pd.json_normalize(data)
    df_etl = df.copy()
    df_etl['SYS_TIMESTAMP'] = pd.to_datetime(pd.Timestamp('now'))
    df_etl['DATASET_ID'] = dataset_id
    df_etl = df_etl.rename(columns={'[Column Id]':'COLUMN_ID',
                                    '[Table Id]':'TABLE_ID',
                                    '[Column Name]':'COLUMN_NAME',
                                    '[Column Type Id]':'COLUMN_TYPE_ID',
                                    '[Column Type]':'COLUMN_TYPE',
                                    '[DAX Expression]':'DAX_EXPRESSION',
                                    '[Data Type Id]':'DATA_TYPE_ID',
                                    '[Data Type]':'DATA_TYPE',
                                    '[Data Category]':'DATA_CATEGORY',
                                    '[Description]':'DESCRIPTION',
                                    '[Is Hidden?]':'IS_HIDDEN',
                                    '[Modified Time]':'MODIFIED_AT',
                                    '[Display Folder]':'DISPLAY_FOLDER'})
    df_etl['MODIFIED_AT'] = pd.to_datetime(df_etl['MODIFIED_AT']).dt.date
    df_etl = df_etl[['DATASET_ID',
                     'TABLE_ID',
                     'COLUMN_ID',
                     'COLUMN_NAME',
                     'COLUMN_TYPE',
                     'DATA_TYPE',
                     'DESCRIPTION',
                     'DAX_EXPRESSION',
                     'DATA_CATEGORY',
                     'IS_HIDDEN',
                     'MODIFIED_AT',
                     'SYS_TIMESTAMP']]
    return df_etl


# ETL function for pbi dataset measures
def etl_pbi_measures(dataset_id:str):
    """
    Extract all measures from a Power BI dataset, transform and load in a Pandas DataFrame.
    """
    with open(f'dax_queries/measures_info.txt', 'r') as f:
        dax_query = f.read()

    data = get_datasets_dax_info(dataset_id=dataset_id, dax_query=dax_query)
    df = pd.json_normalize(data)
    return df


# ETL function for pbi dataset relationships
def etl_pbi_relationships(dataset_id:str):
    """
    Extract all relationships from a Power BI dataset, transform and load in a Pandas DataFrame.
    """
    with open(f'dax_queries/relationships_info.txt', 'r') as f:
        dax_query = f.read()

    data = get_datasets_dax_info(dataset_id=dataset_id, dax_query=dax_query)
    df = pd.json_normalize(data)
    return df

if __name__ == '__main__':
    df_datasets = etl_pbi_datasets()
    # print(df_datasets.head())
    
    test_dataset = df_datasets['DATASET_ID'].iloc[0]
    
    df_tables = etl_pbi_tables(dataset_id=test_dataset)
    # print(df_tables.head())
    df_tables.to_csv('data_raw/pbi_tables_raw.csv', index=False, sep=';', encoding='utf-8')

    df_columns = etl_pbi_columns(dataset_id=test_dataset)
    # print(df_columns.info())
    df_columns.to_csv('data_raw/pbi_columns_raw.csv', index=False, sep=';', encoding='utf-8')
    
    # df_measures = etl_pbi_measures(dataset_id=test_dataset)
    # # print(df_measures.head(2))
    
    # df_relationships = etl_pbi_relationships(dataset_id=test_dataset)
    # # print(df_relationships.head(2))


    # # Export raw data to csv
    # df_datasets.to_csv('data_raw/pbi_datasets_raw.csv', index=False, sep=';', encoding='utf-8')

    # df_columns.to_csv('data_raw/pbi_columns_raw.csv', index=False, sep=';', encoding='utf-8')
    # df_measures.to_csv('data_raw/pbi_measures_raw.csv', index=False, sep=';', encoding='utf-8')
    # df_relationships.to_csv('data_raw/pbi_relationships_raw.csv', index=False, sep=';', encoding='utf-8')
    # print('The raw data files were exported successfully')