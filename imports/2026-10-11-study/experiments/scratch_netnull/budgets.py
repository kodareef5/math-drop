"""Turn the paper's Lean-formalized spectral bounds into swap budgets for realistic sizes.

Lean-formalized (switch_chain_main / switch_chain_tv_bound, OAI/Probability/SwitchChain/Main.lean):
   gap(P_d) >= 1/(24 n^2 C(n,4))  for the lazy 4-vertex-set chain,  TV(t) <= 0.5 sqrt(|Omega|) exp(-gap t)
Equivalent (paper eq. mix:L-poincare, Lean generator_energy_le_switchLaplacian_unconditional + PairPoincare):
   Var(f) <= 2 n^2 <f, L f>   where L is the switch-graph Laplacian (each valid switch weight 1)

Rescalings (our corollaries, exact algebra; not in the paper):
 (A) edge-pair proposal with rejections held (igraph rewire, NetworKit EdgeSwitching, graph-tool persist=False):
     each valid switch has prob c per attempt. igraph: c = 1/(m(m-1)) [ordered pair, flip coin, one of 2
     orientations matches]; NetworKit/NetworkX-style degree-weighted node draws: c = 4/(4 m^2) = 1/m^2.
     Then I - P = c L, gap >= c/(2 n^2).
 (B) undirected Curveball, uniform random pair (NetworKit Curveball+UniformTradeGenerator):
     P = mean_a E_a = I - H/C(n,2); paper Cor. mix:poincare (Var <= <f,Hf>, Lean uniformVariance_le_generator)
     => gap >= 1/C(n,2).
 Mixing bound t(eps) <= gap^-1 (0.5 log|Omega| + log(1/(2 eps))) with log|Omega| <= log C(C(n,2), m) (all graphs with m edges).
 (C) sharpened comparison (ours, checked numerically on 8 instances, not proved here): Var <= <f, L f>,
     i.e. replace 2n^2 by 1 -- uses the exact Johnson-graph gap instead of the paper's path bound h_a <= n^2 J_a.
"""
import math, json


def logC(N, k):
    return math.lgamma(N + 1) - math.lgamma(k + 1) - math.lgamma(N - k + 1)


def row(n, m, eps=0.25):
    logOmega = logC(n * (n - 1) // 2, m)
    tvfac = 0.5 * logOmega + math.log(1 / (2 * eps))
    gap_paper = 1 / (24 * n * n * math.comb(n, 4))
    t_paper = tvfac / gap_paper
    c_ig = 1 / (m * (m - 1))
    t_edgepair = tvfac * 2 * n * n / c_ig
    t_edgepair_sharp = tvfac / c_ig
    t_cb = tvfac * math.comb(n, 2)
    return dict(n=n, m=m, log_Omega=round(logOmega), paper_lazy4set_steps=f"{t_paper:.2e}",
                paper_steps_per_edge=f"{t_paper / m:.1e}",
                edgepair_steps=f"{t_edgepair:.2e}", edgepair_steps_per_edge=f"{t_edgepair / m:.1e}",
                edgepair_sharpened_steps_per_edge=f"{t_edgepair_sharp / m:.1e}",
                curveball_pair_trades=f"{t_cb:.2e}",
                curveball_trades_per_node=f"{t_cb / n:.1e}",
                curveball_global_rounds=f"{t_cb / (n / 2):.1e}",
                default_100m=f"{100 * m:.1e}", default_10m=f"{10 * m:.1e}",
                ratio_edgepair_bound_to_100m=f"{t_edgepair / (100 * m):.1e}",
                ratio_sharpened_to_100m=f"{t_edgepair_sharp / (100 * m):.1e}")


if __name__ == "__main__":
    out = []
    for n, m in [(34, 78), (1000, 10**4), (10**4, 10**4 * 5), (10**5, 10**6), (10**6, 10**7)]:
        r = row(n, m)
        out.append(r)
        print(json.dumps(r))
    json.dump(out, open("budgets.json", "w"), indent=1)
