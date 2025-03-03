import re
import pandas as pd

def transform_workspaces(workspaces_data):
    """
    Transform workspaces data.
    """
    df = pd.json_normalize(workspaces_data)
    df['is_dedicated_capacity'] = df['is_dedicated_capacity'].astype(int)
    return df


def transform_reports(reports_data, datasets_data, workspaces_data):
    """
    Transform reports data.
    """
    df1 = pd.json_normalize(reports_data)
    
    df2 = pd.json_normalize(datasets_data)
    df2 = df2[["workspace_id", "dataset_id", "dataset_name"]]

    df3 = pd.json_normalize(workspaces_data)
    df3 = df3[["workspace_id", "workspace_name"]]
    
    df = pd.merge(df1, df2, on=["dataset_id", "workspace_id"], how="left")
    df = pd.merge(df, df3, on="workspace_id", how="left")
    df = df[df["report_type"] == "PowerBIReport"]
    df = df[["workspace_id", "workspace_name", "report_id", "report_name", "report_type", "dataset_id", "dataset_name", "web_url", "extract_timestamp"]]
    df["extract_timestamp"] = pd.to_datetime(df["extract_timestamp"])

    return df


def transform_report_pages(reports_pages_data, reports_data, workspaces_data):
    """
    Transform reports pages data.
    """
    df1 = pd.json_normalize(reports_pages_data)

    df2 = pd.json_normalize(reports_data)
    df2 = df2[["report_id", "workspace_id","report_name"]]

    df3 = pd.json_normalize(workspaces_data)
    df3 = df3[["workspace_id", "workspace_name"]]

    df = pd.merge(df1, df2, on=["report_id", "workspace_id"], how="left")
    df = pd.merge(df, df3, on="workspace_id", how="left")
    df = df[["workspace_id", "workspace_name", "report_id", "report_name", "page_id", "page_name", "order", "extract_timestamp"]]
    df["extract_timestamp"] = pd.to_datetime(df["extract_timestamp"])

    return df


def transform_datasets(datasets_data, workspaces_data):
    """
    Transform datasets data.
    """
    df1 = pd.json_normalize(datasets_data)

    df2 = pd.json_normalize(workspaces_data)
    df2 = df2[["workspace_id", "workspace_name"]]

    df = pd.merge(df1, df2, on="workspace_id", how="left")
    df = df[["workspace_id", "workspace_name", "dataset_id", "dataset_name", "web_url", "created_at",  "extract_timestamp"]]
    df[["created_at", "extract_timestamp"]] = df[["created_at", "extract_timestamp"]].apply(pd.to_datetime)
    df[["created_at", "extract_timestamp"]] = df[["created_at", "extract_timestamp"]].apply(lambda col: col.dt.tz_localize(None))

    return df


def resolve_workspaces_datasets_list(datasets_data, workspaces_data):
    """
    Generate a list of names and ids from workspaces and datasets.
    """
    df1 = pd.json_normalize(datasets_data)
    df1 = df1[["dataset_id", "dataset_name", "workspace_id"]]

    df2 = pd.json_normalize(workspaces_data)
    df2 = df2[["workspace_id", "workspace_name"]]
    
    df_all = pd.merge(df1, df2, on="workspace_id", how="left")
    data = df_all.to_dict(orient="records")
    return data


def transform_relationships_info(datasets_info_data):
    """
    Transform relationships info data.
    """
    df = pd.json_normalize(datasets_info_data, meta=["workspace_id", "workspace_name", "dataset_id", "dataset_name", "extract_timestamp"], record_path="info_relationships")
    cols_cleaned_names = { col : col.lstrip("[").rstrip("]") for col in df.columns if col.startswith("[") and col.endswith("]") }
    df = df.rename(columns=cols_cleaned_names)
    df = df[["workspace_id", "workspace_name", "dataset_id", "dataset_name", "from_table", "from_column", "relationship", "to_table", 
             "to_column", "is_active_flag", "modified_at", "extract_timestamp"]]
    df[["modified_at", "extract_timestamp"]] = df[["modified_at", "extract_timestamp"]].apply(pd.to_datetime)
    df[["modified_at", "extract_timestamp"]] = df[["modified_at", "extract_timestamp"]].apply(lambda col: col.dt.tz_localize(None))
    return df


