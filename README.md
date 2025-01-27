# ETL Power BI Data Catalog

This project automates the extraction of metadata from Power BI workspaces, including reports and semantic models, and stores it as CSV files in SharePoint, making them readily available for further analysis and reporting.

By enabling data catalog management, this project helps organizations and data professionals better understand and manage their assets in Power BI Service. It enhances data governance, facilitates data discovery and documentation processes, also contributing to improve the team’s overall data literacy.

The project supports execution in various environments, including Docker, Poetry with Pyenv, or pip for dependency management.

<img src=assets\pj_diagram2.png alt="pj_diagram" width="100%"/>

### Key features include:

- **Automated Metadata Extraction:** Collects metadata from multiple Power BI workspaces in the Power BI Service.

- **Data Storage:** Saves extracted metadata as CSV files in a SharePoint folder for centralized access.

- **Power BI Integration:** Provides a Power BI-ready template to enable detailed reporting and analysis.

- **Data Catalog Management:** Supports the creation and maintenance of a comprehensive data catalog for better governance.


## Table of Contents
- [Requirements](#requirements)
- [Setup](#setup)
  - [Clone the repository](#1-clone-the-repository)
  - [Activate the Python version for the project](#2-activate-the-python-version-for-the-project)
  - [Install Dependencies and Run the Application:](#3-install-dependencies-and-run-the-application)
    - [Option 1: Run with Docker (Recommended)](#option-1-run-with-docker-recommended)
    - [Option 2: Option 2: Run with Pyenv and Poetry](#option-2-run-with-pyenv-and-poetry)
    - [Option 3: Run with pip (without Poetry)](#option-3-run-with-pip-without-poetry)

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
* Create a `.env` file in the root directory of the project.
* Copy the content from .env-example and update it with your Azure application credentials, source workspaces ids, and target sharepoint details.

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
