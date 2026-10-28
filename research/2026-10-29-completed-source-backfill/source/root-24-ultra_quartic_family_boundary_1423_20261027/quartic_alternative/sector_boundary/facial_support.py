"""Spin-decomposed exact face, followed by an ordinary numerical SDP.

No PC assertion before exact reconstruction. Only the accepted boundary
relations and literal polynomial algebra define the face.
"""
from pathlib import Path
from itertools import combinations_with_replacement as cwr
import json,pickle,time
import sympy as s
from sympy.polys.matrices import DomainMatrix
import numpy as np
import cvxpy as cp

ROOT=Path(__file__).resolve().parent


def build():
    root=s.sqrt(42);tau=89-12*root;field=s.QQ.algebraic_field(root)
    a=s.symbols('a0:4',real=True);x=s.symbols('x0:4',real=True);variables=a+x
    ac=[a[0]+s.I*a[2],a[1]+s.I*a[3]]
    xc=[x[0]+s.I*x[2],x[1]+s.I*x[3]]
    def rephase(e,k):return s.expand_complex(s.I**k*e).expand()
    spin1=[rephase(ac[i]*xc[j]*s.conjugate(xc[k]),i+j+k)
           for i in range(2) for j in range(2) for k in range(2)]
    spin1 += [rephase(s.conjugate(ac[i])*xc[j]*xc[k],i+j+k)
              for i in range(2) for j,k in cwr(range(2),2)]
    spin1 += [rephase(xc[i]*xc[j]*s.conjugate(xc[k]),i+j+k)
              for i,j in cwr(range(2),2) for k in range(2)]
    spin3=[rephase(ac[i]*xc[j]*xc[k],i+j+k)
           for i in range(2) for j,k in cwr(range(2),2)]
    spin3 += [rephase(xc[i]*xc[j]*xc[k],i+j+k) for i,j,k in cwr(range(2),3)]
    z=s.symbols('z');critical=json.loads((ROOT/'CRITICAL_SELECTOR.json').read_text())
    A=[s.sympify(e,locals={'z':z}) for e in critical['kernel_vector']]
    mc=-s.Rational(39,58)+s.Rational(15,29)*root
    modulus=s.Poly(z**4-mc*z*z+1,z,domain=field)
    def reduce(e):return s.Poly(s.expand(e),z,domain=field).rem(modulus)
    substitution=dict(zip(a,A));substitution.update(dict(zip(x,[1,z,0,0])))
    bases=[];features=[];kernel_ranks=[]
    for block,axcount in [(spin1,14),(spin3,6)]:
        real=[s.re(e).expand() for e in block];imag=[s.im(e).expand() for e in block]
        kernel=[]
        for parts in [real,imag]:
            polynomials=[reduce(e.subs(substitution)) if j<axcount else s.Poly(0,z,domain=field)
                         for j,e in enumerate(parts)]
            kernel += [[p.nth(k) for p in polynomials] for k in range(4)]
        K=DomainMatrix.from_Matrix(s.Matrix(kernel)).convert_to(field)
        V=K.nullspace(divide_last=True).to_Matrix().T
        assert K.matmul(DomainMatrix.from_Matrix(V).convert_to(field)).is_zero_matrix
        kernel_ranks.append(len(block)-V.cols);bases.append(V)
        features.append(([s.expand(sum(V[i,j]*real[i] for i in range(len(block)))) for j in range(V.cols)],
                         [s.expand(sum(V[i,j]*imag[i] for i in range(len(block)))) for j in range(V.cols)]))
    def inv(v):
        aa,b,c,d=v
        return aa*aa+c*c,b*b+d*d,aa*b+c*d,aa*d-b*c
    def energy(v):
        u,vv,w,q=inv(v);return u*u+vv*vv+3*w*w+tau*q*q+4*q*(u-vv)
    f=energy(a);u,v,w,q=inv(a);qx=inv(x)[3];norm=sum(e*e for e in x)
    R=-s.Rational(3,2)+root/3;K0=162-21*root
    target=s.Poly(norm*(energy(tuple(ai+xi for ai,xi in zip(a,x)))-f-
                       sum(s.diff(f,ai)*xi for ai,xi in zip(a,x))-K0*q*qx),variables)
    alpha_term=s.Poly(norm*((u-v)-R*q)*qx,variables)
    terms=[]
    for block,(real,imag) in enumerate(features):
        for i in range(len(real)):
            for j in range(i,len(real)):
                terms.append((block,i,j,s.Poly(s.expand(real[i]*real[j]+imag[i]*imag[j]),variables)))
    monoms=sorted(set(target.monoms()).union(alpha_term.monoms(),*(set(p.monoms()) for _,_,_,p in terms)))
    M=s.zeros(len(monoms),len(terms)+1);b=s.zeros(len(monoms),1);lookup={e:i for i,e in enumerate(monoms)}
    for col,(block,i,j,p) in enumerate(terms):
        for e,c in p.terms():M[lookup[e],col]=s.expand(c*(1 if i==j else 2))
    for e,c in alpha_term.terms():M[lookup[e],len(terms)]=c
    for e,c in target.terms():b[lookup[e],0]=c
    nonzero=[i for i in range(M.rows) if any(M[i,j]!=0 for j in range(M.cols))]
    assert all(b[i,0]==0 for i in range(M.rows) if i not in nonzero)
    M=M[nonzero,:];b=b[nonzero,:];monoms=[monoms[i] for i in nonzero]
    return M,b,terms,bases,kernel_ranks,monoms


