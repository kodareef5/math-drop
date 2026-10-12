"""Given COVER/FASTCOVER selected segments (logged in order), compare:
  concat length (what zstd does: memcpy end-to-end)
  greedy-SCS length of the segment set (max suffix-prefix overlap merging)
  dict-internal duplicate content."""
import sys
buf = open("samples_concat.bin", "rb").read()
def ov(a, b):
    m = min(len(a), len(b)) - 1
    for o in range(m, 0, -1):
        if a[-o:] == b[:o]:
            return o
    return 0
for mode in ["cover", "fastcover"]:
    segs = [tuple(map(int, l.split())) for l in open(f"seg_{mode}.log")]
    S = [buf[b:b + n] for b, n in segs]
    concat = sum(len(s) for s in S)
    # remove contained segments
    uniq = list(dict.fromkeys(S))
    nc = [s for s in uniq if not any(s != t and s in t for t in uniq)]
    contained = concat - sum(len(s) for s in nc)
    # greedy merge via overlap matrix (n ~ 560)
    import itertools
    n = len(nc)
    pairs = []
    for i in range(n):
        for j in range(n):
            if i != j:
                o = ov(nc[i], nc[j])
                if o:
                    pairs.append((o, i, j))
    pairs.sort(reverse=True)
    nxt = {}; prv = {}; comp = list(range(n))
    def find(x):
        while comp[x] != x:
            comp[x] = comp[comp[x]]; x = comp[x]
        return x
    saved = 0
    for o, i, j in pairs:
        if i in nxt or j in prv or find(i) == find(j):
            continue
        nxt[i] = j; prv[j] = i; comp[find(i)] = find(j); saved += o
    total_ov = sum(o for o, _, _ in pairs)
    print(f"{mode}: segments={len(S)} concat={concat} bytes; duplicate/contained segments drop {contained} bytes; "
          f"greedy SCS saves further {saved} bytes; SCS length={concat - contained - saved} "
          f"({100*(contained+saved)/concat:.2f}% shorter); median seg len={sorted(len(s) for s in S)[len(S)//2]}; pairs with overlap>0: {len(pairs)}")
