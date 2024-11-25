from werp_projecting_sfis.base import NAME
from werp_projecting_sfis.file_io import sfi_file_to_pandas
import os as os
from pathlib import Path
import pandas as pd

here = Path(os.path.abspath(os.path.dirname(__file__)))

def test_base():
    assert NAME == "werp_projecting_sfis"

def test_fileio():
    filename = here/"data/_MURR_B0D000__eFA_annual_stats_10discount.txt"
    output = sfi_file_to_pandas(filename)
    assert output['BMF_R1'].iloc[0] == 1.0, "Incorrect read of start year"  
    assert output.index.shape[0]== 114

def test_predictor():
    inflowfile = "/Users/26wanga/Documents/ORAC/CSIRO/MURR_P0H.csv"
    inpredictor = pd.read_csv(inflowfile)
    n = len(inpredictor['date'])
    year = 1895
    cycle = 0
    for i in range(6, n + 6):
        if (i - cycle == 12):
            cycle = i
            year += 1
        if (i % 12 + 1 < 10):
            assert str(year) + '-0' + str(i % 12 + 1) + '-01' == inpredictor['date'].iloc[i - 6], "Incorrect year"
        else:
            assert str(year) + '-' + str(i % 12 + 1) + '-01' == inpredictor['date'].iloc[i - 6], "Incorrect year"
    
