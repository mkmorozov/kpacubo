# KPACUBO cache management.
# KPACUBO is distributed under GPLv3 or later.
# Matvey Morozov, 2022.


import os
import pandas as pd
from os import listdir
from os.path import isdir, isfile, join
from datetime import datetime
from kpacuboLib.Result import Result, FailsWhen


def IndexToTime(df):
    df.index = pd.to_datetime(df.index)
    return Result.Ok(df)


class CachesDataFrame:
    def __init__(self, cache, indexCol=0):
        (self.Cache, self.IndexCol) = (cache, indexCol)

    def __call__(self, func):
        def CachesDataFrameReturn(*args, **kwargs):
            fileName = self.Cache.FileName(*args, **kwargs)
            return self.Cache.Fetch(fileName, self.IndexCol).OnFail(lambda _:
                func(*args, **kwargs)
                .OnOkAct(lambda x: self.Cache.Store(fileName, x)))
        return CachesDataFrameReturn


class CachesTimeSeries(CachesDataFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, func):
        baseCall = super().__call__(func)
        def CachesDataFrameReturn(*args, **kwargs):
            return baseCall(*args, **kwargs).OnOk(IndexToTime)
        return CachesDataFrameReturn


class CacheManager:
    def __init__(self, cacheDir, prefix='', fmt='zip'):
        (self.CacheDir, self.Prefix, self.Format) = (cacheDir, prefix, fmt)
        if not isdir(self.CacheDir):
            os.mkdir(self.CacheDir)

    def Clear(self, *args, **kwargs):
        fileName = self.FileName(*args, **kwargs)
        if isfile(fileName):
            os.remove(fileName)

    def ClearAll(self):
        for i in listdir(self.CacheDir):
            if isfile(join(self.CacheDir, i)):
                os.remove(join(self.CacheDir, i))

    @FailsWhen(predicates=[lambda x: x.empty])
    def Fetch(self, fileName, indexCol):
        return pd.read_csv(fileName, index_col=indexCol) if isfile(fileName) \
            else pd.DataFrame()

    @staticmethod
    def SafeString(string):
        keep = [' ', '.', '_']
        return "".join(c for c in string if c.isalnum() or c in keep).rstrip()

    def FileName(self, *args, **kwargs):
        return join(self.CacheDir, self.Prefix
            + '_'.join(str(i) for i in args)
            + ('_' if kwargs else '')
            + '_'.join(str(i)+SafeString(str(j)) for i,j in
                zip(kwargs.keys(), kwargs.values()))
            + f".{self.Format}")

    def Store(self, fileName, df):
        return Result.Ok(df.to_csv(fileName))
