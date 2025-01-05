import pandas as pd
from etl import etl_pbi_datasets, etl_dataset_tables, etl_dataset_columns, etl_dataset_measures, etl_dataset_relationships

def etl_pbi_tables(dataset_ids:list) -> pd.DataFrame:
    df_list = [ etl_dataset_tables(dataset_id=id) for id in dataset_ids ]
    df = pd.concat(df_list, ignore_index=True)
    return df

def etl_pbi_columns(dataset_ids:list) -> pd.DataFrame:
    df_list = [ etl_dataset_columns(dataset_id=id) for id in dataset_ids ]
    df = pd.concat(df_list, ignore_index=True)
    return df

def etl_pbi_measures(dataset_ids:list) -> pd.DataFrame:
    df_list = [ etl_dataset_measures(dataset_id=id) for id in dataset_ids ]
    df = pd.concat(df_list, ignore_index=True)
    return df

def etl_pbi_relationships(dataset_ids:list) -> pd.DataFrame:
    df_list = [ etl_dataset_relationships(dataset_id=id) for id in dataset_ids ]
    df = pd.concat(df_list, ignore_index=True)
    return df


if __name__ == '__main__':
    df_pbi_datasets = etl_pbi_datasets()
    df_pbi_datasets.to_csv('data/pbi_datasets_info.csv', index=False, sep=';', encoding='utf-8')
    print('Power BI datasets info has been sucessefully exported')

    dataset_ids = list(df_pbi_datasets['DATASET_ID'])

    df_pbi_tables = etl_pbi_tables(dataset_ids)
    df_pbi_tables.to_csv('data/pbi_datasets_info.csv', index=False, sep=';', encoding='utf-8')
    print('Power BI tables info has been sucessefully exported')

    df_pbi_columns = etl_pbi_columns(dataset_ids)
    df_pbi_columns.to_csv('data/pbi_columns_info.csv', index=False, sep=';', encoding='utf-8')
    print('Power BI columns info has been sucessefully exported')

    df_pbi_measures = etl_pbi_measures(dataset_ids)
    df_pbi_measures.to_csv('data/pbi_measures_info.csv', index=False, sep=';', encoding='utf-8')
    print('Power BI measures info has been sucessefully exported')

    df_pbi_relationships = etl_pbi_relationships(dataset_ids)
    df_pbi_relationships.to_csv('data/pbi_relationships_info.csv', index=False, sep=';', encoding='utf-8')
    print('Power BI relationships info has been sucessefully exported')