import pandas as pd
import warnings
from src.pipeline import etl_pbi_tables

output_path = 'data/'

# Ignore specific FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

pbi_dfs = etl_pbi_tables()

with pd.ExcelWriter(f'{output_path}/powerbi_data_catalog.xlsx') as writer:
    for sheet_name, df in pbi_dfs.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print('The powerbi_data_catalog.xlsx file has been exported successfully')