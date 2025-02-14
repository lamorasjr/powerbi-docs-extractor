# Power BI Catalog Extractor

This project automates the documentation process for Power BI reports and semantic models across multiple workspaces in the Power BI service.

### Key features include:
- **Metadata Extraction from Power BI Premium Workspaces:** For each defined workspace, the project extracts data from various components, including Workspaces, Reports, Report Pages, Semantic Models, Tables, Measures, Relationships, Calculation Groups, and Calculation Items.

- **Data Storage:** The extracted metadata is saved as CSV files in a SharePoint folder, enabling centralized access.

- **Data Catalog Management:** A Power BI integration is provided through a ready-made template, allowing for detailed reporting and analysis.


<!-- <img src=assets\pj_diagram2.png alt="pj_diagram" width="100%"/> -->


## Table of Contents
- [Requirements](#requirements)
- [Setup](#setup)
  - [Clone the repository](#1-clone-the-repository)
  - [Activate the Python version](#2-activate-the-python-version-for-the-project)
  - [Install dependencies:](#3-install-dependencies-and-run-the-application)
    - [Option 1: Option 2: Run with Pyenv and Poetry](#option-2-run-with-pyenv-and-poetry)
    - [Option 2: Run with pip (without Poetry)](#option-3-run-with-pip-without-poetry)
- [Run the project](#to-run-the-project)

## Requirements

- **Python 3.12 or greater**
- **Power BI workspace with Premium or Fabric license**.
- **[Microsoft Entra App](https://learn.microsoft.com/en-us/power-bi/developer/embedded/register-app?tabs=customers)** with at least one of the following scopes:
  - **Power BI Service**:
    - `Workspace.Read.All`
    - `Workspace.ReadWrite.All`
  - **Microsoft Graph**:
    - `User.Read`
    - `Files.ReadWrite.All`
    - `Sites.ReadWrite.All`
- **Power BI Desktop** (Required only for report templates)


## Setup
### 1. Clone the repository:
Clone the repository to your local machine:
```bash
git clone https://github.com/lamorasjr/powerbi-catalog-extractor.git

cd powerbi-catalog-extractor
```

### 2. Create the .env File:
* A `.env` file is required to run the project.
* Create a `.env` file in the root directory of the project.
* Copy the content from .env-example and update it with your Microsoft Entra app credentials, source workspaces ids, and details of the target sharepoint.

### 3. Install Dependencies and Run the Application

You can run the application using one of the following methods:

### Option 1: Run with Pyenv and Poetry (Recommended)

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

```bash
poetry run python src/main.py
```

### Option 2: Run with pip
If you prefer not to use Poetry, you can install the dependencies using pip:

#### 1. Create the .venv 
```bash
python -m venv .venv
```

#### 2. Activate the .venv
```bash
.venv\Scripts\activate
```

#### 3. Install dependencies with pip:
```bash
pip install -r requirements.txt
```

## Run the Project
#### 1. With Poetry:
```bash
poetry run python src/main.py
```

#### 2. With Pip
```bash
python src/main.py
```
