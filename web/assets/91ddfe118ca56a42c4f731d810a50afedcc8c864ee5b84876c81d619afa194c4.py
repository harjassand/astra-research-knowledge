"""Finite evidence for independently written bounds; no proof certification."""
from fractions import Fraction as F
from pathlib import Path
import json, math
import numpy as np
import sympy as sp
out=Path(__file__).resolve().parent
rng=np.random.default_rng(172904)
counts={}
# Exact covariance counterexample family: TMSV occupation n=1, retained q-squeeze s,
# herald q-displacement s; p(vacuum herald)=exp(-s^2/4)/2.
family=[]
for s in range(2,21):
    a=F(s*s)
    E=F(5,4)*a+F(3,4)/a+F(1,2)
    Evac=F(1,4)*a*a+F(1,4)*(a+1/a-2)
    assert Evac <= E*E+3*E
    family.append({'s':s,'E':str(E),'E_vac':str(Evac),'E_vac_over_E':float(Evac/E),'E_vac_over_E_squared':float(Evac/(E*E))})
counts['exact_quadratic_counterexample_family']=len(family)
# Exact positive-kernel vacuum-energy tests. A=a J/m,C=c I commute;
# normal mode inequalities a,c>=0,a+c<1 ensure physical squeezed-thermal input.
for trial in range(100):
    m=int(rng.integers(2,6)); a=sp.Rational(int(rng.integers(1,8)),20)
    c=sp.Rational(int(rng.integers(0,7)),20)
    A=a*sp.ones(m)/m; C=c*sp.eye(m)
    M=C.row_join(A).col_join(A.row_join(C))
    ell=sp.Matrix([sp.Rational(int(rng.integers(0,7)),11) for _ in range(m)]*2)
    def energy(W,g):
        R=(sp.eye(W.rows)-W).inv()
        return sp.trace(W*R)/2+(g.T*R*R*g)[0]/2
    E=energy(M,ell)
    keep=list(range(1,m))+list(range(m+1,2*m))
    Evac=energy(M.extract(keep,keep),ell.extract(keep,[0]))
    assert Evac<=E
counts['exact_positive_vacuum_energy_fixtures']=100
# Numerically check universal Schur/energy bound on physically constructed Gaussian states.
max_ratio=0
for trial in range(400):
    m=int(rng.integers(2,7)); h=int(rng.integers(1,m))
    # q1..qm,p1..pm ordering, orthogonal passive mix, local squeezes, Williamson temperatures.
    Q,_=np.linalg.qr(rng.normal(size=(m,m)))
    P=np.block([[Q,np.zeros((m,m))],[np.zeros((m,m)),Q]])
    ss=np.exp(rng.uniform(-1.8,1.8,m)); S=np.diag(np.r_[ss,1/ss])
    nu=.5+rng.exponential(.5,m)
    V=P@S@np.diag(np.r_[nu,nu])@S@P.T
    d=rng.normal(size=2*m)*rng.uniform(.1,2)
    Ec=(np.trace(V)-m)/2; Ed=float(d@d)/2; E=Ec+Ed
    H=list(range(h))+list(range(m,m+h)); R=list(range(h,m))+list(range(m+h,2*m))
    VR=V[np.ix_(R,R)]; VH=V[np.ix_(H,H)]; X=V[np.ix_(R,H)]
    B=X@np.linalg.inv(VH+.5*np.eye(2*h))
    V0=VR-B@X.T; d0=d[R]-B@d[H]
    E0=(np.trace(V0)+d0@d0-(m-h))/2
    assert np.linalg.eigvalsh(V).max() <=2*Ec+1+1e-9
    assert np.linalg.norm(B,2)**2<=4*Ec+2+1e-8
    assert E0<=Ec+(4*Ec+3)*Ed+1e-8
    assert E0<=E*E+3*E+1e-8
    max_ratio=max(max_ratio,float(E0/(E*E+3*E)))
counts['numerical_universal_covariance_fixtures']=400
# Evaluate quadratic N' on complete Fock-support blocks in one and two modes.
# u,v canonical rational pairs. This tests the dimension-free operator bound;
# it is finite floating-point evidence, not a verification of the general lemma.
for m in [1,2]:
    for h in range(9):
        uv=[(1.25,.75)]*m; al=np.array([.3,-.4][:m]); es=sum(v*v for u,v in uv); ed=float(al@al); e=es+ed
        basis=[(i,) for i in range(h+3)] if m==1 else [(i,j) for i in range(h+3) for j in range(h+3-i)]
        idx={n:i for i,n in enumerate(basis)}; Aops=[]
        for k in range(m):
            a=np.zeros((len(basis),len(basis)))
            for n,j in idx.items():
                if n[k]:
                    t=list(n);t[k]-=1;a[idx[tuple(t)],j]=math.sqrt(n[k])
            Aops.append(a)
        Nprime=np.zeros((len(basis),len(basis)))
        # normal ordered form avoids top-boundary artifacts from b^dagger b.
        for k,(u,v) in enumerate(uv):
            a=Aops[k];ad=a.T;alpha=al[k]
            Nprime+=(u*u+v*v)*(ad@a)+u*v*(ad@ad+a@a)+(u+v)*alpha*(ad+a)
        Nprime+=e*np.eye(len(basis))
        cols=[idx[n] for n in basis if sum(n)<=h]
        operator_norm=np.linalg.norm(Nprime[:,cols],2)
        assert operator_norm <=4*h+3+(6*h+5)*e+1e-9
counts['numerical_quadratic_ladder_blocks']=18
out.joinpath('check_bounds.json').write_text(json.dumps({'status':'finite_scoped_checks_passed','counts':counts,'maximum_universal_covariance_ratio':max_ratio,'quadratic_counterexample_family':family,'warning':'No finite check is a proof or formal certification.'},indent=2)+'\n')
print(json.dumps(counts,sort_keys=True))
