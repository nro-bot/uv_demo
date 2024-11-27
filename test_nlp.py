'''
Stub Pytest file. Currently checks dataframe schema (typing) and tests regexs.
'''
import matplotlib.pyplot as plt
import pandas as pd
import pandera as pa
import seaborn as sns

from phenoxtractor import find_gleasons
from utils import get_mock_results_df, get_mock_truth_df


# def schema():
def test_find_gleasons():
    assert len(find_gleasons("hello world")) == 0
    assert len(find_gleasons("gleason score 3+3=6")) == 3


def test_truth_df_schema():
    schema = pa.DataFrameSchema(
        {
            "PatientICN": pa.Column(
                int,
                checks=[
                    pa.Check(lambda x: 1_000_000_000 <= x),
                    pa.Check(lambda x: x < 1_100_000_000),
                ],
            ),
            "TextSID": pa.Column(int, checks=pa.Check.ge(800_000_000_000)),
            "Start": pa.Column(int),
            "Text": pa.Column(
                pd.StringDtype(),
                checks=[
                    pa.Check(lambda x: 0 <= x.astype(int)),
                    pa.Check(lambda x: x.astype(int) <= 9),
                ],
            ),
            "Label": pa.Column(
                pd.StringDtype(),
                checks=[
                    pa.Check(lambda x: x.isin(["Gleason_total", "Gleason_1", "Gleason_2"]))
                ]
            ),
        },
        strict=False,
    )  # Mandate columns exactly match, no more no less
    #'End': pa.Column(int),
    mock_truth_df = get_mock_truth_df()
    print(mock_truth_df)
    assert isinstance(schema.validate(mock_truth_df), pd.DataFrame)

# Mapping TextSID : TIUDocumentSID, 'Start'


if __name__ == "__main__":
    pass

