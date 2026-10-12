"""For Comparator configs with `definition_names`, Comparator checks only the
name/type/universe/safety of each listed definition, not its body. This script
locates each listed definition's source text in the challenge file and in the
solution's OAI import closure and compares them after alpha-normalising
identifiers that are local binders (crude: strips whitespace and compares the
sequence of non-binder tokens). It is a triage aid, not a proof of equality."""
import json, os, re, sys, glob, collections

ROOT = sys.argv[1]
OUT = sys.argv[2]
imports = collections.defaultdict(list)
for line in open(os.path.join(OUT, 'imports.txt')):
    p, _, rest = line.partition(':')
    m = re.match(r'import\s+(\S+)', rest.strip())
    if m: imports[p].append(m.group(1))

def m2p(m): return m.replace('.', '/') + '.lean'

def closure_files(mod):
    seen = set(); st = [mod]
    while st:
        m = st.pop()
        if m in seen: continue
        seen.add(m)
        for i in imports.get(m2p(m), []):
            if i.split('.')[0] == 'OAI': st.append(i)
    return [m2p(m) for m in seen if os.path.exists(os.path.join(ROOT, m2p(m)))]

def grab(src, short):
    m = re.search(r'^\s*(?:noncomputable\s+)?(?:def|abbrev)\s+' + re.escape(short) + r'\b.*?(?=^\s*(?:noncomputable\s+)?(?:def|abbrev|theorem|lemma|structure|end|namespace|/--|instance|@\[)|\Z)',
                  src, flags=re.S | re.M)
    return m.group(0) if m else None

KEYWORDS = set('def abbrev fun let in if then else by exact Measure Set Real ENNReal Prop Type'.split())
def shape(txt):
    toks = re.findall(r"[A-Za-z_][A-Za-z_0-9'.]*|\S", txt)
    # keep qualified/library identifiers and symbols; replace short lowercase locals by '_'
    out = []
    for t in toks:
        if re.fullmatch(r"[a-zα-ωπρμνγ][A-Za-z0-9_']{0,12}", t) and '.' not in t and t not in KEYWORDS:
            out.append('_')
        else:
            out.append(t)
    return out

os.chdir(ROOT)
for cfg in sorted(glob.glob('ComparatorChallenges/*.json')):
    j = json.load(open(cfg))
    dn = j.get('definition_names') or []
    if not dn: continue
    name = os.path.basename(cfg)[:-5]
    chal = open(f'ComparatorChallenges/{name}.lean').read()
    files = closure_files(j['solution_module'])
    srcs = {f: open(f).read() for f in files}
    res = []
    for d in dn:
        short = d.split('.')[-1]
        c = grab(chal, short)
        sol = None
        for f, s in srcs.items():
            g = grab(s, short)
            if g and (d.split('.')[-2] in s):
                sol = g; break
        if c is None or sol is None:
            res.append((short, 'not-found'))
        elif 'sorry' in c:
            res.append((short, 'genuine-hole'))
        else:
            res.append((short, 'same-shape' if shape(c) == shape(sol) else 'DIFFERS'))
    print(name, collections.Counter(r[1] for r in res), [r[0] for r in res if r[1] == 'DIFFERS'])
