import pandas as pd
import numpy as np
import pymc as pymc
from matplotlib import pyplot as plt
def sfi_file_to_pandas (filename):

    openfile = open(filename)
    inlines = openfile.readlines()

    openfile.close()
    outstruct = dict()
    sitelist = list()
    for line in inlines:
        if ("year_start" in line):
            outstruct['year_start'] = int(line.split("=")[1].split("\n")[0])
        if ("year_end" in line):
            outstruct['year_end'] = int(line.split("=")[1].split("\n")[0])
        if ("[" in line):
            sitename = line.split("[")[1].split("]")[0]
            sitelist.append(sitename)
    nlines = len(inlines)
    ln = 0
    while ln < nlines:
        flags = [ st in inlines[ln] for st in sitelist]  
        if (any(flags)):
            sitename = sitelist[ np.where(flags)[0][0]]
            nrules = int(inlines[ln+1].split("=")[1])
            rules = dict()
            for rule in range(nrules):
                linesplit = inlines[ln+2+rule].split("=")
                outlongsplit = linesplit[1].split(",")

                rules[linesplit[0]]=[float(val) for val in outlongsplit]

            outstruct[sitename] = rules
            ln = ln + nrules + 2


        ln = ln +1

    timeindex = pd.date_range(start=(str(outstruct['year_start'])+"-07-01"), 
                                end = (str(outstruct['year_end'])+"-06-30"),
                                freq = "YE-JUN")
    outstruct["time"]= timeindex


    outlist = list()
    for site in sitelist:
        outlist.append( pd.DataFrame(outstruct[site], index = timeindex))
    outdf = pd.concat(outlist, axis = 1, join='inner')
    
    return(outdf)

def predictor_to_str(annualpredictor):
    laggedinflow_predictor = annualpredictor.copy(deep=True)
    laggedtimeindex = laggedinflow_predictor.index
    laggedtimeindexstring = [ str(laggedtime.year-1) + "-" + str(laggedtime.month) + "-" + str(laggedtime.day) for laggedtime in laggedtimeindex]
    laggedinflow_predictor.index = pd.to_datetime(laggedtimeindexstring)
    laggedinflow_predictor.columns = [col +"_lagged" for col in laggedinflow_predictor.columns]
    return laggedinflow_predictor

def inpredictor_function(inflowfile):
    inpredictor = pd.read_csv(inflowfile)
    inpredictor['date'] = pd.to_datetime(inpredictor['date'])
    inpredictor.set_index('date', inplace=True)
    annualpredictor0 = inpredictor.resample("YE-JUN").sum()
    return annualpredictor0

def regression_model(data, inn, BMF):
    with pymc.Model() as binomial_regression_model_preview:
        x = pymc.Data("x", (data[inn]))
        beta0 = pymc.Normal("beta0", mu=0, sigma=100)
        beta1 = pymc.Normal("beta1", mu=0, sigma=100)
        mu = beta0 + beta1 * x
        p = pymc.Deterministic("p", pymc.math.invlogit(mu))
        print(mu, p)
        pymc.Bernoulli("y", p=p, observed=data[BMF])
    return binomial_regression_model_preview
