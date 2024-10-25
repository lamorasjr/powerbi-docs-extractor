import os
from datasets import pipeline_datasets
from measures_info import pipeline_measures_info

if __name__ == '__main__':
    pipeline_datasets()
    pipeline_measures_info('data/datasets.csv')