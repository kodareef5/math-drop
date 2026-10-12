"""Better upper bound for synthetic tandem k-mer set: shrink tandem copies in the generating sequence while
preserving the k-mer set; also try KmerCamel local-greedy / streaming."""
import random, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import kmer_exp as E
k = 31
rnd = random.Random(7)
g = E.read_genome(); L = 20000
region = g[:L]; allk = [region[i:i+k] for i in range(len(region)-k+1)]
uniq = sorted(set(allk))
for frac in (0.5, 0.2, 0.1): rnd.sample(uniq, int(frac*len(uniq)))
def rnd_dna(n): return "".join(rnd.choice("ACGT") for _ in range(n))
blocks = []
for _ in range(60):
    unit = rnd_dna(rnd.randint(1, 12)); fl = rnd_dna(rnd.randint(20, 80)); r = rnd.randint(4, 30)
    blocks.append([fl, unit, r])
def build(bl): return "".join(f + u*r for f, u, r in bl)
s = build(blocks)
K = set(s[i:i+k] for i in range(len(s)-k+1))
# shrink each repeat count greedily while k-mer set preserved
changed = True
while changed:
    changed = False
    for b in blocks:
        while b[2] > 1:
            b[2] -= 1
            t = build(blocks)
            if set(t[i:i+k] for i in range(len(t)-k+1)) >= K:
                changed = True
            else:
                b[2] += 1; break
t = build(blocks)
print("original len", len(s), "shrunk-repeat superstring len", len(t), "distinct kmers", len(K))
path = "kmer_runs/synthetic_tandem_full.fa"
for alg in ["greedy", "local-greedy", "streaming"]:
    args = [E.KC, "compute", "-k", "31", "-u", "-a", alg] + (["-d", "31"] if alg == "local-greedy" else []) + [path]
    out = subprocess.run(args, capture_output=True, text=True).stdout
    print(alg, len("".join(l.strip() for l in out.splitlines() if not l.startswith(">"))))
