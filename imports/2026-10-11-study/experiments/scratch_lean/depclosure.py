"""Static check: do the external-package modules transitively imported by a
Comparator solution contain `sorry`, `axiom`, `native_decide`?
Note: Comparator itself rejects any proof whose axiom closure uses sorryAx or
non-permitted axioms, so a hit here only matters if the hit declaration is
actually used. This script reports the file-level exposure."""
import os, re, sys, json, collections
DEPS = sys.argv[1]   # /home/claude/work/repos/deps
PKGDIR = {'PrimeNumberTheoremAnd': 'PrimeNumberTheoremAnd', 'StrongPNT': 'StrongPNT',
          'RellichKondrachov': 'rellich-kondrachov', 'AbsorptionCutoff': 'AbsorptionCutoff'}
roots = sys.argv[2:]

def path_of(mod):
    top = mod.split('.')[0]
    d = PKGDIR.get(top)
    if not d: return None
    p = os.path.join(DEPS, d, mod.replace('.', '/') + '.lean')
    return p if os.path.exists(p) else None

seen = set(); stack = list(roots); hits = []
while stack:
    m = stack.pop()
    if m in seen: continue
    seen.add(m)
    p = path_of(m)
    if not p: continue
    txt = open(p).read()
    # strip comments crudely
    code = re.sub(r'/-.*?-/', '', txt, flags=re.S)
    code = re.sub(r'--.*', '', code)
    for kw in ('sorry', 'native_decide', 'axiom'):
        n = len(re.findall(r'\b' + kw + r'\b', code))
        if n: hits.append((m, kw, n))
    for i in re.findall(r'^import\s+(\S+)', txt, flags=re.M):
        if i.split('.')[0] in PKGDIR: stack.append(i)
print('modules visited', len([m for m in seen if path_of(m)]))
for h in hits: print(h)
