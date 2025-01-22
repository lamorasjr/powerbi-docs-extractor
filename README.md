# Power BI Data Catalog Extractor

## Introduction
This project provides a Python script designed to extract metadata from Power BI reports and datasets across specified Power BI Service workspaces using the Power BI REST API. The extracted data can be exported in either CSV or Parquet format to a designated output directory.

Once exported, the data can be loaded into Power BI for further analysis, supporting data catalog management and enabling insights into the Power BI assets within your environment.

It supports running in different environments using Docker, Poetry with Pyenv, or pip for dependency management.

### Key Features:
* **Extract metadata:** Retrieve metadata from multiple Power BI Service workspaces using the Power BI REST API.
* **Export options:** Export the metadata to CSV or Parquet formats.
* **Power BI integration:** Load the exported data into Power BI Desktop for data catalog analysis and reporting.

## Requirements

- **Python 3.12 or greater**
- **[Azure AD application](https://learn.microsoft.com/en-us/power-bi/developer/embedded/register-app?tabs=customers)** with at least one of the following scopes:
  - Power BI Service:
    - `Workspace.Read.All`
    - `Workspace.ReadWrite.All`
  - Microsoft Graph:
    - `User.Read`
    - `Files.ReadWrite.All`
    - `Sites.ReadWrite.All`
- **Power BI Desktop** (Required only for report templates)
- **Docker** (Optional but recommended for containerized deployment)

## Setup
### 1. Clone the repository:
Clone the repository to your local machine:
```bash
git clone https://github.com/lamorasjr/extract-powerbi-datasets-info.git

cd extract-powerbi-datasets-info
```

### 2. Create the .env File:
* A `.env` file is required to run the project.
* Create a .env file in the root directory of the project.
* Copy the content from .env-example and update it with your Azure AD application credentials, target workspaces ids, sharepoint information and app configuration.

### 3. Install Dependencies and Run the Application

You can run the application using one of the following methods:

### Option 1: Run with Docker (Recommended)


### Option 2: Run with Pyenv and Poetry

#### 1. Install Python with Pyenv:
Install the required Python version (3.12.6) with Pyenv:
```bash
pyenv install 3.12.6
```

#### 2. Activate the Python version for the project:
```bash
pyenv local 3.12.6
```

#### 3. Install dependencies with Poetry:
if you don't have it yet. First, install Poetry, then install the dependencies.
```bash
poetry install
```

#### 4. Activate the Poetry virtual environment:
```bash
poetry shell
```

5. Run the application:
```bash
poetry run python src/main.py
```

### Option 3: Run with pip (without Poetry)
If you prefer not to use Poetry, you can install the dependencies using pip:

#### 1. Install dependencies with pip:
```bash
pip install -r requirements.txt
```

#### 2. Run the application:
```bash
python main.py
```