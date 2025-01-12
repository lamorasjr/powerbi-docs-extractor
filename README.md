# Power BI Data Catalog 

## Introduction
This project contains a Python script for extracting metadata from Power BI reports and datasets within specified Power BI Service workspaces using the REST API. The data can be exported to "CSV" or "Parquet" in a given output directory and loaded into the Power BI report to enable data catalog management and analysis of your Power BI assets contained in your Power BI environment.

Key Features:
* Extracts metadata from Power BI Service workspaces using the REST API.
* Supports exporting data to CSV or Parquet formats.
* Integration with Power BI desktop for Data Catalog analysis and reporting.

## Requirements
* Pyenv
* Poetry
* Power BI access token

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/lamorasjr/extract-powerbi-datasets-info.git

    cd extract-powerbi-datasets-info
    ```

2. Install the required Python version with Pyenv:
    ```bash
    pyenv install 3.12.6
    ```

3. Activate the Python version into the local repository:
    ```bash
    pyenv local 3.12.6
    ```

4. Create the virtual enviroment and install the dependencies with Poetry:
    ```bash
    poetry install
    ```

5. Activate the virtual environment:
    ```bash
    poetry shell
    ```

5. Run the script using Python:

    ```bash
    poetry run python <place_holder>
    ```
