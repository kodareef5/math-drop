default(realprecision, 28);
t1(b, a) = a^(-b)*incgam(b, a) + a^(b-1)*incgam(1-b, a);
\\ same narrow zero-free window as Tatuzawa/EKN Lemma 3: b = 1 - 1/(4 log d)
hn(d) = { my(a = 2*Pi/sqrt(d), b = 1 - 1/(4*log(d))); 2*b*(1-b)*t1(b, a); }
tat(d) = 0.655/(Pi*exp(1))*sqrt(d)/log(d);
for(e = 5, 40, if(e%5, next); d = 10.^e; printf("1e%d: Hecke(narrow window)/Tatuzawa = %.3f\n", e, hn(d)/tat(d)));
quit
