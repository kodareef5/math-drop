"""Control: 3-connected cubic planar graphs (duals of triangulations, plantri -d) of the same order,
mostly non-bipartite, vs Barnette graphs (plantri -bd). Only Hamiltonian ones are counted
(verified by any LKH run finding a tour)."""
import sys, subprocess, networkx as nx, numpy as np
sys.path.insert(0, '.')
from barnette_hcp import hcp_lkh
def gen(args, count, nv):
    p = subprocess.Popen(['/home/claude/work/repos/plantri/plantri'] + args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
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
    return gs
def run(label, gs):
    f1 = f10 = nh = 0; nb = 0
    for G in gs:
        G = nx.convert_node_labels_to_integers(G)
        perm = np.random.default_rng(len(G)).permutation(len(G)); G = nx.relabel_nodes(G, {i: int(perm[i]) for i in G})
        nb += nx.is_bipartite(G)
        d1, b1, _ = hcp_lkh(G, 1); d10, b10, _ = hcp_lkh(G, 10)
        f1 += b1 > 0; f10 += b10 > 0
    print(f"{label}: graphs={len(gs)} bipartite={nb} LKH fail runs=1: {f1}/{len(gs)}  runs=10: {f10}/{len(gs)}", flush=True)
tri = int(sys.argv[1]); nv = 2 * tri - 4; N = int(sys.argv[2])
run(f"plantri -d {tri} (cubic planar 3-conn, |V|={nv})", gen(['-d', str(tri), '5/100000'], N, nv))
run(f"plantri -bd {tri} (Barnette, |V|={nv})", gen(['-bd', str(tri), '5/1000'], N, nv))
