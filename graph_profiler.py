import timeit
from collections import defaultdict
from functools import partial, update_wrapper

import numpy as np
import matplotlib.pyplot as plt
from memory_profiler import memory_usage, profile


class GraphProfiler:
    def __init__(self, x_range=(10, 110, 10), repeat=3, number=10000, gc_enable=False):
        self.x_range = x_range
        self.repeat = repeat
        self.number = number
        self.gc_enable = gc_enable
        self.functions = []

    def time_measure(self, function):
        if self.gc_enable:
            t = timeit.Timer(function)
        else:
            t = timeit.Timer(function, 'gc.enable()')
        
        try:
            measurement = t.repeat(repeat=self.repeat, number=self.number)
        except:
            t.print_exc()

        return np.mean(measurement)

    @staticmethod
    def memory_usage(func):
        memory = memory_usage(func)
        return max(memory)

    def graph(self, time_performance, memory_usage):
        t = list(range(*self.x_range))
        *_, step = self.x_range 
        
        plt.subplot(2, 1, 1)
        for key, value in time_performance.items():
            plt.plot(t, value, label=key)
        plt.xticks(np.arange(min(t), max(t) + 1, float(step)))
        plt.ylabel('Time [s]')
        plt.legend(loc='lower right')

        plt.subplot(2, 1, 2)
        for key, value in memory_usage.items():
            plt.plot(t, value, label=key) 
        plt.xticks(np.arange(min(t), max(t) + 1, float(step)))
        plt.ylabel('Memory usage [MiB]')
        plt.legend(loc='lower right')
 
        plt.show()
   
    @staticmethod
    def wrapped_partial(func, *args, **kwargs):
        partial_func = partial(func, *args, **kwargs)
        update_wrapper(partial_func, func)
        return partial_func
    
    def prepare_funcs(self, funcs, *args, **kwargs):
        for func in funcs:
            for i in range(*self.x_range):
                if func.__code__.co_argcount == 0:
                    self.functions.append(func)
                else:
                    self.functions.append(self.wrapped_partial(func, i, *args, **kwargs))

    def run(self):
        time_performance = defaultdict(list)
        memory_usage = defaultdict(list)
        for function in self.functions:
            time_performance[str(function.__name__)].append(self.time_measure(function))
            memory_usage[str(function.__name__)].append(self.memory_usage(function))
        self.graph(time_performance=time_performance, memory_usage=memory_usage)

if __name__ == "__main__":
    import datetime

    def list_comp(n):
        ''.join([str(i) for i in range(n)])

    def join1(n):
        ''.join(str(i) for i in range(n))

    def join2(n):
        ''.join(map(str, range(n)))

    def foo():
        return True

    def date_strptime(n):
        dt = '2018-12-12'
        while n > 0:
            datetime.datetime.strptime(dt, '%Y-%m-%d')
            n -= 1

    def date_ymd_parser(n):
        dt = '2018-12-12'
        while n > 0:
            y, m, d = dt.split('-')
            datetime.datetime(int(y), int(m), int(d))
            n -= 1
    
    gp = GraphProfiler(x_range=(20,230,20))
    gp.prepare_funcs([list_comp, join1, join2])
#    gp.prepare_funcs([date_strptime, date_ymd_parser])
    gp.run()


