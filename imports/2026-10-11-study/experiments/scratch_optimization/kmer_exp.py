"""Greedy (KmerCamel BIGREEDY, -u) vs cycle-cover LB (KmerCamel lowerbound -u) vs paper's W (family 128)
on k=31 k-mer sets from S. pneumoniae ATCC 700669 (NC_011900.1, bundled in kmercamel/data) and synthetic repeats."""
import subprocess, sys, time, random, json, os
sys.path.insert(0, os.path.dirname(__file__))
from scs_W import compute_W

KC = "/home/claude/work/repos/kmercamel/kmercamel"
GEN = "/home/claude/work/repos/kmercamel/data/spneumoniae.fa"
OUT = "/home/claude/work/repos/scratch_optimization/kmer_runs"
os.makedirs(OUT, exist_ok=True)


def read_genome():
    return "".join(l.strip() for l in open(GEN) if not l.startswith(">")).upper()


def write_kmers(kmers, path):
    with open(path, "w") as f:
        for i, s in enumerate(kmers):
            f.write(">%d\n%s\n" % (i, s))


def kc_greedy(path, k):
    t = time.perf_counter()
    out = subprocess.run([KC, "compute", "-k", str(k), "-u", path], capture_output=True, text=True, check=True).stdout
    seq = "".join(l.strip() for l in out.splitlines() if not l.startswith(">"))
    return seq, time.perf_counter() - t


def kc_lb(path, k):
    t = time.perf_counter()
    out = subprocess.run([KC, "lowerbound", "-k", str(k), "-u", path], capture_output=True, text=True, check=True).stdout
    return int(out.strip().split()[-1]), time.perf_counter() - t


def run(name, kmers, k):
    kmers = sorted(set(kmers))
    path = os.path.join(OUT, name + ".fa")
    write_kmers(kmers, path)
    ms, tg = kc_greedy(path, k)
    sup = ms.upper()
    # verify superstring
    present = set(sup[i:i + k] for i in range(len(sup) - k + 1))
    missing = sum(1 for s in kmers if s not in present)
    lb, tl = kc_lb(path, k)
    st = {}
    t = time.perf_counter(); W = compute_W(kmers, stats=st); tw = time.perf_counter() - t
    We = compute_W(kmers, use_period=False)
    row = dict(name=name, n_kmers=len(kmers), k=k, greedy=len(sup), missing=missing,
               cycle_cover_LB=lb, W=W, W_extension_only=We, best_LB=max(lb, W),
               greedy_over_cc=len(sup) / lb, greedy_over_W=len(sup) / W,
               certified_gap_pct=100 * (len(sup) - max(lb, W)) / max(lb, W),
               t_greedy=tg, t_lb=tl, t_W=tw, **st)
    print(json.dumps(row)); sys.stdout.flush()
    return row


if __name__ == "__main__":
    k = 31
    g = read_genome()
    rnd = random.Random(7)
    rows = []
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 50000
    region = g[:L]
    allk = [region[i:i + k] for i in range(len(region) - k + 1)]
    rows.append(run("spn_%dbp_full" % L, allk, k))
    uniq = sorted(set(allk))
    for frac in (0.5, 0.2, 0.1):
        rows.append(run("spn_%dbp_sub%02d" % (L, int(frac * 100)), rnd.sample(uniq, int(frac * len(uniq))), k))
    # synthetic: tandem repeats + random DNA, exercises the period rule
    def rnd_dna(n): return "".join(rnd.choice("ACGT") for _ in range(n))
    synth = ""
    for _ in range(60):
        unit = rnd_dna(rnd.randint(1, 12))
        synth += rnd_dna(rnd.randint(20, 80)) + unit * rnd.randint(4, 30)
    sk = [synth[i:i + k] for i in range(len(synth) - k + 1)]
    rows.append(run("synthetic_tandem_full", sk, k))
    rows.append(run("synthetic_tandem_sub30", rnd.sample(sorted(set(sk)), int(0.3 * len(set(sk)))), k))
    json.dump(rows, open(os.path.join(OUT, "results_%d.json" % L), "w"), indent=1)
