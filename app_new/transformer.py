import pandas as pd

def transform_workspaces(workspaces_data):
    """
    Transform workspaces data.
    """
    df = pd.json_normalize(workspaces_data)
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


def unpack_dax_info_data(datasets_info_data):
    """
    Unpack records from dax info data into a dict of dataframes.
    """
    dfs = {}
    for record in datasets_info_data:
        workspace_id = record["workspace_id"]
        workspace_name = record["workspace_name"]
        dataset_id = record["dataset_id"]
        dataset_name = record["dataset_name"]
        extract_timestamp = record["extract_timestamp"]

        for key in ["info_tables", "info_partitions", "info_columns", "info_measures", "info_relationships", "info_calculationgroups", "info_calculationitems"]:
            if key in record:
                
                temp_df = pd.DataFrame(record[key])
                temp_df["workspace_id"] = workspace_id
                temp_df["workspace_name"] = workspace_name
                temp_df["dataset_id"] = dataset_id
                temp_df["dataset_name"] = dataset_name
                temp_df["extract_timestamp"] = extract_timestamp
                
                dfs[key] = temp_df
    
    return dfs


def transform_tables(datasets_info_data):
    """
    Transform datasets data.
    """
    dfs = unpack_dax_info_data(datasets_info_data)

    df1 = dfs['info_tables']
    # df1 = df1[df1["[ExcludeFromModelRefresh]"] == "false"]
    # df1 = df1[df1[["[CalculationGroupID]"]].notnull().all(1)]
    columns1 = {
        "[ID]" : "table_id",
        "[Name]" : "table_name",
        "[Description]" : "description",
        "[IsHidden]" : "is_hidden",
        "[ModifiedTime]" : "modified_at"
    }
    df1 = df1.rename(columns=columns1)
    df1 = df1[["workspace_id", "workspace_name", "dataset_id", "dataset_name","table_id", "table_name", "description", "is_hidden", "modified_at", "extract_timestamp"]]


    df2 = dfs["info_partitions"]
    columns2 = {
        "[TableID]" : "table_id",
        "[QueryDefinition]" : "query_definition",
        "[Type]" : "type"
    }
    df2 = df2.rename(columns=columns2)
    df2 = df2[["workspace_id", "dataset_id", "table_id", "query_definition", "type"]]
    df2["type"] = df2["type"].map({4: "M", 2: "DAX", 7: "Interno"})

    df = pd.merge(df1, df2, how="left", on=["workspace_id", "dataset_id", "table_id"])

    return df