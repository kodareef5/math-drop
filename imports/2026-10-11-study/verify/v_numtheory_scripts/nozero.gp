default(realprecision, 28);
t1(b, a) = a^(-b)*incgam(b, a) + a^(b-1)*incgam(1-b, a);
\\ if L(s,chi_D) has no real zero in (0,1) (Watkins 2004: verified for odd chi, q <= 3e8), b may be anywhere in (0,1)
hfree(d) = { my(a = 2*Pi/sqrt(d), best = 0, v); for(k = 1, 999, b = k/1000.; v = 2*b*(1-b)*t1(b, a); if(v > best, best = v)); best; }
printf("|D|=3e8: free-b Hecke bound h >= %.1f\n", hfree(3e8));
printf("|D|=3e8: 7/8-window Hecke bound h >= %.1f\n", 2*(7/8)*(1/8)*t1(7/8, 2*Pi/sqrt(3e8)));
quit
