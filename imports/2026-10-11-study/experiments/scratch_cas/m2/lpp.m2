needsPackage "LexIdeals";
R = QQ[a,b,c];
setRandomSeed 7;
-- I contains a regular sequence of degrees 2,2,3 plus one extra cubic
f = {random(2,R), random(2,R), random(3,R), random(3,R)};
I = ideal f;
h = hilbertFunct I;
print("HF of I: " | toString h);
L = LPP(R, h, {2,2,3});
print("LPP ideal: " | toString L);
bI = betti res I; bL = betti res L;
print(bI); print(bL);
print("LPP has HF equal: " | toString(hilbertFunct L == h));
print("Betti(I) <= Betti(LPP) entrywise: " | toString(all(keys bI, k -> bI#k <= (if bL#?k then bL#k else 0))));
-- non-Artinian (c<n) case is not supported by LPP(): powers list must have length n
print("LPP with 2 powers in 3 vars -> " | toString(LPP(R, {1,3,4,4}, {2,2})));
