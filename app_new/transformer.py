import pandas as pd

def transform_workspaces(workspaces_data):
    df = pd.json_normalize(workspaces_data)
    return df


def transform_reports(reports_data, datasets_data, workspaces_data):
    df1 = pd.json_normalize(reports_data)
    
    df2 = pd.json_normalize(datasets_data)
    df2 = df2[["workspace_id", "dataset_id", "dataset_name"]]

    df3 = pd.json_normalize(workspaces_data)
    df3 = df3[["workspace_id", "workspace_name"]]
    
    df = pd.merge(df1, df2, on=["dataset_id", "workspace_id"], how="left")
    df = pd.merge(df, df3, on="workspace_id", how="left")
    df = df[df["report_type"] == "PowerBIReport"]
    df = df[["report_id", "report_name", "report_type", "dataset_id", "dataset_name", "workspace_name", "web_url", "extract_timestamp"]]

    return df


def transform_report_pages(reports_pages_data, reports_data, workspaces_data):
    df1 = pd.json_normalize(reports_pages_data)

    df2 = pd.json_normalize(reports_data)
    df2 = df2[["report_id", "workspace_id","report_name"]]

    df3 = pd.json_normalize(workspaces_data)
    df3 = df3[["workspace_id", "workspace_name"]]

    df = pd.merge(df1, df2, on=["report_id", "workspace_id"], how="left")
    df = pd.merge(df, df3, on="workspace_id", how="left")
    df = df[["workspace_name", "report_name", "page_name", "page_name", "order", "extract_timestamp"]]

    return df