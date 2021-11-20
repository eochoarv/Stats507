# ---
# jupyter:
#   jupytext:
#     cell_metadata_json: true
#     notebook_metadata_filter: markdown
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

# ## Topics in Pandas
# **Stats 507, Fall 2021** 
#   

# ## Contents
#
# + [Dropping](#Dropping) 
# + [Pandas Aggregation](#Pandas-Aggregation)
# + [Pandas with Time](#Pandas-with-Time)
# + [Window Functions](#Window-Functions) 
# + [Rolling Functions](#Rolling-Functions) 
# + [Expanding Functions](#Expanding-Functions) 
# + [Time series](#Time-series)
# + [Timestamps vs time spans](#Timestamps-vs-time-spans)

# ## Dropping
#
# __Pengfei Liu__    
# 2021/11/16

# ## Dropping In Pandas
# - Delete (some parts of) data samples under certain conditions using `pd.drop()`.
# - Use `axis` to choose to drop from the index(`0` or `index`) or columns(`1` or `columns`).
# - General usage: `df.drop(df[<some boolean condition>].index)`

import numpy as np
import pandas as pd
df1 = pd.DataFrame(np.arange(24).reshape(6, 4), columns=['A', 'B', 'C', 'D'])
print(df1)
#drop columns
print(df1.drop(['B','C'], axis = 1))
#drop the items that is less than 6 in column A.
print(df1.drop(df1[df1['A'] < 6].index))

# - In the previous test, we showed the importance of `labels`, which was `df1[df1['A'] < 6].index` there.
# - we can also use the parameter `level` to make multiple indexing.
#

midx = pd.MultiIndex(levels=[['lama', 'cow', 'falcon'],
                             ['speed', 'weight', 'length']],
                     codes=[[0, 0, 0, 1, 1, 1, 2, 2, 2],
                            [0, 1, 2, 0, 1, 2, 0, 1, 2]])
df = pd.DataFrame(index=midx, columns=['big', 'small'],
                  data=[[45, 30], [200, 100], [1.5, 1], [30, 20],
                        [250, 150], [1.5, 0.8], [320, 250],
                        [1, 0.8], [0.3, 0.2]])
print(df)
print(df.drop(index = 'cow', columns = 'small'))

# - We also have other relative functions such as `pd.dropna()` and `pd.drop_duplicates()`.

# ## Pandas Aggregation
#
# __LiHsuan Lin__    
# 2021/11/16

# ####  An essential piece of analysis in large dataset is efficient summarization
# #### There are a few aggregation operations in Pandas that are useful
# #### Aggregate using one or more operations over the specified axis

# +


# create df
df = pd.DataFrame([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9],
                   [np.nan, np.nan, np.nan]],
                  columns=['A', 'B', 'C'])
df

# +


# sum and min aggregation operation
df.agg(['sum', 'min'])


# ### Normally, it is used hand in hand with group_by to find the aggregation on groups
# 
# - first specify the column (group) and then apply agg

# +


# create example df
data1 = {'Name':['Max', 'Bill', 'Max', 'Princi', 
                 'Gaurav', 'Bill', 'Princi', 'Tom'], 
        'salary(K)':[80, 78, 56, 110, 
               78, 87, 150, 32], 
        'Address':['Nagpur', 'Kanpur', 'Allahabad', 'Kannuaj',
                   'Jaunpur', 'Kanpur', 'Allahabad', 'Aligarh'], 
        'Qualification':['MS', 'MA', 'MCA', 'Phd',
                         'B.Tech', 'Phd', 'MA', 'MS']}
df = pd.DataFrame(data1)
df

# +


# group by Name
df.groupby(['Name']).mean()

# +


df.groupby(['Name','Qualification']).sum()


# - multiple aggregrations
# - use {Column:Operation} to specify the group and which operations to use

# +


df.groupby('Name').agg({'salary(K)':['min', 'max']})
# -

# ## Pandas with Time
# *Stats 507, Fall 2021*  
#    
# __Jinhuan Ke__  
# jhgoblue@umich.edu  
# 10/19/2021
#   
# - Timestamp
# - Period
# - DatetimeIndex and PeriodIndex
# - Generating ranges of timestamps

import pandas as pd
import numpy as np
import datetime

# ## Timestamp
# - Timestamped data is the most basic type of time series data that associates values with points in time. 
# - For pandas objects it means using the points in time.
# - use `pd.Timestamp()` to generate time series data save in seconds.
# - time variable can be `year, month, day` or `"year-month=day"`.

print(pd.Timestamp("2021-10-21"))
print(pd.Timestamp(2021, 10, 21))

# ## Period
# - Time spans can be represented by `Period`.
# - use `pd.Period()` to generate time span variables.
# - the `freq` parameter in the function specify the frequency of the time series.

print(pd.Period("2021-10-21", freq='Y'))
print(pd.Period("2021-10-21", freq='M'))
print(pd.Period("2021-10-21", freq='D'))

# ## DatetimeIndex and PeriodIndex
# - Timestamp and Period can serve as an index. 
# - Lists of Timestamp and Period are automatically coerced to DatetimeIndex and PeriodIndex respectively.

dates = [
    pd.Timestamp("2021-10-21"),
    pd.Timestamp("2021-10-22")
]
t1 = pd.Series(np.random.randn(2), dates)
print(t1.index)
print(type(t1))
t1

periods = [pd.Period("2021-10-21"), pd.Period("2021-10-22")]
t2 = pd.Series(np.random.randn(2), periods)
print(t2.index)
print(type(t2))
t2

