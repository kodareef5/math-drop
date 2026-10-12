"""CV of deg_sw(G) under the uniform law (sampled by igraph rewire) = max possible z-score shift (in null SDs)
of ANY statistic caused by NetworkX's retry-until-success bias (Cauchy-Schwarz: |Cov(x,w)|/(E w sd x) <= CV(w))."""
import json, random, numpy as np, networkx as nx, igraph as ig
from practical_bias import degsw_terms
def cv(name, G, S=400):
    G=nx.convert_node_labels_to_integers(nx.Graph(G)); G.remove_edges_from(nx.selfloop_edges(G))
    n,m=G.number_of_nodes(),G.number_of_edges(); g=ig.Graph(n=n,edges=list(G.edges())); d=np.array(g.degree(),float)
    random.seed(5); ig.set_random_number_generator(random); g.rewire(n=50*m)
    W=[]
    for _ in range(S):
        g.rewire(n=5*m); A=np.array(g.get_adjacency().data,float); W.append(degsw_terms(A,d)[0])
    W=np.array(W); r=dict(network=name,n=n,m=m,dmax=int(d.max()),CV_deg_sw=round(float(W.std()/W.mean()),4),valid_fraction=round(float(W.mean()/(2*degsw_terms(A,d)[1])),3))
    print(json.dumps(r),flush=True); return r
out=[cv("ER n=60 p=0.5 (dense)",nx.gnp_random_graph(60,0.5,seed=1)),
     cv("ER n=40 p=0.8 (very dense)",nx.gnp_random_graph(40,0.8,seed=2)),
     cv("star+ring hubs (wheel W_60)",nx.wheel_graph(60)),
     cv("Chung-Lu power-law gamma=2.1 n=1000",nx.expected_degree_graph([min(300,5*(i+1)**(-1/1.1)*30) for i in range(1000)],seed=3,selfloops=False)),
     cv("powerlaw_cluster n=500",nx.powerlaw_cluster_graph(500,3,0.3,seed=4)),
     cv("complete bipartite-ish K_{10,40} plus matching",nx.compose(nx.complete_bipartite_graph(10,40),nx.Graph([(10+2*i,11+2*i) for i in range(20)])))]
json.dump(out,open("cv_hard.json","w"),indent=1)
