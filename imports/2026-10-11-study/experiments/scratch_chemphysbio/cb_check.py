"""For the mass-action, weakly reversible BioModels found by scan_wr.py, extract
rate constants and test complex balance at the curated rates (van der Schaft,
Rao, Jayawardhana 2015 / Catalyst iscomplexbalanced method: rho from the
matrix-tree theorem per linkage class, then check D^T log(rho) in im(S^T)).
Usage: python3 -I cb_check.py <final_dir> <scan_json>
"""
import sys, json, glob, os
import numpy as np
import libsbml, sympy as sp
import networkx as nx


def extract(path):
    doc = libsbml.readSBMLFromFile(path)
    m = doc.getModel()
    comps = {c.getId(): (c.getSize() if c.isSetSize() else 1.0) for c in m.getListOfCompartments()}
    sp_all = {s.getId(): s for s in m.getListOfSpecies()}
    dyn = sorted(s for s, o in sp_all.items() if not (o.getBoundaryCondition() or o.getConstant()))
    vals = {p.getId(): p.getValue() for p in m.getListOfParameters() if p.isSetValue()}
    vals.update(comps)
    fdefs = {}
    for fd in m.getListOfFunctionDefinitions():
        args = [fd.getArgument(i).getName() for i in range(fd.getNumArguments())]
        body = libsbml.formulaToL3String(fd.getBody())
        asy = sp.symbols(args)
        if not isinstance(asy, (list, tuple)):
            asy = (asy,)
        loc = dict(zip(args, asy)); loc.update(fdefs)
        fdefs[fd.getId()] = sp.Lambda(tuple(asy), sp.sympify(body.replace('^', '**'), locals=loc))
    dsy = [sp.Symbol(s) for s in dyn]
    edges = {}  # (y,y') -> k (effective, divided by compartment volume of reactant? use raw)
    species_comp = {s: comps.get(sp_all[s].getCompartment(), 1.0) for s in dyn}
    for rx in m.getListOfReactions():
        def cplx(lst):
            d = {}
            for sr in lst:
                s = sr.getSpecies()
                if s in dyn:
                    d[s] = d.get(s, 0) + (sr.getStoichiometry() if sr.isSetStoichiometry() else 1.0)
            return tuple(sorted((k, int(v)) for k, v in d.items() if v))
        y, yp = cplx(rx.getListOfReactants()), cplx(rx.getListOfProducts())
        if y == yp:
            continue
        kl = rx.getKineticLaw()
        loc = {}
        for lp in kl.getListOfLocalParameters():
            loc[lp.getId()] = lp.getValue()
        for lp in kl.getListOfParameters():
            loc[lp.getId()] = lp.getValue()
        ns = dict(fdefs)
        ids = set(vals) | set(loc) | set(sp_all)
        for i in ids:
            if i not in ns:
                ns[i] = sp.Symbol(i)
        expr = sp.sympify(libsbml.formulaToL3String(kl.getMath()).replace('^', '**'), locals=ns)
        sub = {sp.Symbol(k): v for k, v in {**vals, **loc}.items()}
        for s, o in sp_all.items():
            if s not in dyn:
                sub[sp.Symbol(s)] = (o.getInitialConcentration() if o.isSetInitialConcentration() else o.getInitialAmount())
        e = sp.expand(expr.subs(sub))
        P = sp.Poly(e, *dsy)
        idx = {s: i for i, s in enumerate(dyn)}

        def mono(c):
            v = [0]*len(dyn)
            for s, st in c:
                v[idx[s]] = st
            return tuple(v)
        terms = {tuple(mn): float(cf) for mn, cf in P.terms()}
        kf = terms.get(mono(y), 0.0)
        edges[(y, yp)] = edges.get((y, yp), 0) + kf
        if rx.getReversible():
            kr = -terms.get(mono(yp), 0.0)
            edges[(yp, y)] = edges.get((yp, y), 0) + kr
    return dyn, edges, len(set(species_comp.values())), species_comp


def complex_balanced(dyn, edges):
    nodes = sorted({c for e in edges for c in e})
    ni = {c: i for i, c in enumerate(nodes)}
    G = nx.DiGraph()
    for (a, b), k in edges.items():
        G.add_edge(ni[a], ni[b], k=k)
    n = len(nodes)
    # Laplacian-based kernel per linkage class (matrix-tree: rho = kernel vector of A_k)
    A = np.zeros((n, n))
    for (a, b), k in edges.items():
        A[ni[b], ni[a]] += k
        A[ni[a], ni[a]] -= k
    rho = np.zeros(n)
    for comp in nx.weakly_connected_components(G):
        comp = sorted(comp)
        sub = A[np.ix_(comp, comp)]
        # kernel vector
        u, s, vt = np.linalg.svd(sub)
        v = vt[-1]
        v = v * np.sign(v.sum())
        rho[comp] = v / v.sum()
    if not np.all(rho > 1e-14):
        return False, rho.min()
    # Y: species x complexes
    Y = np.zeros((len(dyn), n))
    di = {s: i for i, s in enumerate(dyn)}
    for c, i in ni.items():
        for s, st in c:
            Y[di[s], i] = st
    D = np.zeros((n, len(edges)))
    for j, (a, b) in enumerate(edges):
        D[ni[a], j] = -1; D[ni[b], j] = 1
    S = Y @ D
    img = D.T @ np.log(rho)
    r1 = np.linalg.matrix_rank(S.T, tol=1e-9)
    r2 = np.linalg.matrix_rank(np.column_stack([S.T, img]), tol=1e-9)
    return r1 == r2, float(rho.min())


def main():
    final, scan = sys.argv[1], sys.argv[2]
    R = json.load(open(scan))
    out = []
    for r in R:
        if r.get('mass_action_all') and r.get('wr'):
            f = glob.glob(os.path.join(final, r['id'], r['id'] + '*.xml'))[0]
            try:
                dyn, edges, ncomp, _ = extract(f)
                pos = all(k > 0 for k in edges.values())
                cb, rmin = complex_balanced(dyn, edges)
                row = dict(id=r['id'], deficiency=r['deficiency'], lc=r['linkage_classes'], n_compartment_volumes=ncomp,
                           all_rates_positive=pos, complex_balanced_at_curated_rates=bool(cb),
                           events=r['n_events'], rules=r['rules_on_species'])
            except Exception as ex:
                row = dict(id=r['id'], error=repr(ex)[:200])
            print(row)
            out.append(row)
    json.dump(out, open('cb_check.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
