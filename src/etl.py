import pandas as pd
from powerbi_api_functions import get_datasets_in_workspace, get_datasets_dax_info


def etl_pbi_datasets():
    """
    Extract, transform and load all Power BI datasets from a given workspace to a Pandas dataframe.
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


def etl_dataset_tables(dataset_id:str):
    """
    Extract, transform and load all tables from a Power BI dataset to a Pandas dataframe.
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


def etl_dataset_columns(dataset_id:str):
    """
    Extract, transform and load all columns from a Power BI dataset to a Pandas dataframe.
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



def etl_dataset_measures(dataset_id:str):
    """
    Extract, transform and load all measures from a Power BI dataset to a Pandas dataframe.
    """
    with open(f'dax_queries/measures_info.txt', 'r') as f:
        dax_query = f.read()

    data = get_datasets_dax_info(dataset_id=dataset_id, dax_query=dax_query)
    df = pd.json_normalize(data)
    df_etl = df.copy()
    df_etl['SYS_TIMESTAMP'] = pd.to_datetime(pd.Timestamp('now'))
    df_etl['DATASET_ID'] = dataset_id
    df_etl = df_etl.rename(columns={'[Measure Id]':'MEASURE_ID',
                                    '[Table Id]':'TABLE_ID',
                                    '[Measure Name]':'MEASURE_NAME',
                                    '[Description]':'DESCRIPTION',
                                    '[Data Type Id]':'DATA_TYPE_ID',
                                    '[Data Type]':"DATA_TYPE",
                                    '[DAX Expression]':'DAX_EXPRESSION', 
                                    '[Is Hidden?]':'IS_HIDDEN',
                                    '[Modified Time]':'MODIFIED_AT', 
                                    '[Display Folder]':'DISPLAY_FOLDER'})
    df_etl['MODIFIED_AT'] = pd.to_datetime(df_etl['MODIFIED_AT']).dt.date
    df_etl = df_etl[['DATASET_ID',
                     'TABLE_ID',
                     'MEASURE_ID',
                     'MEASURE_NAME',
                     'DATA_TYPE',
                     'DESCRIPTION',
                     'DAX_EXPRESSION',
                     'DISPLAY_FOLDER',
                     'IS_HIDDEN',
                     'MODIFIED_AT',
                     'SYS_TIMESTAMP']]
    return df_etl


def etl_dataset_relationships(dataset_id:str):
    """
    Extract, transform and load all relationships from a Power BI dataset to a Pandas dataframe.
    """
    with open(f'dax_queries/relationships_info.txt', 'r') as f:
        dax_query = f.read()

    data = get_datasets_dax_info(dataset_id=dataset_id, dax_query=dax_query)
    df = pd.json_normalize(data)
    df_etl = df.copy()
    df_etl['SYS_TIMESTAMP'] = pd.to_datetime(pd.Timestamp('now'))
    df_etl['DATASET_ID'] = dataset_id
    df_etl = df_etl.rename(columns={'[Relationship Id]':'RELATIONSHIP_ID',
                                    '[Relationship]':'RELATIONSHIP',
                                    '[From Table Id]':'FROM_TABLE_ID',
                                    '[From Column Id]':'FROM_COLUMN_ID',
                                    '[From Cardinality Id]':'FROM_CARDINALITY_ID',
                                    '[From Cardinality]':'FROM_CARDINALITY',
                                    '[To Table Id]':'TO_TABLE_ID',
                                    '[To Column Id]':'TO_COLUMN_ID',
                                    '[To Cardinality Id]':'TO_CARDINALITY_ID',
                                    '[To Cardinality]':'TO_CARDINALITY',
                                    '[Cross Filtering Behavior Id]':'CROSS_FILTERING_BEHAVIOR_ID',
                                    '[Cross Filtering Behavior]':'CROSS_FILTERING_BEHAVIOR',
                                    '[Is Active?]':'IS_ACTIVE',
                                    '[Security Filtering Behavior Id]':'SECURITY_FILTERING_BEHAVIOR_ID',
                                    '[Security Filtering Behavior]':'SECURITY_FILTERING_BEHAVIOR',
                                    '[Modified Time]':'MODIFIED_AT'})
    df_etl['MODIFIED_AT'] = pd.to_datetime(df_etl['MODIFIED_AT']).dt.date
    df_etl = df_etl[['DATASET_ID',
                     'RELATIONSHIP_ID',
                     'RELATIONSHIP',
                     'IS_ACTIVE',
                     'FROM_TABLE_ID',
                     'FROM_COLUMN_ID',
                     'FROM_CARDINALITY',
                     'TO_TABLE_ID',
                     'TO_COLUMN_ID', 
                     'TO_CARDINALITY',
                     'CROSS_FILTERING_BEHAVIOR',
                     'SECURITY_FILTERING_BEHAVIOR',     
                     'MODIFIED_AT',
                     'SYS_TIMESTAMP', 
                     ]]
    return df_etl
