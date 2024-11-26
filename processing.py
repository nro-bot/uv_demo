from pathlib import Path
import pandas as pd
import re
from rich import print

SERVER = '\\\\vacrrdevmavdi01.vha.med.va.gov\\'
PROJ_HOME = 'Projects/OncApps'
USER = 'ruiouyang'
DATA_DIR = 'data/profound/annotations/'

HOME = Path(SERVER) / PROJ_HOME / DATA_DIR  

text_files = {
    'small': 'uploaded_samples/Pathology_train_supplement.csv', # 5.4k, Fulltext, Gleason bool, 40 px
    'big': 'uploaded_samples/Pathology_training_1-3_for_analysis.csv', # 19k, fulltext, gleason bool,  136 px
    '__huge': 'Gleason_Pathology_Reports_for_Annotation_no-duplicates.csv' # 2133k, fulltext, gleason bool, 144k px
}

label_files = {
    'small': 'annotated_data/adjudicated_train-supplement_gleason_2024-09-07.csv',  # 0.3k, no fulltext, gleason int, 40 px
    '_small_fulltext': text_files['small'], 
    '__':  'Pathology_validation_Gleason_2024-08-29.csv', # 0.5k, no fulltext, gleason int, 190 px 
}  


import subprocess
def print_info(fname: Path):
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

def print_files_info():
    for key, fname in text_files.items():
        if key[:2] == '__' :
            continue
        print_info(HOME / fname)

if __name__ == '__main__':
    print_files_info()