"""For every structurally weakly reversible BioModels network (scan_wr.py),
emulate CatalystNetworkAnalysis.ispersistent's decision logic:
  conservative & no critical siphon -> :PERSISTENT (ADS07)
  otherwise                          -> :INCONCLUSIVE (or NOT_PERSISTENT if
                                        conservative & inconsistent; WR nets
                                        are always consistent)
and count how many WR networks the new theorem would move from INCONCLUSIVE
to PERSISTENT (if their kinetics are mass action with constant rates).
Usage: python3 -I wr_struct_persist.py <final_dir> <scan_json>
"""
import sys, os, glob, json
import numpy as np
import libsbml
from scipy.optimize import linprog
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from siphons import minimal_siphons, has_psemiflow


def struct_edges(path):
    m = libsbml.readSBMLFromFile(path).getModel()
    sp_all = {s.getId(): s for s in m.getListOfSpecies()}
    dyn = sorted(s for s, o in sp_all.items() if not (o.getBoundaryCondition() or o.getConstant()))
    rule_t = {r.getVariable() for r in m.getListOfRules() if r.isAssignment() or r.isRate()}
    dyn = [s for s in dyn if s not in rule_t]
    edges = {}
    for rx in m.getListOfReactions():
        def cplx(lst):
            d = {}
            for sr in lst:
                s = sr.getSpecies()
                if s in dyn:
                    st = sr.getStoichiometry() if sr.isSetStoichiometry() else 1.0
                    if st != st:
                        st = 1.0
                    d[s] = d.get(s, 0) + st
            return tuple(sorted((k, v) for k, v in d.items() if v))
        y, yp = cplx(rx.getListOfReactants()), cplx(rx.getListOfProducts())
        if y == yp:
            continue
        edges[(y, yp)] = 1.0
        if rx.getReversible():
            edges[(yp, y)] = 1.0
    used = sorted({s for e in edges for c in e for s, _ in c})
    return used, edges


def conservative(dyn, edges):
    n = len(dyn); di = {s: i for i, s in enumerate(dyn)}
    S = []
    for (a, b) in edges:
        v = np.zeros(n)
        for s, st in b: v[di[s]] += st
        for s, st in a: v[di[s]] -= st
        S.append(v)
    S = np.array(S)
    c = np.zeros(n + 1); c[-1] = -1
    A_eq = np.hstack([S, np.zeros((S.shape[0], 1))])
    A_ub = np.hstack([-np.eye(n), np.ones((n, 1))])
    r = linprog(c, A_ub=A_ub, b_ub=np.zeros(n), A_eq=A_eq, b_eq=np.zeros(S.shape[0]),
                bounds=[(0, 1)] * n + [(0, 1)], method='highs')
    return r.status == 0 and -r.fun > 1e-9


if __name__ == '__main__':
    final, scan = sys.argv[1], sys.argv[2]
    R = json.load(open(scan))
    rows = []
    for r in R:
        if not r.get('wr'):
            continue
        f = glob.glob(os.path.join(final, r['id'], r['id'] + '*.xml'))[0]
        try:
            dyn, edges = struct_edges(f)
            if not dyn:
                continue
            cons = conservative(dyn, edges)
            sips = minimal_siphons(dyn, edges, cap=300)
            crit = [s for s in sips if not has_psemiflow(dyn, edges, s)]
            verdict = 'PERSISTENT(ADS07)' if (cons and not crit) else 'INCONCLUSIVE'
            rows.append(dict(id=r['id'], n_species=len(dyn), conservative=bool(cons), n_siphons=len(sips),
                             n_critical=len(crit), ads07=verdict, mass_action_all=r.get('mass_action_all'),
                             ma_frac=r.get('mass_action_frac'), deficiency=r.get('deficiency'),
                             lc=r.get('linkage_classes'), events=r['n_events'], rules=r['rules_on_species']))
        except Exception as ex:
            rows.append(dict(id=r['id'], error=repr(ex)[:150]))
    json.dump(rows, open('wr_struct_persist.json', 'w'), indent=1)
    ok = [x for x in rows if 'error' not in x]
    inc = [x for x in ok if x['ads07'] == 'INCONCLUSIVE']
    print('WR networks analysed', len(ok), 'errors', len(rows) - len(ok))
    print('ADS07 PERSISTENT', len(ok) - len(inc), ' INCONCLUSIVE', len(inc))
    print('  inconclusive because non-conservative', sum(1 for x in inc if not x['conservative']))
    print('  inconclusive with critical siphon (conservative)', sum(1 for x in inc if x['conservative'] and x['n_critical']))
    print('  inconclusive & single linkage class (already covered by GMS14/Anderson11)', sum(1 for x in inc if x['lc'] == 1))
    print('  inconclusive & deficiency 0 (complex balanced for all rates; GAC literature)', sum(1 for x in inc if x['deficiency'] == 0))
    newc = [x for x in inc if x['lc'] > 1 and x['deficiency'] and x['deficiency'] > 0]
    print('  inconclusive & >1 LC & deficiency>0 (only the new theorem covers)', len(newc), [x['id'] for x in newc])
    print('    of these, kinetics verified mass action:', [x['id'] for x in newc if x['mass_action_all']])
    print('    of these, >=50% reactions mass action:', [x['id'] for x in newc if (x['ma_frac'] or 0) >= 0.5])
