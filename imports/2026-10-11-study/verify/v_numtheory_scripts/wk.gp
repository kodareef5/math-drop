\\ enumerate fundamental D<0 with |D| <= B, tally class numbers h <= H
H = 25; B = 31692000;  \\ B(25) from Tatuzawa bound = 3.1692e7
cnt = vector(H); mx = vector(H);
{
for(n = 3, B,
  if(n % 4 == 1 || n % 4 == 2, next);
  D = -n;
  if(!isfundamental(D), next);
  h = qfbclassno(D);
  if(h <= H, cnt[h]++; mx[h] = n));
}
for(h = 1, H, print(h, " ", cnt[h], " ", mx[h]));
quit
