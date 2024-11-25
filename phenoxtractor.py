import re
import pandas as pd
from rich import print 
from rich.traceback import install
install(show_locals=True)


def get_regexs():
    #_3to5_ = '[3-5]'
    _6to10_ = r'\b[6-9]|10\b'
    conjunction = r'&|and|\+'
    regex_total_last = rf'([3-5])\D*([3-5])\D*({_6to10_})'
    regex_total_first = rf'({_6to10_})\D*([3-5])\D*([3-5])'
    regex_nototal= rf'([3-5])\s*({conjunction})\s*([3-5])'

    return {
        'regex_total_last': regex_total_last,
        'regex_total_first': regex_total_first,
        'regex_nomax': regex_nototal,
    }

def find_total_last(text: str) -> list[int] | None:
    m = re.search(get_regexs()['regex_total_last'], text)
    if m:
        gleason1, gleason2, gleason_total = [int(digit) for digit in m.groups()]
        idx1, idx2, idx_total = m.start(1), m.start(2), m.start(3)
        return [idx1, idx2, idx_total, gleason1, gleason2, gleason_total]
    return None

def find_total_first(text: str) -> list[int] | None:
    m = re.search(get_regexs()['regex_total_first'], text)
    if m:
        gleason_total, gleason1, gleason2 = [int(digit) for digit in m.groups()]
        idx_total, idx1, idx2  = m.start(1), m.start(2), m.start(3)
        return [idx1, idx2, idx_total, gleason1, gleason2, gleason_total]
    return None

def find_nomax():
    return None

def find_matches(text:str):
    if vals := find_total_last(text) or find_total_first(text):
        #if checksum(*vals[3:]):
        return vals
    return None

def find_gleasons(text: str):
    text = text.lower()
    all_matches = []
    for gl in re.finditer('gleason', text):
        start = gl.start()
        context_start, context_end = \
            max(0, gl.start()-50), min(gl.end()+80, len(text))
        context = text[context_start:context_end]

        candidate = text[gl.start():context_end]

        gleason_match = find_matches(candidate)
        if gleason_match:
            idx1, idx2, idx_total, gleason1, gleason2, gleason_total = gleason_match
            # start, text, label, context
            match = [start+idx1, gleason1, 'Gleason_1', context]
            all_matches.append(match)
            match = [start+idx2, gleason2, 'Gleason_2', context]
            all_matches.append(match)
            match = [start+idx_total, gleason_total, 'Gleason_total', context]
            all_matches.append(match)

    return all_matches

def test_find_gleasons():
    for sample in get_test_strs():
        print(sample)
        print(find_gleasons(sample))


def process_report(report_df: pd.DataFrame):
    all_results = []

#def extract(doc):
    #print('Hello world from phenoxtract')

def get_mock_labels_df():
    # make dummy deF
    df = pd.DataFrame(
        [
            [1010101010, 1231231231230, 11, 3, 'Gleason_1'], 
            [1010101010, 1231231231230, 13, 4, 'Gleason_2'], 
            [1010101010, 1231231231230, 16, 7, 'Gleason_total'], 
        ],
        columns = ['PatientICN', 'TextSID', 'Start', 'Text', 'Label']
    )
    return df


def get_mock_text_df():
    strs = get_test_strs()
    df = pd.DataFrame(
        [
            [1010101010, 1231231231230, strs[0]], 
        ],
        columns = ['PatientICN', 'TIUDocumentSID', 'ReportText']
    )
    return df

def evaluate_predictions(ground_truth: pd.DataFrame, predicted_lbls: pd.DataFrame):
    y_true = ground_truth['Label']
    labels = ['Gleason_total', 'Gleason_1', 'Gleason_2']

    # test


def get_test_strs():
    str1A = 'gleason score 3+3 = 6; 3 of 3 cores; 40%'
    str1B = 'gleason score 4+4=9; one of two; 10%'
    str2 = 'gleason 3+4=7/10, involving 5% of 1/2 cores'
    str3 = 'gleason grade 3+4 \n\t (combined gleason score 7/10) involving 2 (of 2) cores'
    str4 = 'gleason scores 6/10) involving '
    str5A = 'gleason score 7 (3+4) in one of one'
    str5B = 'gleason score 9 (4+5) in one of one'
    str5C = 'adenocarcinoma, grade group 2, gleason score 7 (3+4)'
    str_8 = 'gleason pattern 4 is noted'
    str9A = "gleason's score 3+3"
    str9B = "gleason's score 4 + 3"
    str10 = "GLEASON pattern 3+4(10%)=7 (GRADE GROUP 2)."
    strs =  [str1A, str1B, str2, str3, str4, str5A, str5B, str5C, str_8,
    str9A, str9B, str10]
    return strs

def main():
    print("Designed to extract phenotypes from EHR")
    test_find_gleasons()

if __name__ == "__main__":
    main()