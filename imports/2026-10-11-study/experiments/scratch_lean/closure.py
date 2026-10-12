"""Static import-closure analysis of the OAI Lean library.

For each Comparator config: solution module -> transitive closure of OAI.* imports,
total lines/files, external (non-Mathlib, non-OAI) packages touched.
Also maps configs -> family numbers via lean/docs/*.md.
"""
import json, os, re, glob, sys, collections

ROOT = sys.argv[1]  # /root/openai-math/lean
OUT = sys.argv[2]

imports = collections.defaultdict(list)
for line in open(os.path.join(OUT, 'imports.txt')):
    path, _, rest = line.partition(':')
    m = re.match(r'import\s+(\S+)', rest.strip())
    if m:
        imports[path].append(m.group(1))

lines = {}
for line in open(os.path.join(OUT, 'linecounts.txt')):
    p, _, n = line.rstrip().rpartition(':')
    lines[p] = int(n)

def mod2path(mod):
    return mod.replace('.', '/') + '.lean'

ext_prefix = collections.Counter()
for p, ims in imports.items():
    for i in ims:
        top = i.split('.')[0]
        if top not in ('OAI', 'Mathlib'):
            ext_prefix[top] += 1

closure_cache = {}
def closure(mod):
    seen = set(); stack = [mod]; ext = set()
    while stack:
        m = stack.pop()
        if m in seen: continue
        seen.add(m)
        p = mod2path(m)
        for i in imports.get(p, []):
            top = i.split('.')[0]
            if top == 'OAI' or top == 'ComparatorChallenges':
                stack.append(i)
            elif top != 'Mathlib':
                ext.add(top)
    return seen, ext

# config -> family
cfg2fam = collections.defaultdict(set)
for d in glob.glob(os.path.join(ROOT, 'docs/*.md')):
    num = os.path.basename(d)[:3]
    for c in re.findall(r'ComparatorChallenges/([A-Za-z0-9_]+)\.lean', open(d).read()):
        cfg2fam[c].add(num)

os.chdir(ROOT)
rows = []
for cfg in sorted(glob.glob('ComparatorChallenges/*.json')):
    j = json.load(open(cfg))
    name = os.path.basename(cfg)[:-5]
    sol = j['solution_module']
    mods, ext = closure(sol)
    files = [mod2path(m) for m in mods if os.path.exists(mod2path(m))]
    tot = sum(lines.get(f, 0) for f in files)
    rows.append(dict(cfg=name, fam=sorted(cfg2fam.get(name, [])), solution=sol,
                     files=len(files), lines=tot, ext=sorted(ext),
                     theorems=j['theorem_names'], defs=j.get('definition_names', [])))
json.dump(rows, open(os.path.join(OUT, 'closure.json'), 'w'), indent=1)
print('external import prefixes:', ext_prefix.most_common(40))
want = sys.argv[3].split(',') if len(sys.argv) > 3 else []
for r in rows:
    if not want or set(r['fam']) & set(want):
        print(f"{','.join(r['fam']):8s} {r['cfg']:38s} files={r['files']:6d} lines={r['lines']:9d} ext={r['ext']}")
