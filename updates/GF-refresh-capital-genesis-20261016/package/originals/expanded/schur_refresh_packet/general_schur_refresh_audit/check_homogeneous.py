from fractions import Fraction as F
from math import comb
import numpy as np
from scipy.optimize import minimize
import json

def reduced(m,eta=F(1,4)):
    return [[sum((F(comb(w,l)*comb(m-w,v-l))*eta**(w+v-2*l)
        for l in range(max(0,v-(m-w)),min(w,v)+1)),F(0))/comb(m,v)
        for v in range(1,m+1)] for w in range(1,m+1)]

def explicit_check(m):
    R=reduced(m); n=2**m
    groups=[[j for j in range(1,n) if j.bit_count()==w] for w in range(1,m+1)]
    for w in range(m):
        for v in range(m):
            entry=sum((F(1,4)**((j^k).bit_count()) for j in groups[w] for k in groups[v]),F(0))/len(groups[w])/len(groups[v])
            assert entry==R[w][v]
            assert R[w][v]==R[v][w]
    return True

def certify(m):
    R=reduced(m); B=np.array(R,dtype=float); c=np.array([.25**w for w in range(1,m+1)])
    alpha=F(1,16); h=F(3,16); Q=F(7,16)
    # Splitting u into positive and negative parts makes the l1 ball a simplex.
    def unpack(x): return x[:m]-x[m:]
    def fun(x):
        u=unpack(x); return float(alpha)*u@B@u-2*float(h)*c@u
    def jac(x):
        u=unpack(x); g=2*float(alpha)*B@u-2*float(h)*c
        return np.r_[g,-g]
    x0=np.zeros(2*m)
    opt=minimize(fun,x0,jac=jac,method='SLSQP',bounds=[(0,None)]*(2*m),constraints=[{'type':'ineq','fun':lambda x:1-sum(x),'jac':lambda x:-np.ones(2*m)}],options={'ftol':1e-13,'maxiter':500})
    # A denominator-10^10 rational candidate is projected radially if rounding exceeds l1=1.
    D=10**10
    raw=[F(round(float(v)*D),D) for v in unpack(opt.x)]
    norm=sum(map(abs,raw)); u=[v/max(F(1),norm) for v in raw]
    Bu=[sum((R[i][j]*u[j] for j in range(m)),F(0)) for i in range(m)]
    quad=sum((u[j]*Bu[j] for j in range(m)),F(0))
    cv=[F(1,4)**w for w in range(1,m+1)]
    g=[h*cv[j]-alpha*Bu[j] for j in range(m)]
    lower=Q+2*h*sum((cv[j]*u[j] for j in range(m)),F(0))-alpha*quad
    upper=Q+alpha*quad+2*max(map(abs,g))
    assert upper>=lower
    if m in [2,32]: assert upper==lower
    if m==2: assert lower==F(255,512)
    return {'m':m,'eta':'1/4','p':'1/4','q':'1/4','solver_success':bool(opt.success),'solver_message':str(opt.message),'iterations':int(opt.nit),'nonzero_rational_u':{str(i+1):str(v) for i,v in enumerate(u) if v},'lower':str(lower),'upper':str(upper),'gap':str(upper-lower),'decimal_value':float(lower),'active_tangent_weight':1+max(range(m),key=lambda i:abs(g[i])),'unconstrained_l1':str(3*((F(5,4)**m)-1))}

out={'explicit_full_matrix_checks':{str(m):explicit_check(m) for m in range(1,6)},'examples':[certify(2),certify(32)]}
print(json.dumps(out,indent=2))
