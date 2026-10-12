import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kmer_exp as E
k = 31; L = int(sys.argv[1])
rnd = random.Random(7)
g = E.read_genome(); region = g[:L]
uniq = sorted(set(region[i:i+k] for i in range(len(region)-k+1)))
for frac in (0.5, 0.2, 0.1): rnd.sample(uniq, int(frac*len(uniq)))
def rnd_dna(n): return "".join(rnd.choice("ACGT") for _ in range(n))
blocks = []
for _ in range(60):
    unit = rnd_dna(rnd.randint(1, 12)); fl = rnd_dna(rnd.randint(20, 80)); r = rnd.randint(4, 30)
    blocks.append([fl, unit, r])
build = lambda bl: "".join(f + u*r for f, u, r in bl)
kset = lambda s: set(s[i:i+k] for i in range(len(s)-k+1))
s = build(blocks); K = kset(s)
for b in blocks:
    while b[2] > 1:
        b[2] -= 1
        if not kset(build(blocks)) >= K:
            b[2] += 1; break
t = build(blocks)
fa = set(l.strip() for l in open("kmer_runs/synthetic_tandem_full.fa") if not l.startswith(">"))
print("L=%d generating len %d, shrunk superstring len %d, kmers %d, file kmers match: %s" % (L, len(s), len(t), len(K), fa == K))
