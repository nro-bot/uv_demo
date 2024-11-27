import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import utils

def eval_gleason_model(truth_df: pd.DataFrame | None, predictions_df: pd.DataFrame | None)-> None:

    """
    Evaluates the performance of a Gleason score prediction model using precision, recall, and F1 score.

    The function compares predicted and true labels, computes metrics (TP, FP, FN), and displays:
    - Precision, recall, and F1 score.
    - A confusion matrix plot.

    Args:
        mock (bool): If True, uses mock data for evaluation. Defaults to True.
    """
    if truth_df is None: 
        truth_df = utils.get_mock_truth_df()
    if predictions_df is None:
        predicts_df = utils.get_mock_results_df()


    metrics = truth_df.merge(
        predicts_df, on=["TextSID", "Start"], suffixes=["_True", "_Pred"], how="outer"
    )

    metrics = metrics.assign(
        TP=lambda x: (x.Label_True.astype(str) == x.Label_Pred.astype(str))
        & (x.Text_True == x.Text_Pred),  # str to ensure non-null
        FP=lambda x: x.Label_True.isna(),
        FN=lambda x: x.Label_Pred.isna(),
    )

    TP = sum(metrics.TP)
    FP = sum(metrics.FP)
    FN = sum(metrics.FN)
    TN = 0
    precision = TP / (TP + FP)
    print(f"{precision=}")

    recall = TP / (TP + FN)
    print(f"{recall=}")

    f1 = 2 * (precision * recall) / (precision + recall)
    print(f"{f1=}")

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
    # plt.subplots_adjust(bottom=0.5)

    plt.figtext(
        0.1,
        0.1,  # -0.1
        f""" TP = {TP} FP = {FP}\n TN = {TN} FN = {FN}"""
        f"""\n Precision = {precision:.2f} \n Recall =    {recall:.2f}\n F1 Score =  {f1:.2f}""",
        ha="left",
        va="center",
        fontsize=8,
        font="monospace",
    )
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    pass