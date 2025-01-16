import pandas as pd

def load_data(df: pd.DataFrame, file_name:str, output_path: str, output_format: str):
    if output_format == 'csv':
        df.to_csv(f'{output_path}/{file_name}.csv', index=False, sep=';', encoding='utf-8')
        print(f'The data for {file_name} has been sucessfully exported.')
    elif output_format == 'parquet':
        df.to_parquet(f'{output_path}/{file_name}.parquet', index=False)
        print(f'The data for {file_name} has been sucessfully exported.')
    else:
        print('Wrong output format, select between "csv" or "parquet"')