periods_m = [pd.Period("2021-10-21", 'M'), pd.Period("2021-10-22", 'M')]
t3 = pd.Series(np.random.randn(2), periods_m)
print(t3.index)
print(type(t3))
t3

# ## Generating ranges of timestamps
# - we can use the `date_range()` and `bdate_range()` functions to create a DatetimeIndex. 
# - The default frequency for `date_range` is a calendar day,
# - while the default for `bdate_range` is a business day.
# - `freq` parameter in function can refer to the [Date Offset][do]
#
# [do]: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects

# +
start = datetime.datetime(2021, 10, 21)
end = datetime.datetime(2021, 12, 21)
dtindex_1 = pd.date_range(start, end)
print(dtindex_1)

dtindex_2 = pd.bdate_range(start, end)
print(dtindex_2)

dtindex_3 = pd.bdate_range(start, periods=10, freq='BM') #business month end
print(dtindex_3)
# -

# # Question 0 - Topics in Pandas

# ##  Window Functions
# * Provide the calculation of statistics 
# * Primarily used in signal processing and time series data
# * Perform desired mathematical operations on consecutive values at a time

# ## Rolling Functions
# * Can apply on Series and Dataframe type
# * For DataFrame, each function is computed column-wise
# * Here is an example for calculation of rolling sum
# * Similar way to calculate the mean, var, std ...

series = pd.Series(range(5))
df = pd.DataFrame({"A": series, "B": series ** 3})
df.rolling(3).sum()

# ## Parameters
# * **win_type** changes the window function (equally weighted by default)
# * You can set the minimum number of observations in window required to have a
# value by using **min_periods=k**
# * Set the labels at the center of the window by using **center==True** 
# (set to the right edge by default)

print(df.rolling(3, win_type='gaussian').sum(std=3))
print(df.rolling(3, win_type='gaussian', center=True).sum(std=3))
print(df.rolling(3, win_type='gaussian', min_periods=2, 
                 center=True).sum(std=3))

# ## Expanding Functions
# * Calculate the expanding sum of given DataFrame or Series
# * Perform desired mathematical operations on current all previous values
# * Similar way to calculate the mean, var, std...
df.expanding(min_periods=2).sum()

# + [General Time Series Functions](#General-Time-Series-Functions)
# modules: -------------------------------------------------------------------
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from scipy.stats import ttest_ind_from_stats
from scipy.stats import norm
from Stats507_hw4_helper import ci_prop
from Stats507_hw4_helper import ci_mean
from numpy import arange
import itertools
from scipy.stats import binom
from collections import defaultdict
import math
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import datetime
# + [Convert to Timestamps](#Convert-to-Timestamps) [markdown]
# ## Time Series 
# **Ran Yan**
# -
# # Question 0 - Topics in Pandas
#
# ##  General Time Series Functions
# * pandas contains extensive capabilities and features for working with time series data for all domains.
# * can parse time series information in different formats and sources
# * can manipulating and converting date times with timezone information

# +
# example 1
dti = pd.to_datetime(
    ["5/20/2000", np.datetime64("2000-05-20"), datetime.datetime(2000, 5, 20)]
)
dti

# example 2
dti = pd.date_range("2000-01", periods=5, freq="D")
dti

# example 3
dti = dti.tz_localize("UTC")
dti
# -

# ## Convert to Timestamps
# * when convert to timestamps, convert series to series and convert list-like data to DatetimeIndex
# * return a single timestamp if pass a string
# * can use format argument to ensure specific parsing, here is an example below

pd.to_datetime("2021/10/23", format="%Y/%m/%d")

# ## Other Useful Time Series Functions
# - `between_time` 
#     - to select rows in data frame that are only between certain time range
#     - here is an example below to select time from 9:00 to 10:00
# - `date_range`
#     - convert timestamp to a 'unix' epoch
# - `bdate_range`
#     - create DatetimeIndex for in a range of business days

# +
rng = pd.date_range('2/3/2000', periods=24, freq='H')
ts = pd.Series(np.random.randn(len(rng)), index=rng)
ts.iloc[ts.index.indexer_between_time(datetime.time(9), datetime.time(10))]

stamps = pd.date_range("2021-10-23 20:15:05", periods=2, freq="H")
stamps

start = datetime.datetime(2021, 10, 20)
end = datetime.datetime(2021, 10, 23)
index = pd.bdate_range(start, end)
index
# -

# Eduardo Ochoa Rivera \
# eochoa@umich.edu \
# November 20, 2021

# ## Module imports

import numpy as np
import pandas as pd
import datetime

# ## Time series

# pandas contains extensive capabilities and features for working with time series data for all domains.
# For example: 
# * Parsing time series information from various sources and formats

dti = pd.to_datetime(["1/1/2018", 
                      np.datetime64("2018-01-01"), 
                      datetime.datetime(2018, 1, 1)])
dti

# * Generate sequences of fixed-frequency dates and time spans

dti = pd.date_range("2018-01-01", periods=3, freq="H")
dti

# * Performing date and time arithmetic with absolute or relative time increments. It can be specially usefull for financial data analysis.
#

friday = pd.Timestamp("2018-01-05")
print(friday.day_name())
saturday = friday + pd.Timedelta("1 day")
print(saturday.day_name())
monday = friday + pd.offsets.BDay()
print(monday.day_name())

# ## Timestamps vs time spans

# Timestamped data is the most basic type of time series data that associates values with points in time.

pd.Timestamp(datetime.datetime(2012, 5, 1))

# However, in many cases it is more natural to associate things like change variables with a time span instead.
#

pd.Period("2011-01"), pd.Period("2012-05", freq="D")

# **Timestamp** and **Period** can serve as an index.

# +
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
