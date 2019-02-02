from graph_profiler import GraphProfiler


def with_dot(n):
    temp = []
    for s in range(n):
        temp.append(s)

def without_dot(n):
    temp = []
    temp_append = temp.append
    for s in range(n):
        temp_append(s)


gp = GraphProfiler(range_=(1000,6000,1000))
gp.prepare_funcs([
    without_dot,
    with_dot
])

gp.run()

