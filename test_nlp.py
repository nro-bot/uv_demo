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

