default(realprecision, 28);
t1(b, a) = a^(-b)*incgam(b, a) + a^(b-1)*incgam(1-b, a);
hbopt(d) = { my(a = 2*Pi/sqrt(d), best = 0, v, b); for(k = 0, 400, b = 1 - (1/8)*exp(-k/40.); v = 2*b*(1-b)*t1(b, a); if(v > best, best = v)); best; }
cross(H) = { my(lo = 10., hi = 1e16, m); for(i = 1, 120, m = sqrt(lo*hi); if(hbopt(m) > H, hi = m, lo = m)); hi; }
for(i = 1, 5, H = [10, 25, 100, 457, 2900][i]; printf("H=%d  opt-b Hecke search bound: %.4e\n", H, cross(H)));
printf("opt-b coverage: 2e10 -> h<=%.0f ; 1e11 -> h<=%.0f ; 2^40 -> h<=%.0f\n", hbopt(2e10), hbopt(1e11), hbopt(2.^40));
quit
