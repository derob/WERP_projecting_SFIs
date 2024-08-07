from werp_projecting_sfis.base import NAME
from werp_projecting_sfis.file_io import sfi_file_to_pandas
import os as os
from pathlib import Path
here = Path(os.path.abspath(os.path.dirname(__file__)))

def test_base():
    assert NAME == "werp_projecting_sfis"

def test_fileio():
    filename = here/"data/_MURR_B0D000__eFA_annual_stats_10discount.txt"
    output = sfi_file_to_pandas(filename)
    assert output['BMF_R1'].iloc[0] == 1.0, "Incorrect read of start year"  
    assert output.index.shape[0]== 114