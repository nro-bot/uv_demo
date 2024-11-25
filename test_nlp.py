import pytest
import sys
import os
from pandera.typing import Series
import pandera as pa
import pandas as pd
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


sys.path.append(os.path.abspath(os.path.join("..")))
from phenoxtractor import find_gleasons 
#import phenoxtractor

def schema():
    class Schema(pa.DataFrameModel): 
        PatientICN: int = pa.Field(ge=1_000_000_000, lt=1_100_000_000), #6 digit int leading with 10
        TextSID: int = pa.Field(ge=800_000_000_000)
        Start: int
        End: int
        Text: int = pa.Field(ge=0, le=9)
        Label: pa.Fields(isin=['Gleason_total', 'Gleason_1', 'Gleason_2'])

        class Config:
            ordered = True

def test_find_gleasons():
    assert len(phenoxtractor.find_gleasons('hello world')) == 0
    assert len(phenoxtractor.find_gleasons('gleason score 3+3=6')) == 3

MOCKSID = 1231231231230
def get_mock_truth_df():
    # make dummy deF
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
    # strs = get_test_strs()
    df = pd.DataFrame(
        [
            [
                1010101010,
                1231231231230,
                """Lorem ipsum there is a Gleason 3+4=7 in this text that we are looking at and in fact there may even be a """
                """second gleason 6 (3 +3) score in the text with a gleason of 3 and 4 (7/10)""",
            ],
        ],
        columns=["PatientICN", "TIUDocumentSID", "ReportText"],
    )
    return df

 

def get_mock_results_df():
    MOCKSID = 1231231231230
    results = []
    text_df = get_mock_text_df()
    truth_df = get_mock_truth_df()
    for i, row in text_df.iterrows():
        #    print(row)
        #    print(find_gleasons(row.ReportText))
        gl = phenoxtractor.find_gleasons(row.ReportText)
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

def eval_find_gleasons():
    predicted = get_mock_results_df()

    metrics = truth_df.merge(
            predicted, on=["TextSID", "Start"], suffixes=["_True", "_Pred"],
            how="outer")

    metrics = metrics.assign(
                TP=lambda x: (x.Label_True.astype(str) == x.Label_Pred.astype(str)) & (x.Text_True == x.Text_Pred),  # str to ensure non-null
                FP=lambda x: x.Label_True.isna(),
                FN=lambda x: x.Label_Pred.isna(),
            )

    TP = sum(metrics.TP)
    FP = sum(metrics.FP)
    FN = sum(metrics.FN)
    TN = 0
    precision = TP / (TP + FP)

    print(f'{precision=}')

    recall = TP / (TP + FN)
    print(f'{recall=}')

    f1 = 2 * (precision * recall) / (precision + recall)
    print(f'{f1=}')

    conf_matrix = [[TN, FP], [FN, TP]]

    # -- Plot confusion matrix
    sns.set_theme(font="serif", context="notebook", style="darkgrid", font_scale=1.5)
    sns.heatmap(
        conf_matrix,
        annot=True,
        fmt="d",
        cmap="crest",
        linewidth=0.5,
        linecolor="gray",
        xticklabels=["None", "Gleason"],
        yticklabels=["None", "Gleason"],
        cbar=False,
        square=True,
    )

    plt.title("Confusion Matrix\n", fontdict={"weight": "bold", "size": "x-large"})
    plt.xlabel("Predicted Label", labelpad=10)
    plt.ylabel("True Label", labelpad=10)
    plt.yticks(rotation=45)
    #plt.subplots_adjust(bottom=0.5)

    plt.figtext( 0.1, 0.1, # -0.1
        f""" TP = {TP} FP = {FP}\n TN = {TN} FN = {FN}"""
        f"""\n Precision = {precision:.2f} \n Recall =    {recall:.2f}\n F1 Score =  {f1:.2f}""",
        ha="left",
        va="center",
        fontsize=8,
        font='monospace'
    )
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    eval_find_gleasons()
