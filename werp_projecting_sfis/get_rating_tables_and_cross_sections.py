#!usr/bin/env python
# -*- coding: utf-8 -*-

## -- Script Meta Data --
## Author  : Julien Lerat, CSIRO L&W
## Created : 2022-08-16 Tue 05:57 PM
## Comment : Download rating curves from Water NSW
##           API reference : https://kisters.com.au/doco/hydllp.htm
##
## ------------------------------
import sys, os, re, json, math
from datetime import datetime
from pathlib import Path
from datetime import datetime
import requests
import argparse
import numpy as np
import pandas as pd
import scipy as sp
#import iutils

from tqdm import tqdm


def query2url(url, query):
    c1, c2 = "'", "\""
    txt = re.sub(c1, c2, str(query))
    return f"{url}?{txt}".strip()

def download_rating_table( site_id, url = "http://www.bom.gov.au/waterdata/services", datasource = "A", api_version = "1",discharge_code = '141'):
    query = {\
        "function": "get_effective_rating", \
        "version": api_version, \
        "params": {\
            "site_list": str(site_id), \
            "table_from": '100', \
            "table_to": discharge_code, \
            'interval': '0.01',\
            'datetime': '20240101000000',\
            'force_range' : '1',\
            'quantised' : '1',\
            'shifts' : '1'    
        }
    }
    print(query)
    req_url = query2url(url, query)
    print(req_url)
    req = requests.get(req_url)
    print(req.status_code)
    print(req)
    if req.status_code == 200:
        js = req.json()
        print(js)
        sites_keys = js['return']['sites'][0].keys()
        if 'points' in sites_keys:
            res = pd.DataFrame(js['return']['sites'][0]['points'])
            res['vf'] =  res['vf'].astype('float')
            res['vt'] =  res['vt'].astype('float')
            if (discharge_code == '141') :
                res['vt'] = res['vt']/86.4
            res['ctf']= float(js['return']['sites'][0]['ctf'])
        else:
            res = pd.DataFrame()
    else:
         res = pd.DataFrame()

    return(res)



def download_cross_section( site_id, url = "http://www.bom.gov.au/waterdata/services?", datasource = "A", api_version = "1"):
    query = {\
        "function": "get_cross_sections", \
        "version": api_version, \
        "params": {\
            "site_list": str(site_id), \
            'section_types': ['xs'], \
            'comments': 'yes',\
            'gauge_datum': 'yes',\
            'start_date': '19800101',\
            'end_date': '20240901'   
        }
    }

    req_url = query2url(url, query)
    req = requests.get(req_url)

    if req.status_code == 200:
        js = req.json()
        print(len(js['return']))
        if len(js['return']) > 0:
            if 'sections' in js['return'][0].keys():
                rs = js['return'][0]['sections']
                rskey = list(rs.keys())
                rspd = pd.DataFrame(rs[rskey[0]])
                rspd['rl'] = rspd['rl'].astype('float')
                rspd['chain'] = rspd['chain'].astype('float')
            else:
                rspd = pd.DataFrame()
        else:
            rspd = pd.DataFrame()
    else:
         rspd = pd.DataFrame()

    return(rspd)


def unify_tables(rating, cross_section):

    if rating['vf'].min() < rating['ctf'].values[0]:
        ctfoffset = 0.01 - rating['ctf'].values[0]
        offset = 0.01  - (cross_section['rl'].min() )

    else:
        ctfoffset = 0.01  - rating['vf'].min() 
        offset = 0.01  - (cross_section['rl'].min() )
   

    all_chainages = np.arange(cross_section['chain'].min(),cross_section['chain'].max(),1.0)
    interpfunc = sp.interpolate.interp1d(cross_section['chain'].values, cross_section['rl'].values ,kind='linear')
    newlevels = interpfunc(all_chainages) + offset


    print(cross_section['rl'].min() + offset, cross_section['rl'].max()+offset, offset ,rating['vf'].max()+ctfoffset, ctfoffset)
    alllevels = np.arange(cross_section['rl'].min() + offset, min(cross_section['rl'].max()+offset,rating['vf'].max()+ctfoffset), 0.01)
    #print(newlevels.min(), newlevels.max())
    #print(alllevels.min(), alllevels.max())
    pd_lvl_area = pd.DataFrame({'level':alllevels})
    pd_lvl_area['area'] = np.nan

    for lvl in pd_lvl_area['level'].values:
        diffs = lvl - newlevels
        diffs[diffs<0] = 0.0
        area = sp.integrate.trapezoid(diffs,x=all_chainages)

        i = np.where(pd_lvl_area['level']==lvl)[0]
        pd_lvl_area.loc[i,'area'] = area

    interpfunc1 = sp.interpolate.interp1d(rating['vf'].values+ctfoffset, rating['vt'].values,kind='linear')
   # print(pd_lvl_area['level'].min() , np.min(rating['vf'].values) )
    if (pd_lvl_area['level'].min() < np.min(rating['vf'].values) ):
        ii = np.where(pd_lvl_area['level']< np.min(rating['vf'].values+ctfoffset))[0]
        #print(ii)
        pd_lvl_area.loc[ii,'level'] = np.min(rating['vf'].values+ctfoffset)
    pd_lvl_area['discharge'] = interpfunc1(pd_lvl_area['level'])
    pd_lvl_area['velocity'] = pd_lvl_area['discharge']/pd_lvl_area['area']
    ii = np.where(pd_lvl_area['area'] < 0.001 )[0]
    pd_lvl_area.loc[ii,'velocity'] = 0.0
    pd_lvl_area.loc[pd_lvl_area['discharge'] <0.005,'velocity'] = 0.0
    pd_lvl_area.loc[pd_lvl_area['discharge'] <0.005,'discharge'] = 0.0
    return(pd_lvl_area)
