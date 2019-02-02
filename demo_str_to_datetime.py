import datetime
from graph_profiler import GraphProfiler


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
    
gp = GraphProfiler(range_=(30,100,30))
gp.prepare_funcs([
    date_strptime,
    date_ymd_parser
])

gp.run()

