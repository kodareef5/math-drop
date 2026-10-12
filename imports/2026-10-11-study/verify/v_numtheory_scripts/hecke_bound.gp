\\ If L(s,chi_D) != 0 on (7/8,1) then zeta_K(b) <= 0 for b in [7/8,1), and Hecke's identity
\\ Lambda_K(b) = -(h/w)/(b(1-b)) + sum_n a_n [ (an)^-b G(b,an) + (an)^(b-1) G(1-b,an) ] (a = 2pi/sqrt|D|)
\\ gives h >= w b(1-b) * [n=1 term] .  hb(d) = max over a grid of b in [7/8, 1).
default(realprecision, 30);
t1(b, a) = a^(-b)*incgam(b, a) + a^(b-1)*incgam(1-b, a);
hb(d) = { my(a = 2*Pi/sqrt(d), best = 0, v); forstep(b = 0.875, 0.999, 0.001, v = 2*b*(1-b)*t1(b, a); if(v > best, best = v)); best; }
hb78(d) = { my(a = 2*Pi/sqrt(d)); 2*(7/8)*(1/8)*t1(7/8, a); }
tat(d) = 0.655/(Pi*exp(1)) * sqrt(d)/log(d);
for(k = 5, 13, d = 10.^k; printf("|D|=1e%d  Hecke(b=7/8)=%.1f  Hecke(opt b)=%.1f  Tatuzawa=%.1f\n", k, hb78(d), hb(d), tat(d)));
\\ crossover: smallest d with hb78(d) > H
cross(H) = { my(lo = 10., hi = 1e16, m); for(i = 1, 200, m = sqrt(lo*hi); if(hb78(m) > H, hi = m, lo = m)); hi; }
for(i = 1, 7, H = [1, 10, 25, 100, 457, 1000, 2900][i]; printf("H=%d  |D| beyond which Hecke(7/8) bound > H: %.4e\n", H, cross(H)));
printf("coverage at 2e10: h<=%.0f ; at 1e11: h<=%.0f ; at 2^40: h<=%.0f\n", hb78(2e10), hb78(1e11), hb78(2.^40));
quit
