from graph_profiler import GraphProfiler


def join_list_comprehension(n):
    ''.join([str(i) for i in range(n)])

def join_generator(n):
    ''.join(str(i) for i in range(n))

def join_map(n):
    ''.join(map(str, range(n)))
  
gp = GraphProfiler(x_range=(10,130,10), repeat=1, number=1000000)
gp.prepare_funcs([
    join_list_comprehension, 
    join_generator, 
    join_map
])

gp.run()

