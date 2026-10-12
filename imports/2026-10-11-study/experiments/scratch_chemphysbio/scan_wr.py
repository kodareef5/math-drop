"""Scan curated BioModels SBML files for weak reversibility (structural) and
mass-action kinetics (heuristic symbolic check).

Usage: python3 -I scan_wr.py <final_dir> <out_json>

Structural model of the CRN:
  - species with boundaryCondition=true or constant=true are treated as
    parameters (dropped from complexes); this is the standard CRNT convention
  - reactions marked reversible in SBML contribute both directions
  - a model with assignment/rate rules acting on a reaction species, or with
    events, is flagged (not a pure autonomous mass-action CRN)
Weak reversibility: every reaction edge y->y' has y and y' in the same strongly
connected component of the complex graph.
Mass action (heuristic): kinetic law, after inlining function definitions and
substituting numeric parameter/compartment values, expands to
  k_f * prod(reactants^stoich)  [ - k_r * prod(products^stoich) if reversible ]
with k_f, k_r positive constants (free of species).
"""
import sys, json, os, glob, signal
import libsbml
import sympy as sp


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout()


signal.signal(signal.SIGALRM, _alarm)


def scc_ok(edges, nodes):
    # Tarjan SCC, iterative
    adj = {n: [] for n in nodes}
    for a, b in edges:
        adj[a].append(b)
    index = {}
    low = {}
    onstack = set()
    stack = []
    comp = {}
    idx = [0]
    c = [0]

    def strongconnect(v):
        work = [(v, iter(adj[v]))]
        index[v] = low[v] = idx[0]
        idx[0] += 1
        stack.append(v)
        onstack.add(v)
        while work:
            node, it = work[-1]
            advanced = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = idx[0]
                    idx[0] += 1
                    stack.append(w)
                    onstack.add(w)
                    work.append((w, iter(adj[w])))
                    advanced = True
                    break
                elif w in onstack:
                    low[node] = min(low[node], index[w])
            if not advanced:
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[node])
                if low[node] == index[node]:
                    while True:
                        w = stack.pop()
                        onstack.discard(w)
                        comp[w] = c[0]
                        if w == node:
                            break
                    c[0] += 1

    for n in nodes:
        if n not in index:
            strongconnect(n)
    return all(comp[a] == comp[b] for a, b in edges)