def main():
    start=time.monotonic()
    cache=ROOT/'FACE_MAP.pkl'
    if cache.exists():M,b,terms,bases,ranks,monoms=pickle.loads(cache.read_bytes())
    else:M,b,terms,bases,ranks,monoms=build()
    build_seconds=time.monotonic()-start
    with (ROOT/'FACE_MAP.pkl').open('wb') as f:pickle.dump((M,b,terms,bases,ranks,monoms),f)
    mf=np.array(M,float);bf=np.array(b,float).ravel();v=cp.Variable(M.cols);rho=cp.Variable()
    constraints=[];blocks=[]
    for k,V in enumerate(bases):
        n=V.cols;rows=[]
        lookup={(i,j):col for col,(kk,i,j,p) in enumerate(terms) if kk==k}
        for i in range(n):rows.append(cp.hstack([v[lookup[min(i,j),max(i,j)]] for j in range(n)]))
        Q=cp.vstack(rows);blocks.append(Q);constraints.append(Q-rho*np.eye(n)>>0)
    weights=np.linalg.norm(mf,axis=1);assert np.all(weights>0)
    U,sigma,Vt=np.linalg.svd(mf/weights[:,None],full_matrices=False)
    rank=int(np.sum(sigma>1e-9))
    rhs=(U[:,:rank].T@(bf/weights))/sigma[:rank]
    constraints.append(Vt[:rank]@v==rhs)
    problem=cp.Problem(cp.Maximize(rho),constraints)
    problem.solve(solver='CLARABEL',max_iter=180,tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-10)
    root=np.sqrt(42);alpha=None if v.value is None else float(v.value[-1])
    out={'status':'NUMERICAL_FACE_ONLY','tau':'89-12sqrt42','kernel_ranks':ranks,
         'reduced_blocks':[V.cols for V in bases],'variables':M.cols,'equations':M.rows,
         'numerical_affine_rank':rank,
         'solver_status':problem.status,'margin':None if rho.value is None else float(rho.value),
         'alpha':alpha,'delta':None if alpha is None else 162-21*root-alpha*(-1.5+root/3),
         'residual':None if v.value is None else float(np.max(np.abs(mf@v.value-bf))),
         'build_seconds':build_seconds,'total_seconds':time.monotonic()-start,
         'blocks':[None if Q.value is None else Q.value.tolist() for Q in blocks],
         'bases':[[[str(e) for e in row] for row in V.tolist()] for V in bases]}
    (ROOT/'FACIAL_SUPPORT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['blocks','bases']},indent=2))


if __name__=='__main__':main()
