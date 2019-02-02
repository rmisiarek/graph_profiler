from collections import defaultdict
from dataclasses import dataclass, field
from functools import partial, update_wrapper
import timeit

import numpy as np
import matplotlib.pyplot as plt


@dataclass
class GraphProfiler:
    range_: tuple = field(default=(10,110,10))
    repeat: int = field(default=3)
    number: int = field(default=10000)
    gc_enable: bool = field(default=False)
    functions: list = field(default_factory=list, init=False)

    def time_measure(self, function):
        if self.gc_enable:
            t = timeit.Timer(function, 'gc.enable()')
        else:
            t = timeit.Timer(function)
        
        try:
            measurement = t.repeat(repeat=self.repeat, number=self.number)
        except:
            t.print_exc()

        return np.mean(measurement)

    def graph(self, time_performance, time_diff=None):
        t = list(range(*self.range_))
        *_, step = self.range_ 
        
        plt.subplot(2, 1, 1)
        for key, value in time_performance.items():
            plt.plot(t, value, label=key)
        plt.xticks(np.arange(min(t), max(t) + 1, float(step)))
        plt.ylabel('Execution time [s]')
        plt.legend(loc='best')

        if time_diff:
            plt.subplot(2, 1, 2)
            y_pos = np.arange(len(time_diff))
            plt.bar(y_pos, time_diff, align='center')
            plt.ylabel('Time difference [s]')
            frame = plt.gca()     
            frame.axes.get_xaxis().set_visible(False)
  
        plt.show()
   
    @staticmethod
    def wrapped_partial(func, *args, **kwargs):
        partial_func = partial(func, *args, **kwargs)
        update_wrapper(partial_func, func)
        return partial_func
    
    def prepare_funcs(self, funcs, *args, **kwargs):
        self.functions = []
        for func in funcs:
            for i in range(*self.range_):
                if func.__code__.co_argcount == 0:
                    self.functions.append(func)
                else:
                    self.functions.append(self.wrapped_partial(func, i))

    def run(self):
        time_performance = defaultdict(list)
        memory_usage = defaultdict(list)
        for function in self.functions:
            time_performance[str(function.__name__)].append(self.time_measure(function))

        if len(time_performance) == 2:
            diff = []
            perf = list(time_performance.values())
            for t in zip(perf[0], perf[1]):
                diff.append(max(t[0], t[1]) - min(t[0], t[1]))
            self.graph(time_performance=time_performance, time_diff=diff)
        else:
            self.graph(time_performance=time_performance)