def deficiency(edges, nodes, species):
    # delta = #complexes - #linkage classes - rank S
    import numpy as np
    parent = {n: n for n in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in edges:
        parent[find(a)] = find(b)
    lc = len({find(n) for n in nodes})
    sp_idx = {s: i for i, s in enumerate(species)}
    vecs = []
    for a, b in set(edges):
        v = [0.0] * len(species)
        for s, m in b:
            v[sp_idx[s]] += m
        for s, m in a:
            v[sp_idx[s]] -= m
        vecs.append(v)
    rank = int(np.linalg.matrix_rank(np.array(vecs))) if vecs else 0
    return len(nodes) - lc - rank, lc, rank


def ast_to_sympy(node, fdefs, symmap):
    """Convert libsbml AST to sympy via infix formula; inline function defs."""
    formula = libsbml.formulaToL3String(node)
    return formula


def get_value_map(model):
    vals = {}
    for p in model.getListOfParameters():
        if p.isSetValue():
            vals[p.getId()] = p.getValue()
    for c in model.getListOfCompartments():
        if c.isSetSize():
            vals[c.getId()] = c.getSize()
        elif c.isSetVolume():
            vals[c.getId()] = c.getVolume()
    return vals


def analyze(path):
    doc = libsbml.readSBMLFromFile(path)
    model = doc.getModel()
    if model is None:
        return {"error": "nomodel"}
    res = {"id": os.path.basename(path).split("_")[0].replace(".xml", "")}
    species_all = {s.getId(): s for s in model.getListOfSpecies()}
    dyn = [sid for sid, s in species_all.items()
           if not (s.getBoundaryCondition() or s.getConstant())]
    dynset = set(dyn)
    rule_targets = set()
    for r in model.getListOfRules():
        if r.isAssignment() or r.isRate():
            rule_targets.add(r.getVariable())
    res["n_species"] = len(dyn)
    res["n_reactions"] = model.getNumReactions()
    res["n_events"] = model.getNumEvents()
    res["rules_on_species"] = len(rule_targets & set(species_all))
    edges = []
    nodes = set()
    ma_flags = []
    vals = get_value_map(model)
    # local parameters handled per reaction
    fdefs = {}
    for fd in model.getListOfFunctionDefinitions():
        fdefs[fd.getId()] = fd
    for rx in model.getListOfReactions():
        def cplx(lst):
            d = {}
            for sr in lst:
                s = sr.getSpecies()
                if s in dynset and s not in rule_targets:
                    st = sr.getStoichiometry() if sr.isSetStoichiometry() else 1.0
                    if st != st:  # NaN
                        st = 1.0
                    d[s] = d.get(s, 0) + st
            return tuple(sorted((k, v) for k, v in d.items() if v != 0))
        y = cplx(rx.getListOfReactants())
        yp = cplx(rx.getListOfProducts())
        if y == yp:
            continue  # pure catalytic/no net change after dropping boundary species
        nodes.add(y)
        nodes.add(yp)
        edges.append((y, yp))
        if rx.getReversible():
            edges.append((yp, y))
        # mass-action heuristic
        ma_flags.append(check_mass_action(model, rx, y, yp, vals, fdefs, dynset))
    nodes = sorted(nodes)
    res["n_complexes"] = len(nodes)
    res["n_edges"] = len(edges)
    if not edges:
        res["wr"] = None
        return res
    res["wr"] = scc_ok(edges, nodes)
    try:
        res["deficiency"], res["linkage_classes"], res["rank"] = deficiency(edges, nodes, sorted(dynset))
    except Exception as e:
        res["deficiency"] = None
    res["mass_action_all"] = all(f is True for f in ma_flags)
    res["mass_action_frac"] = sum(1 for f in ma_flags if f is True) / max(1, len(ma_flags))
    res["integer_stoich"] = all(float(m).is_integer() for e in edges for c in e for _, m in c)
    return res


import time
DEADLINE = [0.0]


def check_mass_action(model, rx, y, yp, vals, fdefs, dynset):
    if time.time() > DEADLINE[0]:
        return None
    kl = rx.getKineticLaw()
    if kl is None or kl.getMath() is None:
        return None
    try:
        signal.alarm(3)
        math = kl.getMath().deepCopy()
        # inline function definitions
        for _ in range(5):
            changed = False
            for fid, fd in fdefs.items():
                pass
            break
        conv = libsbml.SBMLFunctionDefinitionConverter()
        formula = libsbml.formulaToL3String(math)
        local = {}
        for lp in kl.getListOfLocalParameters():
            local[lp.getId()] = lp.getValue()
        for lp in kl.getListOfParameters():
            local[lp.getId()] = lp.getValue()
        # expand function definitions textually through sympy Lambda
        syms = {}
        allids = set(vals) | set(local) | set(s.getId() for s in model.getListOfSpecies())
        ns = {}
        for fid, fd in fdefs.items():
            body = fd.getBody()
            args = [fd.getArgument(i).getName() for i in range(fd.getNumArguments())]
            if body is None:
                continue
            bstr = libsbml.formulaToL3String(body)
            asyms = sp.symbols(args) if args else ()
            if not isinstance(asyms, (list, tuple)):
                asyms = (asyms,)
            loc = {a: s for a, s in zip(args, asyms)}
            loc.update(ns)
            try:
                bexpr = sp.sympify(bstr.replace("^", "**"), locals=loc)
            except Exception:
                return None
            ns[fid] = sp.Lambda(tuple(asyms), bexpr)
        for i in allids:
            if i not in ns:
                ns[i] = sp.Symbol(i)
        for bad in ["lambda", "S", "E", "I", "N", "O", "Q", "beta", "gamma", "pi", "zeta"]:
            if bad in allids:
                ns[bad] = sp.Symbol(bad)
        expr = sp.sympify(formula.replace("^", "**").replace("&&", "&").replace("||", "|"), locals=ns)
        sub = {}
        for k, v in vals.items():
            sub[sp.Symbol(k)] = v
        for k, v in local.items():
            sub[sp.Symbol(k)] = v
        # constant/boundary species -> treat as positive constants (value irrelevant, use 1.7)
        for s in model.getListOfSpecies():
            if s.getId() not in dynset:
                sub[sp.Symbol(s.getId())] = 1.7
        expr = expr.subs(sub)
        dsyms = [sp.Symbol(s) for s in dynset]
        free = expr.free_symbols
        if any(f not in set(dsyms) for f in free):
            return None  # unresolved parameter (e.g. assignment-rule param)
        e = sp.expand(expr)
        if e == 0:
            return None
        poly = sp.Poly(e, *dsyms) if dsyms else None
        if poly is None:
            return None
        terms = poly.terms()
        idx = {s: i for i, s in enumerate(dynset)}

        def mono(c):
            m = [0] * len(dsyms)
            for s, st in c:
                m[[str(d) for d in dsyms].index(s)] = int(round(st))
            return tuple(m)
        mf = mono(y)
        mr = mono(yp)
        got = {}
        for mon, coef in terms:
            got[tuple(mon)] = float(coef)
        if rx.getReversible():
            ok = set(got) <= {mf, mr} and got.get(mf, 0) > 0 and (got.get(mr, 0) < 0 or mr not in got)
            # require reverse term present for a true reversible
            ok = ok and got.get(mr, 0) < 0
        else:
            ok = set(got) == {mf} and got[mf] > 0
        return bool(ok)
    except Timeout:
        return None
    except Exception:
        return None
    finally:
        signal.alarm(0)


def one(f):
    # per-model wall budget for the (slow, symbolic) mass-action checks;
    # structural weak-reversibility/deficiency are always computed
    DEADLINE[0] = time.time() + float(os.environ.get("MA_BUDGET", "20"))
    try:
        r = analyze(f)
        r["ma_budget_exceeded"] = time.time() > DEADLINE[0]
    except Exception as e:
        r = {"id": os.path.basename(f), "error": repr(e)[:200]}
    return r


def main():
    from multiprocessing import Pool
    d = sys.argv[1]
    out = sys.argv[2]
    files = sorted(glob.glob(os.path.join(d, "*", "BIOMD*.xml")))
    with Pool(int(os.environ.get("NPROC", "2"))) as p:
        results = []
        for i, r in enumerate(p.imap(one, files, chunksize=1)):
            results.append(r)
            if i % 50 == 0:
                print(i, flush=True)
                json.dump(results, open(out + ".partial", "w"))
    json.dump(results, open(out, "w"), indent=0)


if __name__ == "__main__":
    main()
