default(realprecision, 28);
t1(b, a) = a^(-b)*incgam(b, a) + a^(b-1)*incgam(1-b, a);
hb78(d) = { my(a = 2*Pi/sqrt(d)); 2*(7/8)*(1/8)*t1(7/8, a); }
\\ (1) sanity: h(D) >= hb78(|D|) for all fundamental D<0, 4<|D|<=N
N = 400000; worst = [10^9, 0, 0];
{ for(n = 5, N, if(n%4==1 || n%4==2, next); if(!isfundamental(-n), next);
   my(h = qfbclassno(-n), r = h / hb78(n)); if(r < worst[1], worst = [r, -n, h])); }
print("min h/HeckeBound over 4<|D|<=", N, " : ", worst);
\\ (2) optimized-b Hecke bound vs Tatuzawa over a wide range (b = 1 - u, u log-grid)
hbopt(d) = { my(a = 2*Pi/sqrt(d), best = 0, v, b); for(k = 0, 400, b = 1 - (1/8)*exp(-k/40.); v = 2*b*(1-b)*t1(b, a); if(v > best, best = v)); best; }
tat(d) = 0.655/(Pi*exp(1))*sqrt(d)/log(d);
for(e = 5, 60, if(e%5, next); d = 10.^e; printf("1e%d: HeckeOpt/Tatuzawa = %.3f\n", e, hbopt(d)/tat(d)));
printf("e^11.2: HeckeOpt=%.3f Tat=%.3f\n", hbopt(exp(11.2)), tat(exp(11.2)));
quit
