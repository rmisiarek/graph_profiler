from collections import defaultdict
import timeit

from memory_profiler import memory_usage, profile


class GraphProfiler:
    def __init__(self, x_range=(30, 70, 30), number=10000, gc_enable=False):
        self.x_range = x_range
        self.number = number
        self.gc_enable = gc_enable
        self.functions = []

    def time_measure(self, function):
        if self.gc_enable:
            t = timeit.Timer(function)
        else:
            t = timeit.Timer(function, 'gc.enable()')
        
        try:
            measurement = t.timeit(self.number)
        except:
            t.print_exc()

        return measurement

    def memory_usage(self, func):
        memory = memory_usage(func)
        return max(memory)

    def graph(self, time_measure, memory_usage=None):
        pass
    
    def wrapped_partial(self, func, *args, **kwargs):
        print('func: ', func)
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
        memory_usage = defaultdict(set)
        for function in self.functions:
            time_performance[str(function.__name__)].append(self.time_measure(function))
            memory_usage[str(function.__name__)].add(self.memory_usage(function))

        from pprint import pprint
        pprint(time_performance)
        pprint(memory_usage)

        return time_performance


if __name__ == "__main__":
    
    from functools import partial, update_wrapper

   
    def list_comp(n):
        ''.join([str(i) for i in range(n)])

    def join1(n):
        ''.join(str(i) for i in range(n))

    def join2(n):
        ''.join(map(str, range(n)))

    def foo():
        return True

    import datetime

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
    
    gp = GraphProfiler()
    gp.prepare_funcs([foo, date_strptime, date_ymd_parser])
    gp.run()


