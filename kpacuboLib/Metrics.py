# KPACUBO time series metrics.
# KPACUBO is distributed under GPLv3 or later.
# Matvey Morozov, 2021.


import numpy as np


def PnL(price):
    return price-price[0]

def Sharpe(price, rf=0):
    ra = PnL(price)/price[0]
    return np.mean(ra-rf)/np.std(ra)
