# KPACUBO matplotlib line plots wrapper.
# KPACUBO is distributed under GPLv3 or later.
# Matvey Morozov, 2021.


import matplotlib.pyplot as plt
import pandas as pd


class KwargsDefault(dict):
    def __init__(self, *args, **kwargs):
        dictArgs = dict(kwargs)
        if 'default' in dictArgs:
            dictDefault = kwargs['default']
            dictArgs.pop('default')

        dict.__init__(self, *args, **dictArgs)
        for arg in dictDefault.keys():
            if arg not in self.keys():
                self[arg] = dictDefault[arg]


class XY:
    def __init__(self, **kwargs):
        pd.plotting.register_matplotlib_converters()
        self.Fig = None
        self.FigArgs = KwargsDefault(**kwargs, default=self.FigDefault())

    @staticmethod
    def FigDefault():
        return {'figsize':(8, 3), 'dpi':100}

    @staticmethod
    def PltDefault():
        return {'xlabel':None, 'ylabel':None,
            'xlim':(None,None), 'ylim':(None,None)}

    @staticmethod
    def CheckArgs(args):
        if len(args)<2 or not hasattr(args[1], "__len__") \
            or len(args[0])!=len(args[1]):
            return (range(len(args[0])),) + args
        return args

    @staticmethod
    def SplitKwargs(**kwargs):
        (pltArgs, pltOptions) = ({}, {})
        for arg in kwargs:
            if arg in XY.PltDefault().keys():
                pltOptions[arg] = kwargs[arg]
            else:
                pltArgs[arg] = kwargs[arg]
        return (pltArgs, pltOptions)

    def Disp(self, plotF, *args, **kwargs):
        (pltArgs, pltOptions) = XY.SplitKwargs(**kwargs)
        pltOptions = KwargsDefault(pltOptions, default=XY.PltDefault())
        self.Fig = plt.figure(**self.FigArgs)

        plotF(*XY.CheckArgs(args), **pltArgs)
        plt.xlabel(pltOptions['xlabel'])
        plt.ylabel(pltOptions['ylabel'])
        plt.xlim(pltOptions['xlim'])
        plt.ylim(pltOptions['ylim'])
        return self

    def Plot(self, *args, **kwargs):
        return self.Disp(plt.plot, *args, **kwargs)

    def SemilogX(self, *args, **kwargs):
        return self.Disp(plt.semilogx, *args, **kwargs)

    def SemilogY(self, *args, **kwargs):
        return self.Disp(plt.semilogy, *args, **kwargs)

    def LogLog(self, *args, **kwargs):
        return self.Disp(plt.loglog, *args, **kwargs)
