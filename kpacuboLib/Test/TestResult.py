# KPACUBO functional style Result class tests.
# KPACUBO is distributed under GPLv3 or later.
# Matvey Morozov, 2021.


import unittest
from kpacuboLib.Result import Result, FailsWhen, FailsWhenThrows


class TestResult(unittest.TestCase):
    def test_FailsWhen(self):
        @FailsWhen([None])
        def TestResultProvider(x):
            return x

        self.assertTrue(TestResultProvider(0).IsOk())
        self.assertTrue(TestResultProvider(None).IsFail())

        TestResultProvider(0).OnFailAct(lambda _: self.assertTrue(False))
        TestResultProvider(None).OnOkAct(lambda _: self.assertTrue(False))

    def test_FailsWhenThrows(self):
        errorMessage = 'Error message'

        @FailsWhenThrows
        def TestResultProvider(x):
            if x:
                return x
            else:
                raise(ValueError(errorMessage))

        self.assertTrue(TestResultProvider(True).IsOk())
        self.assertTrue(TestResultProvider(False).IsFail())
        self.assertEqual(TestResultProvider(False).Value, errorMessage)


if __name__ == '__main__':
    unittest.main()
