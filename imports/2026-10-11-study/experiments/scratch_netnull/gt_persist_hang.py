import sys, signal
import graph_tool.all as gt
sys.path.insert(0,'.')
from enum_graphs import enumerate_graphs, pair_index, switch_neighbours, edges_of
d=(3,3,2,2,2,2); n=len(d); pidx=pair_index(n)
gs=enumerate_graphs(d)
# find a realisation containing an edge that lies in no valid switch
def stuck_edges(g):
    E=edges_of(g,n); A=[set() for _ in range(n)]
    for i,j in E: A[i].add(j); A[j].add(i)
    out=[]
    for e in E:
        ok=False
        for f in E:
            if len(set(e)|set(f))<4: continue
            a,b=e; c,dd=f
            if (dd not in A[a] and b not in A[c]) or (c not in A[a] and b not in A[dd]): ok=True;break
        if not ok: out.append(e)
    return out
g0=[g for g in gs if stuck_edges(g)][0]
print('realisation', edges_of(g0,n), 'edges with no valid switch partner:', stuck_edges(g0))
g=gt.Graph(directed=False); g.add_vertex(n); g.add_edge_list(edges_of(g0,n))
signal.alarm(20)
try:
    gt.random_rewire(g, model='configuration', n_iter=1, persist=True)
    print('returned')
except Exception as ex:
    print('exception', ex)
