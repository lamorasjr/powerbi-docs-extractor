# Power BI Catalog Extractor
This project automates the documentation process of Power BI reports and semantic models by extracting metadata from multiple Power BI Workspaces, converting it into a .xlxs file and loading into a Sharepoint folder or local directory.

## Key features:
- `main.py` - main script to execute the whole process Power BI docs extraction.
- `extract_powerbi_api.py` - connects to Power BI Rest API endpoints within using Service Principal and extracts metadata of Workspaces, Reports, Reports Pages and Semantic Models.
- `extract_dax_info_tables.py` - connects to Power BI Premium Workspaces by using XMLA endpoint connectivity through DAX Studio CMD (Portable) and extracts DAX Info functions data from Power BI Semantic Models.
- `transformer.py` - transforms, combine and prepare raw data for loading.
- `loader.py` - connects to Sharepoint via Microsoft Graph API and enable load of files to a Sharepoint folder in a site.
- `dax_info_queries.dax`- DAX scripts to query Power BI Semantic Model info about tables, columns, measures, calculation groups and relationships.
- `dax_studio_setup.py` - checks if Dax Studio CMD (Portable) is avaliable in the local directory, otherwise it downloads from the source Github.


## Requirements
- **Python 3.12 or greater**
- Power BI workspace with at least **a Premium or a Fabric license**.
- **[Power BI Rest API access with Service Principal](https://learn.microsoft.com/en-us/power-bi/developer/embedded/embed-service-principal?tabs=azure-portal)**
  - Required scope for Power BI Rest API:
    - `Workspace.Read.All`
    - `Workspace.ReadWrite.All`
  - Required scope for Microsoft Graph API (Sharepoint upload):
    - `User.Read`
    - `Files.ReadWrite.All`
    - `Sites.ReadWrite.All`


## How to run this project?
### 1. Install the requirements

#### 1.1. Clone this repository in your local machine:

```bash
git clone https://github.com/lamorasjr/powerbi-docs-extractor.git
```
```bash
cd powerbi-docs-extractor
```

1.2. Create the `.env` file with a copy of the content from `.env-example`
* The `.env` file is required to run the project.
* For a quick run - create the `.env` file in the root directory of the project.
* Copy the content from .env-example.
* Update the enviroments variables required to run this project.

#### 1.3. Install the project dependencies

**Option 1: Running with Pyenv and Poetry (Recommended)**

1. Install the required Python version Python with Pyenv:
```bash
pyenv install 3.12.6
```

2. Activate the Python version required:
```bash
pyenv local 3.12.6
```

3. Install dependencies with Poetry:
```bash
poetry install
```

4. Activate the Poetry virtual environment:
```bash
poetry shell
```

5. Check if Dax Studio is set up:
```bash
poetry run python src/dax_studio_setup.py
```

**Option 2: Running with with pip**
If you prefer not to use Poetry, you can install the dependencies using pip:

1. Create the .venv 

```bash
python -m venv .venv
```

2. Activate the .venv

```bash
.venv\Scripts\activate
```

3. Install dependencies with pip:

```bash
pip install -r requirements.txt
```

4. Check if Dax Studio is set up:
```bash
python src/dax_studio_setup.py
```

### 2. Running the project

1. With Poetry:
```bash
poetry run python main.py
```

2. With pip:
```bash
python main.py
```

> [!IMPORTANT]
> To run this project and extract the output file locally, you must update both variables `LOCAL_EXTRACT`and `LOCAL_OUTPUT_DIR` in the `.env` file. 
> As default `LOCAL_OUTPUT_DIR`is set as "N" and you must update to "Y".

## Licensing
...

## Contributing
...