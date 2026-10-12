import json,os,re,sys,collections
exec(open('holes2.py').read().split("os.chdir(ROOT)")[0])
os.chdir(ROOT)
name=sys.argv[3]; wanted=sys.argv[4].split(',')
j=json.load(open(f'ComparatorChallenges/{name}.json'))
chal=open(f'ComparatorChallenges/{name}.lean').read()
files=closure_files(j['solution_module'])
for short in wanted:
    c=grab(chal,short)
    for f in files:
        s=open(f).read(); g=grab(s,short)
        if g:
            print('=== CHALLENGE',short); print(c.strip()[:900]); print('=== SOLUTION',f); print(g.strip()[:900]); break
