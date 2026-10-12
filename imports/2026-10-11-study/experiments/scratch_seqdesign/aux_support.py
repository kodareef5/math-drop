# Box bound on the support of p_j: degree of p_j in y_i is 2^(j-i)  => |supp| <= prod_i (2^(j-i+1)+1)
import math
for j in [5,10,20,30,50,100]:
    lb=sum(math.log10(2**(j-i+1)+1) for i in range(1,j+1))
    print(j, f"log10(box bound) = {lb:.1f}")
