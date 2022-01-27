# KPACUBO cache management tests.
# KPACUBO is distributed under GPLv3 or later.
# Matvey Morozov, 2021.


import unittest
import pandas as pd
from os import mkdir, rmdir
from os.path import isdir, isfile
from pandas.api.types import is_datetime64_any_dtype
from kpacuboLib.Persistence import \
    CacheManager, CachesDataFrame, CachesTimeSeries
from kpacuboLib.Result import Result


testDir = 'TestCache'
testCache = CacheManager(testDir)


def DataFrameProducer():
    return Result.Ok(pd.DataFrame({
        'Date' : ['2000-01-01', '2000-01-02', '2000-02-01', '2001-01-01'],
        'Close' : [1,1,1,1]}))


class TestCaches(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not isdir(testDir):
            mkdir(testDir)

    @classmethod
    def tearDownClass(cls):
        testCache.ClearAll()
        rmdir(testDir)

    def test_StoreClearAll(self):
        @CachesDataFrame(testCache)
        def CachedFunc():
            return DataFrameProducer()

        df = CachedFunc().Value
        testCache.ClearAll()
        self.assertTrue(not isfile(testCache.FileName()))

    def test_StoreFetchClear(self):
        @CachesDataFrame(testCache)
        def CachedFunc():
            return DataFrameProducer()

        df1 = CachedFunc().Value
        df2 = testCache.Fetch(testCache.FileName(), 0).Value

        [self.assertEqual(x,y) for x,y in zip(df1.index, df2.index)]
        [self.assertEqual(x,y) for x,y in zip(df1['Close'], df2['Close'])]

        testCache.Clear()
        self.assertTrue(not isfile(testCache.FileName()))

    def test_TimeSeriesIndex(self):
        @CachesTimeSeries(testCache)
        def CachedFunc():
            return DataFrameProducer()

        dfs = (CachedFunc().Value, CachedFunc().Value)

        self.assertTrue(isfile(testCache.FileName()))
        [self.assertTrue(is_datetime64_any_dtype(df.index)) for df in dfs]


if __name__ == '__main__':
    unittest.main()
