\\ Validate Lambda(b) = -R/(b(1-b)) + I(b), R=h/w, theta(t)=sum_{a} exp(-2 pi N(a) t / sqrt(d)), for imaginary quadratic K
default(realprecision, 38);
chk(D, b) = {
  my(d=-D, K=bnfinit(x^2-D), h=K.no, w=K.tu[1], L=lfuncreate(D), R=h/w, a=2*Pi/sqrt(d), N=400, an, I, Lam);
  \\ ideal counts a_n = sum_{m|n} chi(m)
  an = vector(N*40, n, sumdiv(n, m, kronecker(D, m)));
  I = sum(n=1, #an, if(an[n], an[n]*( incgam(b, a*n)*(a*n)^(-b) + incgam(1-b, a*n)*(a*n)^(b-1) ), 0));
  Lam = (sqrt(d)/(2*Pi))^b * gamma(b) * zeta(b) * lfun(L, b);
  [D, h, w, b, Lam, -R/(b*(1-b)) + I];
}
print(chk(-23, 0.9));
print(chk(-163, 0.95));
print(chk(-4, 0.8));
quit
