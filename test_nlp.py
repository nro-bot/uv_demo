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
                ],
            ),
        },
        strict=False,
    )  # Mandate columns exactly match, no more no less
    #'End': pa.Column(int),
    mock_truth_df = get_mock_truth_df()
    print(mock_truth_df)
    assert isinstance(schema.validate(mock_truth_df), pd.DataFrame)


def eval_find_gleasons():
    predicted = get_mock_results_df()
    truth_df = get_mock_truth_df()

    metrics = truth_df.merge(
        predicted, on=["TextSID", "Start"], suffixes=["_True", "_Pred"], how="outer"
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


if __name__ == "__main__":
    eval_find_gleasons()


# def test_truth_df_schema_v2():
# # Use dataclass-inspired format of pandera
# class TruthLabelSchema(pa.DataFrameModel):
# PatientICN: int = pa.Field(ge=1_000_000_000, lt=1_100_000_000), #6 digit int leading with 10
# TextSID: int = pa.Field(ge=800_000_000_000)
# Start: int
# End: int
# Text: int = pa.Field(ge=0, le=9)
# Label: pa.Field(isin=['Gleason_total', 'Gleason_1', 'Gleason_2'])

# class Config:
# ordered = True

# truth_df = get_mock_truth_df()
# assert isinstance(TruthLabelSchema.validate(truth_df), pd.DataFrame)
