default(realprecision, 30);
t1(b, a) = a^(-b)*incgam(b, a) + a^(b-1)*incgam(1-b, a);
\\ simple explicit choice b = 1 - 1/log(d) (valid while 1/log d < 1/8, i.e. d > e^8)
hs(d) = { my(a = 2*Pi/sqrt(d), b = 1 - 1/log(d)); 2*b*(1-b)*t1(b, a); }
tat(d) = 0.655/(Pi*exp(1))*sqrt(d)/log(d);
mn = 1e9; argL = 0;
forstep(L = 11.2, 700, 0.05, d = exp(L); r = hs(d)/tat(d); if(r < mn, mn = r; argL = L));
printf("min over log|D| in [11.2,700] of Hecke(b=1-1/log d)/Tatuzawa = %.4f at log|D| = %.2f\n", mn, argL);
quit
