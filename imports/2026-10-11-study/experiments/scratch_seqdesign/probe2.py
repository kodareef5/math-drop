import numpy as np
from seeds import *
rng=np.random.default_rng(0)
for N in [257,1021]:
  for beta in [0,1,2,4,8]:
    for H in [1,2,4]:
      Fs=[];Fg=[];E=[]
      for rep in range(3):
        k=np.arange(N); X=relaxed_chirp(N,H,rng.permutation(H),v=rng.uniform(0.44,0.5),phi=rng.random())
        if beta>0: X=np.tanh(beta*X)/np.tanh(beta)
        M=1<<int(np.ceil(np.log2(16*N)))
        E.append(np.abs(np.fft.fft(X,M)).max()/np.sqrt(N))
        Fs.append(merit(np.where(X>=0,1,-1))); Fg.append(merit(greedy_l4_round(X)))
      print(f"N={N} beta={beta} H={H} energy={np.mean(X**2):.2f} relaxedmax={np.mean(E):.2f} F_sign={np.mean(Fs):.2f} F_greedy={np.mean(Fg):.2f} max={max(Fg):.2f}")
