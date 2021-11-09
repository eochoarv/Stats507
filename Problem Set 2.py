# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Statistics 507
# ## Fall 2021
# ### Problem Set 2
# Eduardo Ochoa Rivera \
# October 1, 2021

# ## Module imports

import numpy as np
from numpy import random
import pandas as pd
from IPython.core.display import Markdown
from collections import defaultdict
from timeit import Timer
import re
from os.path import exists
import os


# # Question 3 - [30 points]

def download_read_file(file_name, link):
    '''
    Function that look for the file's name to read it. It it doesn't 
    find it, download the file and save it as csv.

    Parameters
    ----------
    file_name : (str)
        Name of the file.
    link : (str)
        Link to download the file from internet.

    Returns
    -------
    DataFrame.

    '''
    if exists(file_name):
        try:
            return pd.read_sas(file_name)
        except:
            return pd.read_csv(file_name)
    else:
        file = pd.read_sas(link)
        file.to_csv(file_name)
        return file


path = '/Users/eochoa/Downloads/'
os.chdir(path)

# ### a) Demographic data

# +
list_filenames_demo = ['DEMO_G.XPT', 
                       'DEMO_H.XPT',
                       'DEMO_I.XPT',
                       'DEMO_J.XPT']

list_link_demo = ['https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/DEMO_G.XPT',
                  'https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/DEMO_H.XPT',
                  'https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/DEMO_I.XPT',
                  'https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/DEMO_J.XPT']

list_cohort_demo = ['2011-2012',
                    '2013-2014',
                    '2015-2016',
                    '2017-2018']

col_ids_demo = ['SEQN', 'RIDAGEYR', 'RIDRETH3', 'DMDEDUC2', 'DMDMARTL', 
            'RIDSTATR', 'SDMVPSU', 'SDMVSTRA', 'WTMEC2YR', 'WTINT2YR', 
            'cohort']

col_names_demo =['unique_ids', 'age', 'race_ethnicity', 
                 'education', 'marital_status', 
                 'interview_status', 
                 'masked_variance_pseudo_PSU',
                 'masked_variance_pseudo_stratum', 
                 'MEC_exam_weight',
                 'interview_weight', 'cohort']

col_dict_demo = {i: n for i,n in zip(col_ids_demo, col_names_demo)}

value_des_race = {1: 'Mexican American',
                  2: 'Other Hispanic',
                  3: 'Non-Hispanic White',
                  4: 'Non-Hispanic Black',
                  6: 'Non-Hispanic Asian',
                  7: 'Other Race - Including Multi-Racial'}

value_des_edu = {1: 'Less than 9th grade',
                 2: '9-11th grade (Includes 12th grade with no diploma)',
                 3: 'High school graduate/GED or equivalent',
                 4: 'Some college or AA degree',
                 5: 'College graduate or above',
                 7: 'Refused',
                 9: 'Dont Know'}

value_des_marit = {1: 'Married',
                   2: 'Widowed',
                   3: 'Divorced',
                   4: 'Separated',
                   5: 'Never married',
                   6: 'Living with partner',
                   77: 'Refused',
                   99: 'Dont Know'}

value_des_interv = {1: 'Interviewed only',
                    2: 'Both interviewed and MEC examined'}

# +
df_demo = pd.DataFrame()

for f,l,c in zip(list_filenames_demo, 
                 list_link_demo, 
                 list_cohort_demo):
    _ = download_read_file(f, l)
    _['cohort'] = c
    df_demo = df_demo.append(_)
    
df_demo = df_demo.loc[:, col_ids_demo]
df_demo = df_demo.rename(columns=col_dict_demo)
df_demo = df_demo.reset_index(drop=True)

df_demo.loc[:,'unique_ids':'age'] = df_demo.loc[:,'unique_ids':
                                                'age'].astype('int')

df_demo['education'] = pd.Categorical(df_demo['education'].
                                      replace(value_des_edu))

df_demo['race_ethnicity'] = pd.Categorical(df_demo['race_ethnicity'].
                                      replace(value_des_race))

df_demo['marital_status'] = pd.Categorical(df_demo['marital_status'].
                                      replace(value_des_marit))

df_demo['interview_status'] = pd.Categorical(df_demo['interview_status'].
                                      replace(value_des_interv))

df_demo.to_feather('DEMO.feather')
# -


# ### b) Oral health and dentition data

