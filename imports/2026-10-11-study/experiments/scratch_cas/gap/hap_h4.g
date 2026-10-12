LoadPackage("hap");;
# compact hyperbolic Coxeter group [5,3,3,3]: linear diagram 1-5-2-3-3-3-4-3-5
D := [[1,[2,5]],[2,[3,3]],[3,[4,3]],[4,[5,3]]];;
t := Runtime();;
R := ResolutionArtinGroup(D,5);;
Print("ranks of free modules R_0..R_4: ", List([0..4], i->R!.dimension(i)), "\n");
TR := TensorWithIntegers(R);;
Print("[5,3,3,3] Artin group homology H1..H4: ", List([1..4], i->Homology(TR,i)), "  ms=", Runtime()-t, "\n");
QUIT;
