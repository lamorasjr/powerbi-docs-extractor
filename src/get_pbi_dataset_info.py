import os
import requests
import pandas as pd
from get_pbi_objects import get_datasets_ids

def get_pbi_dataset_info(dataset_id:str, dax_query:str):
    PBI_API_TOKEN = os.getenv('PBI_API_TOKEN')
    url = f'https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/executeQueries'
    headers = { 
        'Authorization' : f'Bearer {PBI_API_TOKEN}',
        'Content-type' : 'application/json'
    }
    body = {
        'queries': [{'query': f'{dax_query}'}],
        'serializerSettings': {'includeNulls': 'true'}
    }
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    df = pd.json_normalize(data, record_path=['results', 'tables', 'rows'])
    return df

def query_pbi_dataset_info(dax_query:str):
    dataset_ids = get_datasets_ids()
    df_list = []
    for id in dataset_ids:
        df = get_pbi_dataset_info(id, dax_query)
        df['Semantic Model Id'] = id
        df_list.append(df)
    df_total = pd.concat(df_list, ignore_index=True)
    return df_total


# Use case example:
if __name__ == '__main__':
    dax_query = '''
    EVALUATE
        SELECTCOLUMNS(
            INFO.MEASURES(),
            "Measure Id", [ID],
            "Measure Name", [Name],
            "Table Id", [TableID],
            "Description", [Description],
            "Data Type", SWITCH(
                            [DataType], 
                            6, "Whole Number",
                            8, "Decimal Number"
                        ),
            "Is Hidden", [IsHidden],
            "Modified Time", [ModifiedTime]
        )
    '''

    measures_info = query_pbi_dataset_info(dax_query)
    print(measures_info.head())
