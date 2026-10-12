LoadPackage("hap");;
# E10 = T(2,3,7): vertex 1 centre; arms 1-2 ; 1-3-4 ; 1-5-6-7-8-9-10
D := [[1,[2,3],[3,3],[5,3]],[3,[4,3]],[5,[6,3]],[6,[7,3]],[7,[8,3]],[8,[9,3]],[9,[10,3]]];;
t := Runtime();;
R := ResolutionArtinGroup(D,4);;
Print("E10 cells in dims 0..3: ", List([0..3], i->R!.dimension(i)), "\n");
TR := TensorWithIntegers(R);;
Print("E10 Artin group H1,H2: ", List([1..2], i->Homology(TR,i)), "  ms=", Runtime()-t, "\n");
QUIT;
