# Extract Power BI Datasets Info

## Introduction
Project to extract metadata from Power BI datasets for a given Power BI Service workspace via Power BI Rest API and export to a excel file.

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