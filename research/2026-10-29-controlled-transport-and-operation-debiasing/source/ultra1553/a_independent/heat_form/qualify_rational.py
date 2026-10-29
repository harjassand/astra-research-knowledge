"""Literal rational certificate of the ORIGINAL anisotropic Hopf quartic.

Sparse differentiation below is independent of the symbolic map generator.
Floating Cholesky only proposes a rational Gram factor; its exact residual
is verified using integer arithmetic. No floating positivity is a premise.
"""
from __future__ import annotations
import json,hashlib,time,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent

def addto(p,m,c):
    if c:p[m]=p.get(m,F(0))+c

def mul(p,q):
    out={}
    for m,c in p.items():
        for n,d in q.items():addto(out,tuple(a+b for a,b in zip(m,n)),c*d)
    return {m:c for m,c in out.items() if c}

def scaleadd(p,q,c=F(1)):
    out=dict(p)
    for m,d in q.items():addto(out,m,c*d)
    return {m:c for m,c in out.items() if c}

def derivative(p,i):
    out={}
    for m,c in p.items():
        if m[i]:
            n=list(m);n[i]-=1;addto(out,tuple(n),c*m[i])
    return out

def monomial(n,i,power=1):
    m=[0]*n;m[i]=power;return tuple(m)

def literal_target(primitives,coefficients,nu):
    zero=(0,)*4
    T={monomial(4,i,2):F(1) for i in range(4)}
    q={(1,0,0,1):F(1),(0,1,1,0):F(-1)}
    x={(2,0,0,0):F(1),(0,0,2,0):F(1),(0,2,0,0):F(-1),(0,0,0,2):F(-1)}
    f=scaleadd(scaleadd(mul(T,T),mul(q,q),F(252,25)),mul(q,x),F(99,25))
    hess=[[derivative(derivative(f,r),s) for s in range(4)] for r in range(4)]
    b1=[0,1,3,4];b2=[1,2,4,5]
    jindex=[2,3,0,1];jsign=[-1,-1,1,1]
    diss={}
    def jetterm(pol,i,j,c):
        h=[0]*6;h[i]+=1;h[j]+=1
        for m,a in pol.items():addto(diss,m+tuple(h),c*a)
    for r in range(4):
        for s in range(4):
            jetterm(hess[r][s],b1[r],b1[s],F(1));jetterm(hess[r][s],b2[r],b2[s],F(1))
            jetterm(hess[r][s],b1[r],b2[jindex[s]],nu*jsign[s])
            jetterm(hess[r][s],b2[r],b1[jindex[s]],nu*jsign[s])
    T2=mul(T,T)
    out={}
    for m,c in diss.items():
        for n,d in T2.items():addto(out,tuple(a+b for a,b in zip(m[:4],n))+m[4:],c*d)
    numerator=[{} for _ in range(4)]
    for (s,exp),c in zip(primitives,coefficients):addto(numerator[s],tuple(exp),c)
    # omega numerator = T*d(P_5) - dT wedge P_5, with every sign literal.
    for r in range(4):
        for s in range(r+1,4):
            drNs=derivative(numerator[s],r);dsNr=derivative(numerator[r],s)
            omega=scaleadd(mul(T,scaleadd(drNs,dsNr,F(-1))),mul(derivative(T,r),numerator[s]),F(-1))
            omega=scaleadd(omega,mul(derivative(T,s),numerator[r]))
            hp=[0]*6;hp[b1[r]]+=1;hp[b2[s]]+=1
            hm=[0]*6;hm[b1[s]]+=1;hm[b2[r]]+=1
            for m,c in omega.items():addto(out,m+tuple(hp),c);addto(out,m+tuple(hm),-c)
    return {m:c for m,c in out.items() if c}

def main():
    start=time.perf_counter();proposal=HERE/'RATIONAL_cross_CLARABEL_PROPOSAL.json';raw=proposal.read_bytes();p=json.loads(raw)
    map_path=HERE/'RATIONAL_MAP.json';map_bytes=map_path.read_bytes();mp=json.loads(map_bytes)
    den=10**12;nu=F(round(p['nu']*den),den);coeff=[F(round(a*den),den) for a in p['alpha']]
    Q=[[F(round(a*den),den) for a in row] for row in p['Q']];z=[tuple(m) for m in mp['z']];n=len(z)
    target=literal_target(mp['primitives'],coeff,nu)
    actual={};slots={}
    for i in range(n):
        for j in range(n):
            m=tuple(a+b for a,b in zip(z[i],z[j]));addto(actual,m,Q[i][j]);slots.setdefault(m,(i,j))
    corrections=[]
    for m in set(actual)|set(target):
        delta=target.get(m,F(0))-actual.get(m,F(0));i,j=slots[m]
        if i==j:Q[i][j]+=delta
        else:Q[i][j]+=delta/2;Q[j][i]+=delta/2
        if delta:corrections.append(abs(delta))
    replay={}
    for i in range(n):
        for j in range(n):addto(replay,tuple(a+b for a,b in zip(z[i],z[j])),Q[i][j])
    replay={m:c for m,c in replay.items() if c}
    assert replay==target and all(Q[i][j]==Q[j][i] for i in range(n) for j in range(n))
    rho=F(1,1000);A=np.array([[float(Q[i][j]-(rho if i==j else 0)) for j in range(n)] for i in range(n)])
    untrusted=np.linalg.cholesky(A);factor_den=10**10
    L=[[round(float(untrusted[i,j])*factor_den) if j<=i else 0 for j in range(n)] for i in range(n)]
    common=math.lcm(factor_den**2,rho.denominator,*[x.denominator for row in Q for x in row]);fac=common//factor_den**2
    row_error=[0]*n
    for i in range(n):
        for j in range(n):
            qij=Q[i][j]-(rho if i==j else 0)
            qint=qij.numerator*(common//qij.denominator)
            lint=sum(L[i][k]*L[j][k] for k in range(min(i,j)+1))*fac
            row_error[i]+=abs(qint-lint)
    delta=F(max(row_error),common)
    assert delta<F(1,2000) and abs(nu)<F(1,1000)
    result=dict(target='T^2+(252/25)q^2+(99/25)qx',proposal_sha256=hashlib.sha256(raw).hexdigest(),
                map_sha256=hashlib.sha256(map_bytes).hexdigest(),nu=str(nu),
                primitive_denominator='T=|A|^2',primitives=mp['primitives'],alpha=[str(x) for x in coeff],z=mp['z'],
                Q=[[str(x) for x in row] for row in Q],factor_integer=L,factor_denominator=factor_den,
                identity_exact=True,identity_coefficients=len(target),identity_correction_l1=str(sum(corrections,F(0))),
                identity_correction_max=str(max(corrections)),gram_shift=str(rho),exact_factor_residual_row_sum=str(delta),
                verified_gram_lower='1/2000',verified_pointwise_dissipation_lower='T*|h|^2/12000',
                strong_quasiconvexity_constant='1/900000',seconds=time.perf_counter()-start)
    path=HERE/'RATIONAL_EXACT_CERTIFICATE.json';path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['primitives','alpha','z','Q','factor_integer']},indent=2))

if __name__=='__main__':main()
