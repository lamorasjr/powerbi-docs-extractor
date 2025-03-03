# Power BI Catalog Extractor

This project automates the documentation process for Power BI reports and semantic models across multiple workspaces in the Power BI service.


## Requirements

- **Python 3.12 or greater**
- Power BI workspace with **Premium or Fabric license**.
- **[Microsoft Entra App](https://learn.microsoft.com/en-us/power-bi/developer/embedded/register-app?tabs=customers)** with at least one of the following scopes:
  - **Power BI Service** - to extract Power BI metadata:
    - `Workspace.Read.All`
    - `Workspace.ReadWrite.All`
  - **Microsoft Graph** - to upload to Sharepoint:
    - `User.Read`
    - `Files.ReadWrite.All`
    - `Sites.ReadWrite.All`


## Setup
### 1. Clone thiss repository:

```bash
git clone https://github.com/lamorasjr/powerbi-catalog-extractor.git
```
```bash
cd powerbi-catalog-extractor
```

### 2. Create the .env File:
* A `.env` file is required to run the project.
* Create a `.env` file in the root directory of the project.
* Copy the content from .env-example
* Update it with your Microsoft Entra app credentials and details of the target Sharepoint folder.

### 3. Install the project dependencies

### Option 1: Pyenv and Poetry (Recommended)

#### 1. Install Python with Pyenv:
Install the required Python version (3.12.6) with Pyenv:
```bash
pyenv install 3.12.6
```

#### 2. Activate the Python version required:
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

## 4. Run the Project
#### 1. With Poetry:
```bash
poetry run python main.py
```

#### 2. With Pip
```bash
python main.py
```
