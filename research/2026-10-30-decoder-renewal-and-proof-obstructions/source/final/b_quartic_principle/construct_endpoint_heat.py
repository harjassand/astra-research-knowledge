"""One symmetry/null-face driven cubic heat construction, not a hierarchy.

The exact acoustic zeros remove six Gram directions BEFORE the proposal.
The numerical SDP is not a nonexistence proof and is not a QC test.
"""
from pathlib import Path
import hashlib,json,time
import numpy as np
import sympy as S
import cvxpy as cp


def exponents(total,n):
    if n==1:yield(total,)
    else:
        for j in range(total+1):
            for tail in exponents(total-j,n-1):yield(j,)+tail


def main():
    start=time.perf_counter()
    A=S.symbols('a b c d',real=True);h=S.symbols('h0:6',real=True)
    B1=S.Matrix([h[0],h[1],h[3],h[4]])
    B2=S.Matrix([h[1],h[2],h[4],h[5]])
    q=A[0]*A[3]-A[1]*A[2];T=sum(x*x for x in A)
    x=A[0]**2+A[2]**2-A[1]**2-A[3]**2
    F=T*T+12*q*q+4*q*x
    H=S.hessian(F,A)
    target=S.expand((B1.T*H*B1+B2.T*H*B2)[0])
    z=S.Matrix([a*b for a in A for b in h])
    C,D=S.symbols('C D',real=True)
    kernel=[]
    for a,hv in [([-D,C,C,D],[C,0,0,D,0,0]),([C,-D,D,C],[0,0,C,0,0,D])]:
        sub=dict(zip(A,a))|dict(zip(h,hv))
        zz=z.subs(sub,simultaneous=True)
        for monomial in (C*C,C*D,D*D):
            kernel.append(S.Matrix([S.Poly(v,C,D).coeff_monomial(monomial) for v in zz]))
    N=S.Matrix.hstack(*kernel)
    B=S.Matrix.hstack(*N.T.nullspace())
    assert N.rank()==6 and B.shape==(24,18) and N.T*B==S.zeros(6,18)
    w=B.T*z
    pairs=[(i,j) for i in range(18) for j in range(i,18)]
    grams=[S.expand((1 if i==j else 2)*w[i]*w[j]) for i,j in pairs]
    alpha_powers=list(exponents(3,4));forms=[];alpha_labels=[]
    for coord in range(4):
        for power in alpha_powers:
            mon=S.prod(v**e for v,e in zip(A,power))
            # d(mon dA_coord)(B1,B2).
            correction=sum(S.diff(mon,A[i])*(B1[i]*B2[coord]-B2[i]*B1[coord]) for i in range(4))
            forms.append(S.expand(correction));alpha_labels.append([coord,list(power)])
    allvars=(*A,*h)
    polys=[S.Poly(v,*allvars).as_dict() for v in [target,*grams,*forms]]
    keys=sorted(set().union(*(p.keys() for p in polys)))
    M=np.array([[float(p.get(key,0)) for p in polys[1:]] for key in keys])
    rhs=np.array([float(polys[0].get(key,0)) for key in keys])
    mapping_seconds=time.perf_counter()-start
    G=cp.Variable((18,18),symmetric=True);alpha=cp.Variable(80);margin=cp.Variable()
    vector=cp.hstack([G[i,j] for i,j in pairs])
    constraints=[M[:,:len(pairs)]@vector-M[:,len(pairs):]@alpha==rhs,G-margin*np.eye(18)>>0]
    problem=cp.Problem(cp.Maximize(margin),constraints)
    tick=time.perf_counter()
    problem.solve(solver='CLARABEL',tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9,max_iter=250)
    out={'scope':'one endpoint, one facially reduced cubic-form18x18 Gram proposal; not all angular forms',
         'status':problem.status,'margin':None if margin.value is None else float(margin.value),
         'gram':None if G.value is None else G.value.tolist(),
         'alpha':None if alpha.value is None else alpha.value.tolist(),
         'feature_reduction':[[str(v) for v in row] for row in B.tolist()],
         'alpha_labels':alpha_labels,'coefficient_equations':len(keys),
         'mapping_seconds':mapping_seconds,'solve_seconds':time.perf_counter()-tick,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'cvxpy_version':cp.__version__,'random_starts':0}
    Path(__file__).with_name('ENDPOINT_HEAT_PROPOSAL.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','margin','coefficient_equations','mapping_seconds','solve_seconds')},indent=2))


if __name__=='__main__':main()
