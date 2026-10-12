import sys, time, subprocess, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from snaky_qbf import load_cards, encode
AA, TT, HH = load_cards('/root/openai-math/preprints/Snaky-in-21-Maker-moves-September-25-2026/verification/certificate.txt')
CAQE = '/home/claude/work/repos/Q-sage/solvers/caqe/caqe'
BLOQ = '/home/claude/work/repos/Q-sage/tools/Bloqqer/bloqqer'
heights = [int(x) for x in sys.argv[1].split(',')]
tl = int(sys.argv[2])
for h in heights:
    cands = sorted([j for j in range(len(AA)) if HH[j] == h], key=lambda j: len(TT[j]) - len(AA[j]))
    j = cands[0]
    for hq in (h, h - 1):
        if hq < 1: continue
        f = f'qbf/snaky_card{j}_h{hq}.qdimacs'
        nf, nw, nv, nc = encode(AA[j], TT[j], hq, f)
        t = time.time()
        try:
            p = subprocess.run(f'{BLOQ} --keep=0 {f} > {f}.blq; {CAQE} {f}.blq', shell=True, capture_output=True, text=True, timeout=tl)
            out = p.stdout.strip().splitlines()
            res = [l for l in out if 'SATISFIABLE' in l.upper() or l.startswith('c Unsatisfiable') or l.startswith('c Satisfiable')]
            rc = p.returncode
            verdict = {10: 'TRUE', 20: 'FALSE'}.get(rc, f'rc={rc} ' + ' '.join(out[-2:]))
        except subprocess.TimeoutExpired:
            verdict = 'TIMEOUT'
        print(json.dumps({'card': j, 'cert_h': h, 'query_h': hq, '|A|': len(AA[j]), '|T|': len(TT[j]), 'free': nf, 'copies': nw,
                          'vars': nv, 'clauses': nc, 'result': verdict, 'sec': round(time.time() - t, 2)}), flush=True)
