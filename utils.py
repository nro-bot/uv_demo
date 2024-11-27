'''
Generate mock data for use in tests.
Run metrics.
'''
import numpy as np
import pandas as pd
from phenoxtractor import find_gleasons

MOCKSID = 1231231231230


def get_mock_truth_df():
    '''Generate mock dataframe of ground truth gleason score values.
    '''
    # make dummy df
    df = pd.DataFrame(
        [
            [1010101010, 1231231231230, 25, 3, "Gleason_1"],
            [1010101010, 1231231231230, 27, 4, "Gleason_2"],
            [1010101010, 1231231231230, 29, 7, "Gleason_total"],
            [1010101010, 1231231231230, 114, 3, "Gleason_1"],
            [1010101010, 1231231231230, 117, 3, "Gleason_2"],
            [1010101010, 1231231231230, 120, 6, "Gleason_total"],
            [1010101010, 1231231231230, 159, 3, "Gleason_1"],
            [1010101010, 1231231231230, 165, 4, "Gleason_2"],
            [1010101010, 1231231231230, 168, 7, "Gleason_total"],
        ],
        columns=["PatientICN", "TextSID", "Start", "Text", "Label"],
    ).astype({"Label": pd.StringDtype(), "Text": pd.StringDtype()})
    return df


def get_mock_text_df():
    '''Generate mock dataframe of pathology report text. 
    '''
    df = pd.DataFrame(
        [
            [
                1010101010,
                1231231231230,
                (
                    "Lorem ipsum there is a Gleason 3+4=7 in this text that we"
                    "are looking at and in fact there may even be a second"
                    "gleason 6 (3 +3) score in the text with a gleason of 3"
                    "and 4 (7/10)"
                ),
            ]
        ],
        columns=["PatientICN", "TIUDocumentSID", "ReportText"],
    )
    return df


def get_mock_results_df():
    '''Turn find_gleasons into a properly formatted dataframe and return.
    '''
    results = []
    text_df = get_mock_text_df()
    for i, row in text_df.iterrows():
        #    print(row)
        #    print(find_gleasons(row.ReportText))
        gl = find_gleasons(row.ReportText)
        gl = [[MOCKSID] + x for x in gl]
        results.extend(gl)

    results.append([MOCKSID, 1, "4", "Gleason_1", "mock text"])
    results.append([MOCKSID, 3, "4", "Gleason_2", "mock text"])
    results.append([MOCKSID, 5, "8", "Gleason_total", "mock text"])

    df = pd.DataFrame(
        np.array(results), columns=["TextSID", "Start", "Text", "Label", "Context"]
    ).astype(
        {
            "TextSID": int,
            "Start": int,
            "Text": pd.StringDtype(),
            "Label": pd.StringDtype(),
            "Context": pd.StringDtype(),
        }
    )
    return df

if __name__ == '__main__':
    pass