# +
list_filenames_oral_h = ['OHXDEN_G.XPT', 
                         'OHXDEN_H.XPT',
                         'OHXDEN_I.XPT',
                         'OHXDEN_J.XPT']

list_link_oral_h = ['https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/OHXDEN_G.XPT',
                    'https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/OHXDEN_H.XPT',
                    'https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/OHXDEN_I.XPT',
                    'https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/OHXDEN_J.XPT']

list_cohort_oral_h = ['2011-2012',
                      '2013-2014',
                      '2015-2016',
                      '2017-2018']

value_des_dent = {1: 'Complete',
                  2: 'Partial',
                  3: 'Not_Done'}

value_des_tooth = {1: 'Primary tooth (deciduous) present',
                  2: 'Permanent tooth present',
                  3: 'Dental implant',
                  4: 'Tooth not present',
                  5: 'Permanent dental root fragment present',
                  9: 'Could not assess'}

value_des_coronal = {'A': 'Primary tooth with a restored surface condition',
                     'D': 'Sound primary tooth',
                     'E': 'Missing due to dental disease',
                     'F': 'Permanent tooth with a restored surface condition',
                     'J': 'Permanent root tip is present but no restorative replacement is present',
                     'K': 'Primary tooth with a dental carious surface condition',
                     'M': 'Missing due to other causes',
                     'P': 'Missing due to dental disease but replaced by a removable restoration',
                     'Q': 'Missing due to other causes but replaced by a removable restoration',
                     'R': 'Missing due to dental disease but replaced by a fixed restoration',
                     'S': 'Sound permanent tooth',
                     'T': 'Permanent root tip is present but a restorative replacement is present',
                     'U': 'Unerupted',
                     'X': 'Missing due to other causes but replaced by a fixed restoration',
                     'Y': 'Tooth present, condition cannot be assessed',
                     'Z': 'Permanent tooth with a dental carious surface condition'}

# +
df_oral_h = pd.DataFrame()

for f,l,c in zip(list_filenames_oral_h, 
                 list_link_oral_h, 
                 list_cohort_oral_h):
    _ = download_read_file(f, l)
    _['cohort'] = c
    df_oral_h = df_oral_h.append(_)
    
regex_variables = re.compile("OHX\d{2}TC|OHX\d{2}CTC")
col_ids_oral_h = ['SEQN', 'OHDDESTS']
col_ids_oral_h = col_ids_oral_h + list(filter(regex_variables.match, 
                                              list(df_oral_h.columns)))
col_names_oral_h = ['unique_ids', 'dentition_status_code']
col_names_oral_h = col_names_oral_h + ['tooth_counts_'+x[3:5] 
                                       if len(x)==7 
                                       else 'coronal_cavities_'+x[3:5] 
                                       for x in col_ids_oral_h[2:]]

col_dict_oral_h = {i: n for i,n in zip(col_ids_oral_h, 
                                       col_names_oral_h)}

df_oral_h = df_oral_h.loc[:, col_ids_oral_h]
df_oral_h = df_oral_h.rename(columns=col_dict_oral_h)
df_oral_h = df_oral_h.reset_index(drop=True)

u_ids = 'unique_ids'
ft_c = 'coronal_cavities_02'
lt_c = 'coronal_cavities_31'
dent = 'dentition_status_code'
df_oral_h.loc[:, u_ids] = df_oral_h.loc[:, u_ids].astype('int')
df_oral_h.loc[:, ft_c:lt_c] = df_oral_h.loc[:, ft_c:lt_c].astype('str')
df_oral_h[dent] = pd.Categorical(df_oral_h[dent].replace(value_des_dent))

for n in col_names_oral_h:
    if(n[:5]=='tooth'):
        df_oral_h[n] = pd.Categorical(df_oral_h[n].
                                      replace(value_des_tooth))
    elif(n[:5]=='coron'):
        df_oral_h[n] = df_oral_h[[n]].applymap(lambda x: x[2] 
                                               if x != "b''" 
                                               else float("NaN"))
        df_oral_h[n] = pd.Categorical(df_oral_h[n].
                                      replace(value_des_coronal))
        
df_oral_h.to_feather('OHXDEN.feather')
# -

# ### c) Number of cases in datasets

string_demo = 'Number of cases in the demographic datasets: '
string_or_h = 'Number of cases in the health and dentition datasets: ' 

print(string_demo + str(df_demo.shape[0]))
print(string_or_h + str(df_oral_h.shape[0]))
