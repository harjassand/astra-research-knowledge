"""Source-complete rational tensor residual verification.
The witness and operators are interpreted as exact rationals. No global state
vector, sampled residual, approximate eigenvalue, or discarded tail is used.
"""
from fractions import Fraction as F
from math import lcm
from functools import reduce
import time
import numpy as np
from scipy.linalg import solve


def dyadic(x,bits=42):
    # Round the exact IEEE value to a nearest dyadic; the resulting witness is exact.
    a,b=float(x).as_integer_ratio();return F(round(F(a*(1<<bits),b)),1<<bits)

def integer_core(A,bits=42):
    den=1<<bits
    out=np.array([int(dyadic(x,bits)*den) for x in np.asarray(A).ravel()],dtype=object).reshape(A.shape)
    return out,den

def rational_array(A):
    aa=[F(x) for x in np.asarray(A,dtype=object).ravel()];den=lcm(*(x.denominator for x in aa));num=np.array([int(x*den) for x in aa],dtype=object).reshape(np.asarray(A).shape)
    return num,den

def witness(c,V,bits=42):
    return [integer_core(a/p[None,:,None],bits) for a,p in zip(V,c.rootprob)]

def product_term(vs):return [(rational_array(np.array(v,dtype=object).reshape(1,-1,1))) for v in vs]

def apply_one(term,v):
    out=[]
    for M,(a,den) in zip(term,v):
        N,D=rational_array(M)
        if all(N[i,j]==0 for i in range(len(N)) for j in range(len(N)) if i!=j):z=a*np.diag(N)[None,:,None]
        else:z=(N@a.transpose(1,0,2).reshape(a.shape[1],-1)).reshape(a.shape[1],a.shape[0],a.shape[2]).transpose(1,0,2)
        out.append((z,den*D))
    return out

def negative(v):
    z=list(v);z[0]=(-z[0][0],z[0][1]);return z

def dot(c,A,B):
    E=np.ones((1,1),dtype=object);den=1
    for (a,da),(b,db),mass in zip(A,B,c.mass):
        tmp=(E@b.reshape(b.shape[0],-1)).reshape(a.shape[0],a.shape[1],b.shape[2]);tmp=tmp*np.array(mass,dtype=object)[None,:,None]
        E=a.reshape(-1,a.shape[2]).T@tmp.reshape(-1,b.shape[2]);den*=da*db*sum(mass)
    return F(int(E[0,0]),den)

def dot_sums(c,As,Bs,same=False):
    ans=F(0)
    if same:
        for i,a in enumerate(As):
            ans+=dot(c,a,a)
            for b in As[:i]:ans+=2*dot(c,a,b)
    else:
        for a in As:
            for b in Bs:ans+=dot(c,a,b)
    return ans

def alpha_bound(c,bits=46):
    b=next(b for b,g in enumerate(c.groups) if c.model['target'] in g);K=c.refraw[b];u0=solve(np.array(K,float),np.ones(len(K)),check_finite=False)
    u=[dyadic(x,bits) for x in u0]
    if min(u)<=0:raise ValueError('Nonpositive reference MFPT witness')
    d=max(abs(sum(F(K[i,j])*u[j] for j in range(len(K)))-1) for i in range(len(K)))
    if d>=1:raise ValueError('Reference residual too large')
    return (1-d)/max(u),{'reference_residual':str(d),'reference_max_trial':str(max(u)),'reference_local_states':len(K)}

def certify(c,V,source_vectors=None,bits=42,return_data=False):
    t=time.perf_counter();v=witness(c,V,bits);sources=[product_term(vs) for vs in (c.wterms if source_vectors is None else source_vectors)]
    av=[apply_one(M,v) for M in c.rawterms]
    r=sources+[negative(a) for a in av]
    bv=dot_sums(c,sources,[v]);energy=dot_sums(c,[v],av);rr=dot_sums(c,r,r,same=True)
    if rr<0:raise ArithmeticError('Negative exact squared residual')
    alpha,ad=alpha_bound(c);L=2*bv-energy;U=L+rr/alpha
    ans={'lower':str(L/c.Z),'upper':str(U/c.Z),'ratio':str(U/L) if L>0 else None,'lower_float':float(L/c.Z),'upper_float':float(U/c.Z),'ratio_float':float(U/L) if L>0 else None,'residual_squared':str(rr),'alpha_lower':str(alpha),'seconds':time.perf_counter()-t,'witness_dyadic_bits':bits,'norm_term_count':len(r),'scope':'exact rational full-source tensor enclosure for the declared model','reference_check':ad}
    if return_data:return ans,dict(v=v,source=sources,av=av,residual=r,L=L,U=U,alpha=alpha)
    return ans

def sqrt_upper(x,bits=80):
    from math import isqrt
    n=(x.numerator*(1<<(2*bits))+x.denominator-1)//x.denominator
    a=isqrt(n)
    if a*a<n:a+=1
    return F(a,1<<bits)

def cross_certificate(c,d1,d2):
    a=min(d1['alpha'],d2['alpha']);G=dot_sums(c,d1['source'],[d2['v']])+dot_sums(c,d2['source'],[d1['v']])-dot_sums(c,[d1['v']],d2['av'])
    g11=dot_sums(c,d1['residual'],d1['residual'],True)/a;g22=dot_sums(c,d2['residual'],d2['residual'],True)/a;g12=dot_sums(c,d1['residual'],d2['residual'])/a;s=sqrt_upper(g11*g22)
    lo=G+(g12-s)/2;hi=G+(g12+s)/2
    return {'lower':str(lo),'upper':str(hi),'lower_float':float(lo),'upper_float':float(hi),'ratio_float':float(hi/lo) if lo>0 else None,'scope':'two-load exact-rational prepared-source enclosure'}
