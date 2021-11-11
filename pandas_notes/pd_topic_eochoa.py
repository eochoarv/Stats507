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
# ### Problem Set 4
# Eduardo Ochoa Rivera \
# eochoa@umich.edu \
# October 20, 2021

# ## Module imports

import numpy as np
import pandas as pd
import datetime

# # Question 0 - Topics in Pandas [25 points]

# ## Time series / date functionality
#
# pandas contains extensive capabilities and features for working with time series data for all domains.
#
# For example: 
#
# * Parsing time series information from various sources and formats

dti = pd.to_datetime(["1/1/2018", 
                      np.datetime64("2018-01-01"), 
                      datetime.datetime(2018, 1, 1)])
dti

# * Generate sequences of fixed-frequency dates and time spans

dti = pd.date_range("2018-01-01", periods=3, freq="H")
dti

# * Performing date and time arithmetic with absolute or relative time increments. It can be specially usefull for financial data analysis.

friday = pd.Timestamp("2018-01-05")
print(friday.day_name())
saturday = friday + pd.Timedelta("1 day")
print(saturday.day_name())
monday = friday + pd.offsets.BDay()
print(monday.day_name())

# ## Timestamps vs. time spans
#
# Timestamped data is the most basic type of time series data that associates values with points in time.

pd.Timestamp(datetime.datetime(2012, 5, 1))

# However, in many cases it is more natural to associate things like change variables with a time span instead.

pd.Period("2011-01"), pd.Period("2012-05", freq="D")

# **Timestamp** and **Period** can serve as an index.

dates = [
    pd.Timestamp("2012-05-01"),
    pd.Timestamp("2012-05-02"),
    pd.Timestamp("2012-05-03"),
]
ts = pd.Series(np.random.randn(3), dates)
print(ts.index) 
ts

periods = [pd.Period("2012-01"), 
           pd.Period("2012-02"), 
           pd.Period("2012-03")]
ts = pd.Series(np.random.randn(3), periods)
print(ts.index) 
ts
