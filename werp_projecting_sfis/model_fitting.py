import xarray as xr
import pymc as pymc
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import datetime
import arviz as az

from scipy.special import expit

from werp_projecting_sfis.file_io import sfi_file_to_pandas 


class sfi_prediction_model:

    def __init__(self, predictors, predictands):
        npredictors = len(predictors.columns())
        npredictands = len(predictands.columns())
        