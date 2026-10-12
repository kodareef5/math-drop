H = 100; cnt = vector(H); mx = vector(H);
{
for(n = 19000001, 37350000,
  if(n % 4 == 1 || n % 4 == 2, next);
  if(!isfundamental(-n), next);
  my(h = qfbclassno(-n));
  if(h <= H, cnt[h]++; mx[h] = n));
}
for(h = 1, H, print(h, " ", cnt[h], " ", mx[h]));
quit
