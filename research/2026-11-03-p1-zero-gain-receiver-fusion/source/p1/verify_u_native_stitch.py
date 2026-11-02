"""Finite exact stoichiometric checks for the U-native stitching proof.
No assertion about stochastic recurrence is inferred from the finite check.
"""
from itertools import product

# I-port (A,B,C) changes; II-port is the symmetric copy.
R={
 '0':(1,1,0),
 '1':(1,0,1),
 '2':(1,1,1),
 '3':(-3,-2,-2)
}

def f(k):return 2*(k%2)+k//2

def psi(x,a=11):
    A,B,C,D,E,F=x
    r1,r2=B-C,E-F
    t1,t2=min(B,C),min(E,F)
    return 3*max(0,r1)+a*max(0,-r1)+3*max(0,r2)+a*max(0,-r2)+f(t1)+f(t2)

def apply(x,port,src):
    s=list(x);d=R[src]
    ids=(0,1,2) if port==0 else (3,4,5)
    for i,u in zip(ids,d):s[i]+=u
    return tuple(s) if min(s)>=0 else None

def enabled(x,port,src):
    a,b,c = (x[:3] if port==0 else x[3:])
    if src=='0':return True
    if src=='1':return a>=1 and b>=1
    if src=='2':return a>=2 and b>=1 and c>=1
    if src=='3':return a>=3 and b>=2 and c>=2

def core(x,forward):
    s=list(x)
    if forward:
        if not(x[0]>=1 and x[3]>=1 and x[1]>=2 and x[2]>=2):return None
        for i,d in [(1,-2),(2,-2),(4,2),(5,2)]:s[i]+=d
    else:
        if not(x[0]>=1 and x[3]>=1 and x[4]>=2 and x[5]>=2):return None
        for i,d in [(1,2),(2,2),(4,-2),(5,-2)]:s[i]+=d
    return tuple(s)

n=0
for x in product(range(0,6),range(0,10),range(0,10),range(0,6),range(0,7),range(0,7)):
    old=psi(x)
    for port in (0,1):
        for src in R:
            if enabled(x,port,src):
                y=apply(x,port,src)
                assert y is not None
                assert abs(psi(y)-old)<=12,(x,port,src,psi(y)-old)
                n+=1
    for forward in (True,False):
        y=core(x,forward)
        if y is not None:
            assert psi(y)==old,(x,forward,psi(y)-old)
            n+=1

for b,c in product(range(3,25),range(0,13)):
    if b-c<2:continue
    for port in (0,1):
        x=(0,b,c,0,0,0) if port==0 else (0,0,0,0,b,c)
        for word,dpsi in [(('0','1','2','3'),0),(('0','1','1','3'),-3)]:
            y=x
            for src in word:
                assert enabled(y,port,src)
                y=apply(y,port,src)
            assert (psi(y)-psi(x))==dpsi,(x,word,psi(y)-psi(x))
            if dpsi==0:assert y==x
            else:
                ys=list(x);ys[1 if port==0 else 4]-=1
                assert y==tuple(ys)

# Count-gauge vector components and the RHS q + L ell = 4(alpha0+beta0)
def ell(x):return 3*(x[0]+x[3])-4*(x[2]+x[5])
for x in [(0,0,0,0,0,0),(1,2,3,4,5,6),(9,8,7,6,5,4)]:
    for port in (0,1):
        for src,de in [('0',3),('1',-1),('2',-1),('3',-1)]:
            y=tuple(x[i]+(R[src][i%3] if i//3==port else 0) for i in range(6))
            assert ell(y)-ell(x)==de
    assert ell((x[0],x[1]-2,x[2]-2,x[3],x[4]+2,x[5]+2))==ell(x)

print('PASS:',n,'enabled source/core transitions, exact core invariance, safe |DeltaPsi|<=a+1, neutral and good words, count gauge.')
