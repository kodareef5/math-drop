"""Certified (TV<=1/4) budgets for igraph rewire on small real graphs, using (a) the paper's Lean-formalized
comparison Var <= 2n^2 <f,Lf>, and (b) the sharpened Johnson-gap comparison Var <= <f,Lf> (our derivation).
Also measures igraph attempts/second to convert to wall time."""
import math, json, time, random, networkx as nx, igraph as ig
def logC(N, k): return math.lgamma(N + 1) - math.lgamma(k + 1) - math.lgamma(N - k + 1)
random.seed(0); ig.set_random_number_generator(random)
g = ig.Graph.Erdos_Renyi(n=2000, m=20000); t = time.time(); g.rewire(n=2_000_000); rate = 2_000_000 / (time.time() - t)
print("igraph rewire attempts/sec ~ %.2e" % rate)
out = []
for name, G in [("florentine", nx.florentine_families_graph()), ("karate", nx.karate_club_graph()),
                ("les_miserables", nx.les_miserables_graph()), ("n=200,m=1000", nx.gnm_random_graph(200, 1000, seed=1)),
                ("n=1000,m=1e4", nx.gnm_random_graph(1000, 10000, seed=1))]:
    n, m = G.number_of_nodes(), G.number_of_edges()
    tv = 0.5 * logC(n * (n - 1) // 2, m) + math.log(2)
    t_paper = 2 * n * n * m * (m - 1) * tv
    t_sharp = m * (m - 1) * tv
    r = dict(graph=name, n=n, m=m, formalized_attempts=f"{t_paper:.1e}", formalized_per_edge=f"{t_paper/m:.1e}",
             formalized_wall=f"{t_paper/rate:.1e} s", sharpened_attempts=f"{t_sharp:.1e}", sharpened_per_edge=f"{t_sharp/m:.1e}",
             sharpened_wall=f"{t_sharp/rate:.1e} s")
    print(json.dumps(r)); out.append(r)
json.dump(out, open("certified_small.json", "w"), indent=1)