def transform_tables_info(datasets_info_data):
    """
    Transform tables info data.
    """
    df = pd.json_normalize(datasets_info_data, meta=["workspace_id", "workspace_name", "dataset_id", "dataset_name", "extract_timestamp"], record_path="info_tables")
    cols_cleaned_names = { col : col.lstrip("[").rstrip("]") for col in df.columns if col.startswith("[") and col.endswith("]") }
    df = df.rename(columns=cols_cleaned_names)
    df = df[["workspace_id", "workspace_name", "dataset_id", "dataset_name", "table_name", "description", "table_type", "type", 
             "is_hidden_flag", "definition", "modified_at", "extract_timestamp"]]
    df[["modified_at", "extract_timestamp"]] = df[["modified_at", "extract_timestamp"]].apply(pd.to_datetime)
    df[["modified_at", "extract_timestamp"]] = df[["modified_at", "extract_timestamp"]].apply(lambda col: col.dt.tz_localize(None))
    return df


def transform_columns_info(datasets_info_data):
    """
    Transform columns info data.
    """
    df1 = pd.json_normalize(datasets_info_data, meta=["workspace_id", "workspace_name", "dataset_id", "dataset_name", "extract_timestamp"], record_path="info_columns")
    cols_cleaned_names = { col : col.lstrip("[").rstrip("]") for col in df1.columns if col.startswith("[") and col.endswith("]") }
    df1 = df1.rename(columns=cols_cleaned_names)

    df2 = pd.json_normalize(datasets_info_data, meta=["workspace_id", "workspace_name", "dataset_id", "dataset_name", "extract_timestamp"], record_path="info_tables")
    cols_cleaned_names = { col : col.lstrip("[").rstrip("]") for col in df2.columns if col.startswith("[") and col.endswith("]") }
    df2 = df2.rename(columns=cols_cleaned_names)
    df2 = df2[["workspace_id", "dataset_id", "table_id", "table_name"]]

    df = pd.merge(df1, df2, on=["workspace_id", "dataset_id", "table_id"], how="left")
    df = df[["workspace_id", "workspace_name", "dataset_id", "dataset_name", "table_name", "column_name", "column_type", "dax_expression", 
            "data_type", "description", "display_folder", "is_hidden_flag", "modified_at", "extract_timestamp"]]
    df[["modified_at", "extract_timestamp"]] = df[["modified_at", "extract_timestamp"]].apply(pd.to_datetime)
    df[["modified_at", "extract_timestamp"]] = df[["modified_at", "extract_timestamp"]].apply(lambda col: col.dt.tz_localize(None))
    
    return df


def transform_measures_info(datasets_info_data):
    """
    Transform measures info data.
    """
    df1 = pd.json_normalize(datasets_info_data, meta=["workspace_id", "workspace_name", "dataset_id", "dataset_name", "extract_timestamp"], record_path="info_measures")
    cols_cleaned_names = { col : col.lstrip("[").rstrip("]") for col in df1.columns if col.startswith("[") and col.endswith("]") }
    df1 = df1.rename(columns=cols_cleaned_names)

    df2 = pd.json_normalize(datasets_info_data, meta=["workspace_id", "workspace_name", "dataset_id", "dataset_name", "extract_timestamp"], record_path="info_tables")
    cols_cleaned_names = { col : col.lstrip("[").rstrip("]") for col in df2.columns if col.startswith("[") and col.endswith("]") }
    df2 = df2.rename(columns=cols_cleaned_names)
    df2 = df2[["workspace_id", "dataset_id", "table_id", "table_name"]]

    df = pd.merge(df1, df2, on=["workspace_id", "dataset_id", "table_id"], how="left")

    df = df[["workspace_id", "workspace_name", "dataset_id", "dataset_name", "table_name", "measure_name", "dax_expression", "data_type", 
             "description", "format_string", "display_folder", "is_hidden_flag", "modified_at", "extract_timestamp"]]
    df[["modified_at", "extract_timestamp"]] = df[["modified_at", "extract_timestamp"]].apply(pd.to_datetime)
    df[["modified_at", "extract_timestamp"]] = df[["modified_at", "extract_timestamp"]].apply(lambda col: col.dt.tz_localize(None))
    
    return df


def transform_calc_groups(datasets_info_data):
    """
    Transform calculation groups data.
    """
    df = pd.json_normalize(datasets_info_data, meta=["workspace_id", "workspace_name", "dataset_id", "dataset_name", "extract_timestamp"], record_path="info_calculation_groups")
    cols_cleaned_names = { col : col.lstrip("[").rstrip("]") for col in df.columns if col.startswith("[") and col.endswith("]") }
    df = df.rename(columns=cols_cleaned_names)
    df = df[["workspace_id", "workspace_name", "dataset_id", "dataset_name", "table_name", "calc_item_name", "expression", "calc_group_description", "extract_timestamp"]]
    df["extract_timestamp"] = pd.to_datetime(df["extract_timestamp"])
    return df