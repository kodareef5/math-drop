LoadPackage("hap");;
Print("HAP version ", PackageInfo("hap")[1].Version, "\n");
# affine A~2 (triangle of 3s) -- non-spherical; K(pi,1) known (affine, Okonek 1979 / Charney-Peifer for A~n)
D := [[1,[2,3],[3,3]],[2,[3,3]]];;
t := Runtime();;
R := ResolutionArtinGroup(D,4);;
TR := TensorWithIntegers(R);;
Print("A~2 homology H1..H3: ", List([1..3], i->Homology(TR,i)), "  ms=", Runtime()-t, "\n");
# (3,3,oo) triangle -- dimension 2; K(pi,1) known (Charney-Davis dim<=2) 
D2 := [[1,[2,3],[3,0]],[2,[3,3]]];;
R2 := ResolutionArtinGroup(D2,3);; TR2 := TensorWithIntegers(R2);;
Print("(3,3,oo) homology H1..H2: ", List([1..2], i->Homology(TR2,i)), "\n");
# A non-FC, rank-4 example with labels 3 and oo containing an A3 subdiagram and an affine A~2 triangle:
# vertices 1-2-3 path (A3), 4 joined to 1,2,3 by 3,3,oo  -- previously covered? (dim 3 -> Huang-Przytycki 2025)
D3 := [[1,[2,3],[4,3]],[2,[3,3],[4,3]],[3,[4,0]]];;
R3 := ResolutionArtinGroup(D3,4);; TR3 := TensorWithIntegers(R3);;
Print("rank-4 example homology H1..H3: ", List([1..3], i->Homology(TR3,i)), "\n");
# the Word problem: equality test in R.group (fp group)
G := R!.group;; g := GeneratorsOfGroup(G);;
Print("fp-group generators: ", g, "\n");
QUIT;
