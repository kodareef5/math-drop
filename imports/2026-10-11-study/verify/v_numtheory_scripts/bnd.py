import math
def B(C,h,lo0=math.exp(11.2)):
    lo,hi=math.e**2,1e40
    for _ in range(400):
        mid=math.sqrt(lo*hi)
        if C*math.sqrt(mid)/math.log(mid)<=h: lo=mid
        else: hi=mid
    return max(lo,lo0)
CT=0.655/(math.pi*math.e)
CH=1.507/11.657/math.pi   # Hoffstein Lemma 1 (q>1e6)
print('Tatuzawa const 0.655/(pi e)=%.6f ; Hoffstein-derived 1.507/(11.657 pi)=%.6f; e^11.2=%.1f'%(CT,CH,math.exp(11.2)))
for h in (1,5,10,20,25,100,457,458,500,957,1000,2900,2901):
    print('h=%5d  B_Tat=%.4e  B_Hoff=%.4e'%(h,B(CT,h),B(CH,h,1e6)))
def hmax(C,X): return C*math.sqrt(X)/math.log(X)
for X,name in ((2e10,'PARI doc 2e10'),(1e11,'JRW 1e11'),(2**40,'MJ 2^40')):
    print('%-14s X=%.4e  Tatuzawa covers h<=%.2f   Hoffstein covers h<=%.2f'%(name,X,hmax(CT,X),hmax(CH,X)))
