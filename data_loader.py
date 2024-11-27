"""
Handle file inputs, including default file paths. 
"""

from pathlib import Path
import pandas as pd
import re
from rich import print
from typing import Tuple

SERVER = '\\\\vacrrdevmavdi01.vha.med.va.gov\\'
PROJ_HOME = 'Projects/OncApps/data/profound/'
DATA_DIR = 'annotations/'
USER = 'ruiouyang/'

HOME = Path(SERVER) / PROJ_HOME / DATA_DIR  

def get_path_consts():
    TEXT_FILES = {
        'small': 'uploaded_samples/Pathology_train_supplement.csv', # 5.4k, Fulltext, Gleason bool, 40 px
        # - PatientICN, ..., TIUDocumentSID, ..., ReportText, Gleason (bool), cores (bool)

        'big': 'uploaded_samples/Pathology_training_1-3_for_analysis.csv', # 19k, fulltext, gleason bool,  136 px

        '__huge': 'Gleason_Pathology_Reports_for_Annotation_no-duplicates.csv' # 2133k, fulltext, gleason bool, 144k px
    }

    LABEL_FILES = {
        'small': 'annotated_data/adjudicated_train-supplement_gleason_2024-09-07.csv',  # 0.3k, no fulltext, gleason int, 40 px
        # - PatientICN, TextSID, Start, ..., Text, Label
        # - where Text = extracted score

        '_small_fulltext': TEXT_FILES['small'], 
        'medium':  'Pathology_validation_Gleason_2024-08-29.csv', # 0.5k, no fulltext, gleason int, 190 px 
        '_medium_fulltext': TEXT_FILES['small']
    }  

def get_data(files_dict_key='small') -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load text and label data from CSV files (from hardcoded paths), loading small files by default.
    Normalize column names before returning dataframes. 

    Returns:
        The text and label DataFrames.

    Args:
        path_dict_key (str): Must be a key in LABEL_FILES.
    """


    TEXT_FILES, LABEL_FILES = get_path_consts() 

    labels = pd.read_csv(HOME / LABEL_FILES[files_dict_key])
    text = pd.read_csv(HOME / LABEL_FILES[f'__{files_dict_key}__']) 

    norm = {
        'TIUDocumentSID':'TextSID', 
    }

    labels = labels.rename(columns=norm)
    text = text.rename(columns=norm)

    text = text[['PatientICN', 'TextSID', 'ReportText']]
    labels = labels[['PatientICN', 'TextSID', 'Start', 'Text', 'Label']]

    return text, labels


def print_csv_info(fname: Path):
    '''
    Print basic information about a csv file with a PatientICNs column.
    
    Args:
        fname (Path): The path to the file being processed.

    Prints
        1. First line of file, using `head` (the column names)
        2. Column names and first row of values, using pandas
        3. Total number of row (lines) in file, using `wc` 
        4. Number of unique PatientICNs, using pandas

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file does not contain a `PatientICN` column or is not formatted properly for pandas.
    '''
    import subprocess
    print()
    print('----------------------')
    print(fname)
    if fname.is_file():
        print('HEAD -n 1: ', 
            subprocess.run(['head', '-n', '1', fname], capture_output=True, text=True).stdout
        )
        print('DF: ', 
            pd.read_csv(fname, nrows=2)
        )
        print('NUM LINES: ', 
            subprocess.run(['wc', '-l', fname], capture_output=True, text=True).stdout.split()[0]
        )
        print('NUM UNIQUE PX: ', 
            len(pd.read_csv(fname).value_counts(subset='PatientICN'))
        )

def print_csvs_info(skip_large_files=True):
    """
    Prints information about csvs in the hardcoded `text_files` dict.

    Args:
        skip_large_files (bool): If True, skips files with keys starting with '__'.
    """
    for key, fname in TEXT_FILES.items():
        if skip_large_files and key[:2] == '__' :
            continue
        print_info(HOME / fname)

if __name__ == '__main__':
    print_csvs_info()