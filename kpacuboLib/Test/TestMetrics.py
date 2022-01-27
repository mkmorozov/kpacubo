# KPACUBO time series metrics tests.
# KPACUBO is distributed under GPLv3 or later.
# Matvey Morozov, 2021.


import unittest
import pandas as pd
from kpacuboLib.Metrics import PnL, Sharpe


def TestDataPovider():
    return pd.DataFrame({
        'Date' : ['2000-01-01', '2000-01-02', '2000-02-01', '2001-01-01'],
        'Close' : [2,3,3,4]}).set_index('Date')


class TestMetrics(unittest.TestCase):
    def test_PnL(self):
        df = TestDataPovider()
        [self.assertEqual(x,y) for x,y in
            zip(PnL(df['Close']), df['Close']-df['Close'][0])]

    def test_Sharpe(self):
        self.assertTrue(
            abs(Sharpe(TestDataPovider()['Close']) - 2**0.5) < 1E-15)


if __name__ == '__main__':
    unittest.main()
