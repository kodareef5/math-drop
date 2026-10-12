import sys, subprocess, time, networkx as nx, numpy as np, elkai
sys.path.insert(0, '.')
from barnette_hcp import hcp_lkh
tri_n = int(sys.argv[1]); count = int(sys.argv[2]); res = sys.argv[3]
p = subprocess.Popen(['/home/claude/work/repos/plantri/plantri', '-bd', str(tri_n), res], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
nv = 2 * tri_n - 4
data = p.stdout.read(15 + count * (1 + 4 * nv) + 10); p.kill()
gs = []; i = 15
while len(gs) < count and i < len(data):
    n = data[i]; j = i + 1; v = 1; G = nx.Graph()
    while v <= n and j < len(data):
        w = data[j]; j += 1
        if w == 0: v += 1
        else: G.add_edge(v - 1, w - 1)
    if v > n: gs.append(G); i = j
    else: break
fails = {1: 0, 10: 0}; t = {1: 0.0, 10: 0.0}
for G in gs:
    G = nx.convert_node_labels_to_integers(G)
    perm = np.random.default_rng(len(G.edges())).permutation(G.number_of_nodes())
    G = nx.relabel_nodes(G, {i: int(perm[i]) for i in G.nodes()})
    for r in (1, 10):
        dt, bad, ok = hcp_lkh(G, runs=r); t[r] += dt; fails[r] += bad > 0
print(f"plantri -bd {tri_n} res {res}: |V|={nv} graphs={len(gs)}  LKH runs=1 fail {fails[1]}/{len(gs)} ({t[1]/len(gs):.2f}s avg)  runs=10 fail {fails[10]}/{len(gs)} ({t[10]/len(gs):.2f}s avg)")
