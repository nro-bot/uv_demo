import pytest
from phenoxtractor import extract
from pandera.typing import Series
import pandera as pa
import pandas as pd
import re

DATA = 'asdf'

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


def test_extract():
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
    assert extract() == 1
