# KPACUBO functional style Result class.
# KPACUBO is distributed under GPLv3 or later.
# Matvey Morozov, 2021.


def FailsWhen(values=[], predicates=[]):
    def FailsWhenDecorator(func):
        def FailsWhenReturn(*args, **kwargs):
            funcReturn = func(*args, **kwargs)
            if all(funcReturn != v for v in values) \
                and all(not p(funcReturn) for p in predicates):
                return Result.Ok(funcReturn)
            else:
                return Result.Fail(funcReturn) # this could be more informative.
        return FailsWhenReturn
    return FailsWhenDecorator


def FailsWhenThrows(func):
    def FailsWhenThrowsReturn(*args, **kwargs):
        try:
            return Result.Ok(func(*args, **kwargs))
        except Exception as e:
            return Result.Fail(str(e))
    return FailsWhenThrowsReturn


class Result:
    def __init__(self, outcome, value):
        (self.Outcome, self.Value) = (outcome, value)

    @staticmethod
    def Ok(value):
        return Result(True, value)

    def IsOk(self):
        return self.Outcome

    def OnOk(self, func):
        return func(self.Value) if self.IsOk() else self

    def OnOkAct(self, action):
        if self.IsOk():
            action(self.Value)
        return self

    @staticmethod
    def Fail(value):
        return Result(False, value)

    def IsFail(self):
        return not self.IsOk()

    def OnFail(self, func):
        return func(self.Value) if self.IsFail() else self

    def OnFailAct(self, action):
        if self.IsFail():
            action(self.Value)
        return self
