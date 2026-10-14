"""Independent small-system audits; exact rational arithmetic except final PSD spot diagnostics.
No dense expansion is used by the large-state solvers or their certificates.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json, math, random, time, sys
import numpy as np
import sympy as sp
from jacobi_gate import local_basis
sys.set_int_max_str_digits(0)
BASE=Path(__file__).resolve().parent
checks=0

def check(b):
    global checks
    assert b
    checks+=1

def audit_continuum(prefix='audit_continuum3'):
    p=BASE/prefix;meta=json.loads(p.with_suffix('.json').read_text())
    it=iter(map(int,p.with_suffix('.continuum.txt').read_text().split()))
    n,d,D,G=[next(it) for _ in range(4)]
    gram=[F(next(it),G) for _ in range(d)]
    Ws=[]
    for _ in range(n):Ws.append(np.array([F(next(it),D) for _ in range(9*d*d)],object).reshape(3,3,d,d))
    # W above has shared numerator D only once per MPO path, not at every site.
    cores=[];exponents=[]
    for i in range(n):
        l,r,ex=[next(it) for _ in range(3)];exponents.append(ex)
        cores.append(np.array([F(next(it),2**ex) for _ in range(l*d*r)],object).reshape(l,d,r))
    try:next(it);raise AssertionError('extra file payload')
    except StopIteration:pass
    indices=list(product(range(d),repeat=n))
    v=[]
    for ind in indices:
        row=np.array([[F(1)]],object)
        for a,j in zip(cores,ind):row=row@a[:,j,:]
        v.append(row[0,0])
    v=np.array(v,object)
    q=F(meta['q']);rho=F(meta['rho']);eps=F(meta['eps']);k=q*rho
    basis=local_basis(q,rho,d-1);X=basis['X'];h=np.diag(basis['lambda']);I=np.eye(d,dtype=int).astype(object)
    def kron(ms):
        out=np.array([[F(1)]],object)
        for m in ms:out=np.kron(out,m)
        return out
    H=k*eps*np.eye(d**n,dtype=int).astype(object)
    for i in range(n):
        terms=[I]*n;terms[i]=h
        if i==0:H+=kron(terms)
        else:
            terms[i-1]=eps*I+(1-eps)*X;H+=kron(terms)
    terms=[I]*n;terms[-1]=X;H+=k*(1-eps)*kron(terms)
    w=np.array([math.prod(gram[j] for j in ind) for ind in indices],object)
    y=H@v
    raw={key:int(val) for key,val in (line.split() for line in p.with_suffix('.continuum_raw.txt').read_text().splitlines())}
    S=2**sum(exponents);GN=G**n
    check(v[0]==F(raw['source'],S));check(y[0]==F(raw['Hsource'],D*S))
    check(sum(w*v*y)==F(raw['energy'],D*S*S*GN))
    check(sum(w*y*y)==F(raw['Hnorm'],D*D*S*S*GN))
    for cap in range(1,d-1):
        name='Hnorm_low' if cap==1 else 'Hnorm_cap'+str(cap)
        check(sum(wi*yi*yi for wi,yi,ind in zip(w,y,indices) if max(ind)<=cap)==F(raw[name],D*D*S*S*GN))
    for j in range(3):
        check(sum(wi*yi*yi for wi,yi,ind in zip(w,y,indices) if max(ind)<=1 and sum(ind)==j)==F(raw['sector'+str(j)],D*D*S*S*GN))
    for i in range(len(indices)):
        for j in range(len(indices)):
            check(w[i]*H[i,j]==w[j]*H[j,i])
    # Local polynomials solve the actual Jacobi differential eigenproblem.
    x=sp.symbols('x');alpha=q*rho
    for j,coeff in enumerate(basis['polys']):
        poly=sum(sp.Rational(c.numerator,c.denominator)*x**i for i,c in enumerate(coeff))
        Lj=x*(1-x)*sp.diff(poly,x,2)+(sp.Rational(alpha.numerator,alpha.denominator)-sp.Rational(rho.numerator,rho.denominator)*x)*sp.diff(poly,x)
        check(sp.expand(Lj+sp.Rational(basis['lambda'][j])*poly)==0)
    return {'coefficient_dimension':d**n,'checks_after_continuum':checks,'maximum_trial_degree':meta['degree'],'actual_residual_degree':meta['degree']+1}

def psd(M):
    # All principal minors, necessary/sufficient for a real symmetric finite matrix.
    from itertools import combinations
    check(M==M.T)
    for k in range(1,M.rows+1):
        for ids in combinations(range(M.rows),k):check(M.extract(ids,ids).det()>=0)

def audit_source_matrices():
    rng=random.Random(1649)
    for k in range(12):
        d=3 if k<6 else 4
        Z=sp.Matrix(d,d,lambda i,j:rng.randint(-2,2));Y=sp.Matrix(d,d,lambda i,j:rng.randint(-2,2))
        C=Z.T*Z+sp.eye(d);H=C+Y.T*Y
        B=sp.Matrix(d,2,lambda i,j:rng.randint(-3,3));V=sp.Matrix(d,2,lambda i,j:sp.Rational(rng.randint(-3,3),7))
        R=B-H*V;G=B.T*H.inv()*B;G0=B.T*V+V.T*B-V.T*H*V;Gamma=R.T*C.inv()*R
        E=G-G0
        check(E==R.T*H.inv()*R);psd(E);psd(Gamma-E)
        # Two-load cross-response range; avoid irrational square roots by squaring.
        check((2*E[0,1]-Gamma[0,1])**2<=Gamma[0,0]*Gamma[1,1])
        # Source-aware Schur equality, including hidden gamma.
        O=[0];J=list(range(1,d));K=H.extract(O,O)-H.extract(O,J)*H.extract(J,J).inv()*H.extract(J,O)
        m=sp.ones(d,1);mo=m.extract(O,[0]);mh=m.extract(J,[0]);Ah=H.extract(J,J)
        b=mo-H.extract(O,J)*Ah.inv()*mh;gamma=(mh.T*Ah.inv()*mh)[0]
        check((m.T*H.inv()*m)[0]==gamma+(b.T*K.inv()*b)[0])
        # A relative form perturbation bounds the response even if dense/nonlocal.
        eta=sp.Rational(1,10);T=H+eta*Y.T*Y
        lo=(m.T*H.inv()*m)[0]/(1+eta);hi=(m.T*H.inv()*m)[0]/(1-eta)
        check(lo<=(m.T*T.inv()*m)[0]<=hi)
    return {'matrix_instances':12,'loads_per_instance':2}

if __name__=='__main__':
    t=time.perf_counter();a=audit_continuum();b=audit_source_matrices();out={'passed':True,'exact_assertions':checks,'continuum':a,'source_matrix':b,'seconds':time.perf_counter()-t,'scope':'small algebra/implementation audit, not external review or a convergence guarantee'}
    (BASE/'audit_exact_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
