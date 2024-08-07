import pandas as pd
import numpy as np
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
