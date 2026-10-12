"""Tighter WR estimate: SBML Level-2 'reversible' defaults to true, so many
reactions are flagged reversible although their rate law is one-way.
Here a flagged reaction counts as two-way only if its rate-law formula
contains a subtraction or a call to a function definition whose body does.
Usage: python3 -I wr_kinetic.py <final_dir> <scan_json>"""
import sys, os, glob, json
import libsbml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scan_wr import scc_ok
final, scan = sys.argv[1], sys.argv[2]
R = json.load(open(scan))
n_wr_flag = n_wr_kin = 0; rows = []
for r in R:
    if r.get('wr') is None:
        continue
    f = glob.glob(os.path.join(final, r['id'], r['id'] + '*.xml'))[0]
    m = libsbml.readSBMLFromFile(f).getModel()
    fneg = {fd.getId() for fd in m.getListOfFunctionDefinitions() if fd.getBody() is not None and '-' in libsbml.formulaToL3String(fd.getBody())}
    sp_all = {s.getId(): s for s in m.getListOfSpecies()}
    dyn = {s for s, o in sp_all.items() if not (o.getBoundaryCondition() or o.getConstant())}
    rule_t = {x.getVariable() for x in m.getListOfRules() if x.isAssignment() or x.isRate()}
    dyn -= rule_t
    edges = []; nodes = set()
    for rx in m.getListOfReactions():
        def cplx(lst):
            d = {}
            for sr in lst:
                s = sr.getSpecies()
                if s in dyn:
                    st = sr.getStoichiometry() if sr.isSetStoichiometry() else 1.0
                    d[s] = d.get(s, 0) + (1.0 if st != st else st)
            return tuple(sorted((k, v) for k, v in d.items() if v))
        y, yp = cplx(rx.getListOfReactants()), cplx(rx.getListOfProducts())
        if y == yp:
            continue
        nodes |= {y, yp}; edges.append((y, yp))
        kl = rx.getKineticLaw()
        s = libsbml.formulaToL3String(kl.getMath()) if kl is not None and kl.getMath() is not None else ''
        twoway = rx.getReversible() and ('-' in s or any(fn + '(' in s for fn in fneg))
        if twoway:
            edges.append((yp, y))
    if not edges:
        continue
    wk = scc_ok(edges, sorted(nodes))
    n_wr_flag += bool(r['wr']); n_wr_kin += bool(wk)
    rows.append(dict(id=r['id'], wr_flag=r['wr'], wr_kinetic=bool(wk), lc=r.get('linkage_classes'), deficiency=r.get('deficiency'), ma=r.get('mass_action_all')))
json.dump(rows, open('wr_kinetic.json', 'w'), indent=1)
print('networks', len(rows), 'WR by SBML flag', n_wr_flag, 'WR by rate-law-aware direction', n_wr_kin)
k = [x for x in rows if x['wr_kinetic']]
print('rate-law-aware WR & >1 LC & def>0:', sum(1 for x in k if x['lc'] > 1 and (x['deficiency'] or 0) > 0))
print('rate-law-aware WR & single LC:', sum(1 for x in k if x['lc'] == 1))
