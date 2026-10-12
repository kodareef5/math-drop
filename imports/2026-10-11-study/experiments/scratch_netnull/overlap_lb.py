"""Simple rigorous check of too-small defaults: fraction of ORIGINAL edges still present after the default
number of steps, vs the same fraction after a long run (igraph rewire 100m, uniform stationary law)."""
import json, random, numpy as np, networkx as nx, igraph as ig
def overlap(E0, E1):
    a = {frozenset(e) for e in E0}; b = {frozenset(e) for e in E1}
    return len(a & b) / len(a)
out = []
for name, G in [("BA n=2000 m=2", nx.barabasi_albert_graph(2000, 2, seed=1)),
                ("powerlaw_cluster n=2000", nx.powerlaw_cluster_graph(2000, 4, 0.3, seed=2)),
                ("karate", nx.karate_club_graph())]:
    G = nx.convert_node_labels_to_integers(G); m = G.number_of_edges()
    E0 = list(G.edges())
    R1 = nx.random_reference(G, niter=1, connectivity=False, seed=3)              # NetworkX default niter=1
    random.seed(4); ig.set_random_number_generator(random)
    g = ig.Graph(n=G.number_of_nodes(), edges=E0); g.rewire(n=100)                # R igraph keeping_degseq default niter=100
    ov_r100 = overlap(E0, g.get_edgelist())
    g = ig.Graph(n=G.number_of_nodes(), edges=E0); g.rewire(n=100 * m)            # long run reference
    ov_long = overlap(E0, g.get_edgelist())
    r = dict(network=name, m=m, overlap_random_reference_niter1=round(overlap(E0, R1.edges()), 3),
             overlap_R_igraph_default_100_trials=round(ov_r100, 3), overlap_after_100m=round(ov_long, 3))
    print(json.dumps(r)); out.append(r)
json.dump(out, open("overlap_lb.json", "w"), indent=1)
