import sys, subprocess, time, networkx as nx, numpy as np
sys.path.insert(0, '.')
from barnette_hcp import hcp_lkh
def read_planar_code(data):
    assert data.startswith(b'>>planar_code<<'); i = 15; out = []
    while i < len(data):
        n = data[i]; i += 1; G = nx.Graph(); v = 1
        while v <= n:
            w = data[i]; i += 1
            if w == 0: v += 1; continue
            G.add_edge(v - 1, w - 1)
        out.append(G)
    return out
tri_n = int(sys.argv[1]); count = int(sys.argv[2])
p = subprocess.Popen(['/home/claude/work/repos/plantri/plantri', '-bd', str(tri_n), '1/1000000'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
buf = p.stdout.read(15 + count * (2 * tri_n - 4) * 4 + 100); p.kill()
gs = []
data = buf; i = 15
while len(gs) < count and i < len(data):
    n = data[i]; j = i + 1; v = 1; G = nx.Graph()
    while v <= n and j < len(data):
        w = data[j]; j += 1
        if w == 0: v += 1
        else: G.add_edge(v - 1, w - 1)
    if v > n: gs.append(G); i = j
    else: break
for G in gs:
    assert all(d == 3 for _, d in G.degree()) and nx.is_bipartite(G)
    dt, bad, ok = hcp_lkh(nx.convert_node_labels_to_integers(G))
    print(f"plantri -bd {tri_n}: |V|={G.number_of_nodes()} 3conn={nx.node_connectivity(G)} LKH {dt:.2f}s non-edges={bad}")
