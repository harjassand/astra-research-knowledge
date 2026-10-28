"""Exploratory SOS polyconvex support, distinct from a heat identity.

Ordinary SOS-polyconvexity machinery (Fantuzzi et al.2604.11124) applied
to the candidate. Numerical success is not an exact certificate and
numerical failure is not an infeasibility proof.
"""
import json,time
from pathlib import Path
import sympy as s
import numpy as np

def build(coefficients=None, multiplier='auto'):
    a=s.symbols('a0:4');x=s.symbols('x0:4');allvars=a+x
    if coefficients is None:coefficients=(1,1,16,-13,0,0,4,-4,0)
    p=tuple(map(s.Rational,coefficients))
    if len(p)!=9:raise ValueError('nine coefficients required')
    def inv(y):
        aa,b,c,d=y
        return aa*aa+c*c,b*b+d*d,aa*b+c*d,aa*d-b*c
    def F(y):
        u,v,w,q=inv(y)
        basis=(u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w)
        return sum(c*t for c,t in zip(p,basis))
    f=F(a)
    P=s.Poly(s.expand(F(tuple(ai+xi for ai,xi in zip(a,x)))-f-
        sum(s.diff(f,ai)*xi for ai,xi in zip(a,x))),allvars)
    ua,va,wa,qa=inv(a);qx=inv(x)[3]
    candidate_symmetry=(p[0]==p[1] and p[4]==p[5]==p[8]==0 and p[6]==-p[7])
    if multiplier=='auto':multiplier='candidate' if candidate_symmetry else 'SO2'
    if multiplier=='candidate':
        if not candidate_symmetry:raise ValueError('candidate input symmetries absent')
        multiplier_basis=[ua-va,qa]
    elif multiplier=='SO2':multiplier_basis=[ua,va,wa,qa]
    else:raise ValueError('unknown multiplier basis')
    lambdas=[s.Poly(t*qx,allvars) for t in multiplier_basis]
    z=[ai*xi for ai in a for xi in x]+[x[i]*x[j] for i in range(4) for j in range(i,4)]
    terms=[(i,j,s.Poly(z[i]*z[j],allvars)) for i in range(len(z)) for j in range(i,len(z))]
    monoms=sorted(set(P.monoms()).union(*(set(t.monoms()) for _,_,t in terms),
                                         *(set(t.monoms()) for t in lambdas)))
    lookup={e:i for i,e in enumerate(monoms)}
    M=np.zeros((len(monoms),len(terms)+len(lambdas)));b=np.zeros(len(monoms))
    for e,c in P.terms():b[lookup[e]]=float(c)
    for col,(i,j,p) in enumerate(terms):
        for e,c in p.terms():M[lookup[e],col]=float(c)*(1 if i==j else np.sqrt(2))
    for offset,p in enumerate(lambdas):
        for e,c in p.terms():M[lookup[e],len(terms)+offset]=float(c)
    weights=np.linalg.norm(M,axis=1)
    M=M/weights[:,None];b=b/weights
    return M,b,terms,monoms,P,lambdas,z

def solve(max_seconds=30):
    started=time.monotonic()
    M,b,terms,monoms,P,lambdas,z=build();n=len(z)
    U,S,Vt=np.linalg.svd(M,full_matrices=False)
    rank=int(np.sum(S>1e-10));pinv=(Vt[:rank].T/S[:rank])@U[:,:rank].T
    def aff(v):return v+pinv@(b-M@v)
    def mat(v):
        q=np.zeros((n,n))
        for c,(i,j,_) in zip(v,terms):q[i,j]=q[j,i]=c if i==j else c/np.sqrt(2)
        return q
    def vec(q,theta):
        return np.array([q[i,j]*(1 if i==j else np.sqrt(2)) for i,j,_ in terms]+list(theta))
    def pos(v):
        q=mat(v);e,R=np.linalg.eigh(q)
        return vec((R*np.maximum(e,0))@R.T,v[-2:])
    current=aff(np.zeros(M.shape[1]));best=None
    for it in range(100000):
        psd=pos(current);next_aff=aff(2*psd-current)
        error=np.linalg.norm(next_aff-psd)
        if best is None or error<best[0]:best=(error,next_aff.copy(),it)
        current+=next_aff-psd
        if it%1000==0:print('iteration',it,'residual',error,'lambda',next_aff[-2:].tolist(),flush=True)
        if error<1e-8 or time.monotonic()-started>max_seconds:break
    error,answer,itbest=best;Q=mat(answer)
    record={'status':'NUMERICAL_FEASIBILITY_ONLY','coefficient_basis':'lambda=alpha*(u-v)+delta*q',
            'alpha_delta':answer[-2:].tolist(),'best_projection_residual':float(error),
            'eigen_min':float(np.linalg.eigvalsh(Q)[0]),'affine_residual':float(np.max(np.abs(M@answer-b))),
            'iterations':it+1,'best_iteration':itbest,'wall_seconds':time.monotonic()-started,
            'features':n,'constraints':M.shape[0],'rank':rank,'gram':Q.tolist(),
            'interpretation':'NO_QC_OR_POLYCONVEXITY_CLAIM_UNTIL_EXACT_CHECK'}
    Path('poly_support_search.json').write_text(json.dumps(record,indent=2)+'\n')
    np.savez('poly_support_maps.npz',M=M,b=b,answer=answer)
    print({k:v for k,v in record.items() if k!='gram'})

if __name__=='__main__':solve()
