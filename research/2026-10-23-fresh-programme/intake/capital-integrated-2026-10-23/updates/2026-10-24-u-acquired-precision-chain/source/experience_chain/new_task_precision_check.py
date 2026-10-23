"""Exact algebra behind the adaptive noisy new-solution lower-bound note."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math


def mm(A, B):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]


def mv(A, x):
    return [sum(a*b for a,b in zip(row,x)) for row in A]


def dot(x, y):
    return sum(a*b for a,b in zip(x,y))


def cube_check():
    p, n = 4, 6
    delta, beta, a = F(3,2), F(3,5), F(3,5)
    b = [F(1)]+[F(0)]*(n-1)
    I = [[F(i==j) for j in range(n)] for i in range(n)]
    worlds = {}
    estimates_checked = 0
    for theta in product([-1,1],repeat=p):
        v = [F(0),F(4,5)]+[F(3,10)*s for s in theta]
        assert dot(v,v)==1 and dot(b,v)==0
        t = [x+y for x,y in zip(b,v)]
        A = [[I[i][j]+delta*t[i]*t[j]/2 for j in range(n)] for i in range(n)]
        inv = [[I[i][j]-beta*t[i]*t[j]/2 for j in range(n)] for i in range(n)]
        x = [(1-beta/2)*bi-beta*vi/2 for bi,vi in zip(b,v)]
        assert mm(A,inv)==I and mv(A,x)==b and mv(inv,b)==x
        worlds[theta]=(v,A,x,t)
        # Each coordinate is correct, zero, or the sign-flipped exact coordinate.
        for modes in product([0,1,2],repeat=p):
            xhat=x.copy()
            for j,mode in enumerate(modes):
                xhat[j+2] = [x[j+2],F(0),-x[j+2]][mode]
            decoded=tuple(1 if -xhat[j+2]>=0 else -1 for j in range(p))
            H=sum(a0!=b0 for a0,b0 in zip(decoded,theta))
            error=sum((aa-bb)**2 for aa,bb in zip(xhat,x))
            assert error >= beta**2*a**2*H/(4*p)
            estimates_checked+=1

    adjacent=0
    for theta,(v,A,x,t) in worlds.items():
        for j in range(p):
            other=list(theta); other[j]*=-1; other=tuple(other)
            if theta>other:
                continue
            w,Aw,xw,tw=worlds[other]
            dv2=sum((aa-bb)**2 for aa,bb in zip(v,w))
            assert dv2==4*a*a/p
            inner=dot(t,tw)/2
            op2=delta**2*(1-inner**2)
            D=[[aa-bb for aa,bb in zip(ar,br)] for ar,br in zip(A,Aw)]
            D2=mm(D,D); D3=mm(D2,D)
            assert D3==[[op2*aa for aa in row] for row in D]
            assert sum(D2[i][i] for i in range(n))==2*op2
            assert op2<=delta**2*dv2/2
            # One action of energy B has KL <= op2*B/(2 sigma^2).
            assert op2/2 <= delta**2*a*a/p
            assert sum((aa-bb)**2 for aa,bb in zip(x,xw))==beta**2*dv2/4
            adjacent+=1
    return {"worlds":len(worlds),"adjacent_pairs":adjacent,
            "rational_estimates":estimates_checked,
            "status":"all exact inverse, spectral, KL and sign-error checks passed"}


def constant_check():
    alpha, epsilon, beta, delta, sigma, p = F(1,20),F(1,100),F(3,5),F(3,2),F(1,5),62
    c=1-2*alpha
    d=8*(1-alpha)*epsilon**2/beta**2
    astar2=3*d/c
    assert 0<astar2<=1
    derivative=lambda t: -c*c/t**2+4*c*d/t**3-3*d*d/t**4
    assert derivative(astar2)==0
    assert derivative(astar2*F(3,4))>0
    assert derivative(astar2*F(4,3))<0
    direct=2*sigma**2*p/delta**2*(c-d/astar2)**2/astar2
    closed=sigma**2*p*c**3/(27*(1-alpha)*(1+delta)**2*epsilon**2)
    assert direct==closed
    kl=float(c)*math.log(float((1-alpha)/alpha))
    binary=float(sigma**2/(4*(1+delta)**2*epsilon**2))*kl
    # The q=1 exception uses Gaussian sign classification, not 1/epsilon^2.
    sign_exposure=8*float(sigma**2/delta**2)*math.log(1/float(alpha))
    return {"optimized_a_squared":str(astar2),
            "dimension_bound_exact":str(closed),"dimension_bound_float":float(closed),
            "binary_bound_float":binary,"q1_sign_exposure_upper":sign_exposure}


def main():
    out={"status":"PASS","cube":cube_check(),"constants":constant_check(),
         "scope":"Exact algebra check; the proof, not finite enumeration, covers adaptive algorithms."}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
