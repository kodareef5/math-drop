import re,sys,collections
rows=collections.defaultdict(list)
for fn in ['log_a.txt','log_b.txt']:
    for line in open(fn):
        m=re.match(r'(\d+) (\w+) (\d) seedgen=([\d.]+) ts=([\d.]+) .*seedF_max=([\d.]+) seedF_mean=([\d.]+) \| bestE (\d+) bestF ([\d.]+) restarts (\d+) steps (\d+)',line)
        if not m: continue
        N,fam,run,sg,ts,sfm,sfa,bE,bF,rs,st=m.groups()
        rows[(int(N),fam)].append(dict(sg=float(sg),ts=float(ts),seedmax=float(sfm),bestF=float(bF),restarts=int(rs),steps=int(st)))
fams=['random','legendre','pipeline','pipe_sign']
print('| N | TS budget (flip steps) | random | Legendre (rotated+appended) | pipeline (chirp + greedy-L4 rounding) | pipeline (chirp + sign rounding) |')
print('|---|---|---|---|---|---|')
for N in sorted({k[0] for k in rows}):
    cells=[]
    st=None
    for f in fams:
        r=rows.get((N,f),[])
        if not r: cells.append('n/a'); continue
        st=r[0]['steps']
        bf=[x['bestF'] for x in r]; sm=max(x['seedmax'] for x in r)
        cells.append(f"{min(bf):.2f}-{max(bf):.2f} (seed {sm:.2f})")
    print(f"| {N} | {st} | "+' | '.join(cells)+' |')
print()
for k in sorted(rows):
    r=rows[k]; print(k, 'runs',len(r),'mean TS s %.0f'%(sum(x['ts'] for x in r)/len(r)), 'mean seedgen s %.0f'%(sum(x['sg'] for x in r)/len(r)), 'restarts',[x['restarts'] for x in r])
