import json,os,sys,collections,re
OUT=sys.argv[1]; ROOT=sys.argv[2]
imports=collections.defaultdict(list)
for line in open(os.path.join(OUT,'imports.txt')):
    p,_,rest=line.partition(':'); m=re.match(r'import\s+(\S+)',rest.strip())
    if m: imports[p].append(m.group(1))
lines={}
for line in open(os.path.join(OUT,'linecounts.txt')):
    p,_,n=line.rstrip().rpartition(':'); lines[p]=int(n)
rows=json.load(open(os.path.join(OUT,'closure.json')))
def m2p(m): return m.replace('.','/')+'.lean'
seen=set()
for r in rows:
    st=[r['solution']]
    while st:
        m=st.pop()
        if m in seen: continue
        seen.add(m)
        for i in imports.get(m2p(m),[]):
            if i.split('.')[0] in ('OAI',): st.append(i)
reach=[m2p(m) for m in seen if os.path.exists(os.path.join(ROOT,m2p(m)))]
oai=[p for p in lines if p.startswith('OAI/')]
print('OAI files',len(oai),'lines',sum(lines[p] for p in oai))
print('reachable from comparator solutions: files',len(reach),'lines',sum(lines.get(p,0) for p in reach))
# OAI.lean root imports
root=[l.split()[1] for l in open(os.path.join(ROOT,'OAI.lean')) if l.startswith('import ')]
print('OAI.lean imports',len(root))
seen2=set(); st=list(root)
while st:
    m=st.pop()
    if m in seen2: continue
    seen2.add(m)
    for i in imports.get(m2p(m),[]):
        if i.split('.')[0]=='OAI': st.append(i)
r2=[m2p(m) for m in seen2 if os.path.exists(os.path.join(ROOT,m2p(m)))]
print('reachable from OAI.lean: files',len(r2),'lines',sum(lines.get(p,0) for p in r2))
unreach=set(oai)-set(r2)
print('unreachable from OAI.lean',len(unreach),sum(lines[p] for p in unreach))
c=collections.Counter('/'.join(p.split('/')[:3]) for p in unreach)
print(c.most_common(10))
# big line contributors in reachable-from-comparator
c2=collections.Counter()
for p in reach: c2['/'.join(p.split('/')[:3])]+=lines.get(p,0)
print(c2.most_common(25))
