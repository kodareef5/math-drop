import time, math, json, random, networkit as nk
def logC(N,k): return math.lgamma(N+1)-math.lgamma(k+1)-math.lgamma(N-k+1)
out=[]
for n,p in [(264,0.1),(1000,0.02)]:
    nk.engineering.setSeed(1, False)
    G=nk.generators.ErdosRenyiGenerator(n,p).generate()
    m=G.numberOfEdges()
    cert_burn=math.comb(n,2)*(0.5*logC(n*(n-1)//2,m)+math.log(2))
    thin=math.comb(n,2)*math.log(100)
    gen=nk.randomization.CurveballUniformTradeGenerator(10**6, n)
    trades=gen.generate()
    cb=nk.randomization.Curveball(G)
    t=time.time(); cb.run(trades); dt=time.time()-t
    r=dict(n=n,m=m,sec_per_1e6_trades=round(dt,2),certified_burnin_trades=f"{cert_burn:.2e}",
           burnin_seconds=round(cert_burn/1e6*dt,1),thin_trades_for_autocorr_0p01=f"{thin:.2e}",thin_seconds=round(thin/1e6*dt,3))
    print(json.dumps(r)); out.append(r)
json.dump(out,open("curveball_timing.json","w"),indent=1)
