from werp_projecting_sfis.base import NAME
from werp_projecting_sfis.file_io import sfi_file_to_pandas, inpredictor_function, predictor_to_str, regression_model
import os as os
from pathlib import Path
import pandas as pd
import numpy as np
import pymc as pymc
import arviz as az
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
    
def test_lagged_inflow():
    laggedinflow_predictor = predictor_to_str(inpredictor_function("/Users/26wanga/Documents/ORAC/CSIRO/MURR_P0H.csv"))
    assert laggedinflow_predictor['inflow_lagged'].iloc[0] == 8322251.0, "Incorrect inflow"

def test_regression():
    filename1 = r"/Users/26wanga/Documents/ORAC/CSIRO/_MURR_P0H000__eFA_annual_stats_10discount.txt"
    outdf1 = sfi_file_to_pandas(filename1)
    outdf1['ewater'] = 2750.0
    outdf = outdf1.copy(deep=True)
    newinpredictor = inpredictor_function("/Users/26wanga/Documents/ORAC/CSIRO/MURR_P0H.csv")
    newinpredictor['ewater'] = 2750.0
    annualpredictor = newinpredictor.copy(deep=True)
    data = pd.concat([annualpredictor['inflow'],outdf['BMF_R1']],axis=1, join='inner')
    data['inflow'] = np.log(data['inflow']/1000000)
    data = data.reset_index()[data.columns[-2:]]
    data = data.sort_values(by = 'inflow')
    binomial_regression_model = regression_model(data, 'inflow', 'BMF_R1')
    with binomial_regression_model:
        idata = pymc.sample(2000, tune=4000, chains=4)
        posterior_means = idata.posterior.mean(dim=["chain", "draw"])
        beta1_mean = posterior_means['beta1'].values
    assert len(idata.posterior.coords["chain"]) == 4, "wrong number of chains"
    assert len(idata.posterior.coords["draw"]) == 2000, "wrong number of draws"
    assert beta1_mean > 0, "negative mean"
    assert idata.posterior.draw.values.min() == 0, "start year incorrect"
    assert idata.posterior.draw.values.max() == 1999, "end year incorrect"  
    assert idata.posterior.p_dim_0.values.min() == 0, "start p_dim_0 incorrect"
    assert idata.posterior.p_dim_0.values.max() == 113, "end p_dim_0 incorrect"

