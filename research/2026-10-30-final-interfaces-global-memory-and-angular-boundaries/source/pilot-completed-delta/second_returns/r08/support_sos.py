"""Acquire an SOS support at an acoustic base, using local NumPy only.

Numerics propose free Gram entries. All polynomial coefficients and the
subsequent affine correction live in Q[t]/(t^4-Ct^2+1). Exact positivity
is checked separately by rational interval LDL, not optimizer status.
"""
from pathlib import Path
from fractions import Fraction
import json,time
import numpy as np
import sympy as s

OUT=Path(__file__).resolve().parent
FIRST=OUT.parent
a,b,c,d,t,z,v1,v2,v3=s.symbols('a b c d t z v1 v2 v3')
av=(a,b,c,d);vv=(z,v1,v2,v3)
mod=s.Poly(t**4-s.Rational(83981,2710)*t*t+1,t)
def rem(v):return s.rem(s.expand(v),mod.as_expr(),t)
data=json.loads((FIRST/'corrugation_data.json').read_text())
K=s.Matrix([s.sympify(v,locals={'t':t}) for v in data['base_K_mod_m']])
R=s.Matrix([1,t,0,0])
T=sum(w*w for w in av);q=a*d-b*c;X=a*a+c*c-b*b-d*d
F=T*T+s.Rational(3132,301)*q*q+s.Rational(1196,301)*q*X
HK=s.hessian(F,av).subs(dict(zip(av,K)),simultaneous=True)
lam=rem(2*(HK*R)[3])
P=(HK-lam*s.hessian(q,av)/2).applyfunc(rem)
assert all(rem(v)==0 for v in P*R)
H=s.Matrix([z,t*z+v1,v2,v3])
J=s.expand(F.subs(dict(zip(av,K+H)),simultaneous=True)
           -F.subs(dict(zip(av,K)),simultaneous=True)
           -sum(s.diff(F,w).subs(dict(zip(av,K)),simultaneous=True)*h for w,h in zip(av,H))
           -lam*q.subs(dict(zip(av,H)),simultaneous=True)/2)
# P = Hess F - lam*(Hess det)/2, so the support determinant coefficient
# is lam/2, rather than lam. The convention is checked explicitly below.
J=s.Poly(J,*vv)
J=s.Poly(sum(rem(co)*s.prod(w**e for w,e in zip(vv,ee)) for ee,co in J.terms()),*vv)
assert all(sum(ee)>=2 for ee,co in J.terms())
assert all(J.coeff_monomial(z**j*s.prod(w**e for w,e in zip((v1,v2,v3),pw)))==0
           for j,pw in [(3,(0,0,0)),(2,(1,0,0)),(2,(0,1,0)),(2,(0,0,1))])

def degree_powers(degree):
    return [(i,j,k,degree-i-j-k) for i in range(degree+1)
            for j in range(degree+1-i) for k in range(degree+1-i-j)]
quadpowers=degree_powers(2)
featurepowers=[(0,1,0,0),(0,0,1,0),(0,0,0,1)]+quadpowers
monpowers=degree_powers(2)+degree_powers(3)+degree_powers(4)
position={p:i for i,p in enumerate(monpowers)}
entries=[(i,j) for i in range(13) for j in range(i,13)]
Araw=np.zeros((len(monpowers),len(entries)))
for col,(i,j) in enumerate(entries):
    power=tuple(u+v for u,v in zip(featurepowers[i],featurepowers[j]))
    Araw[position[power],col]=1 if i==j else 2
active=np.nonzero(np.max(np.abs(Araw),axis=1)>0)[0]
for row in set(range(len(monpowers)))-set(active):
    assert J.coeff_monomial(s.prod(w**e for w,e in zip(vv,monpowers[row])))==0
Araw=Araw[active]
targetbase=[J.coeff_monomial(s.prod(w**e for w,e in zip(vv,monpowers[row]))) for row in active]
T4=s.Poly(s.expand((H.dot(H))**2),*vv)
T4co=[T4.coeff_monomial(s.prod(w**e for w,e in zip(vv,monpowers[row]))) for row in active]
C=-mod.nth(2);root=s.sqrt((C-s.sqrt(C*C-4))/2)
rootfloat=float(root.evalf(18))

def acquire(margin=s.Rational(1,64),iterations=30000):
    target=[rem(co-margin*tc) for co,tc in zip(targetbase,T4co)]
    bb=np.array([float(co.subs(t,rootfloat)) for co in target])
    weights=np.array([1 if i==j else np.sqrt(2.) for i,j in entries])
    Am=Araw/weights
    projector=Am.T@np.linalg.inv(Am@Am.T)
    def affine(xx):return xx+projector@(bb-Am@xx)
    def matrix(xx):
        mm=np.zeros((13,13))
        for w,(i,j) in zip(xx/weights,entries):mm[i,j]=mm[j,i]=w
        return mm
    def vector(mm):return np.array([mm[i,j] for i,j in entries])*weights
    def psd(xx):
        eig,V=np.linalg.eigh(matrix(xx))
        return vector((V*np.maximum(eig,1e-7))@V.T)
    xx=affine(np.zeros(len(entries)))
    started=time.perf_counter()
    best=None
    for it in range(iterations):
        yy=psd(xx);zz=affine(2*yy-xx);xx+=zz-yy
        if it%250==0:
            candidate=affine(yy)
            mineig=float(np.linalg.eigvalsh(matrix(candidate))[0])
            if best is None or mineig>best[0]:best=(mineig,candidate.copy(),it)
            if it%2500==0:print('iter',it,'min_eig',mineig,'seconds',time.perf_counter()-started,flush=True)
            if mineig>1e-6:break
    print('best',best[0],best[2],flush=True)
    if best[0]<=0:
        return {'margin':str(margin),'feasible':False,'best_min_eigenvalue':best[0]}
    proposal=best[1]/weights
    # Each Gram entry contributes to exactly one monomial coefficient.
    # Keep all but one entry per row as rounded free rationals; enforce
    # every coefficient equation exactly by the remaining pivot entry.
    exact=[s.Rational(round(float(w)*(2**32)),2**32) for w in proposal]
    pivots=[]
    for row,co in enumerate(target):
        occupied=np.nonzero(Araw[row])[0]
        pivot=int(occupied[np.argmax(np.abs(proposal[occupied]))])
        pivots.append(pivot)
        other=sum(s.Integer(int(Araw[row,col]))*exact[col] for col in occupied if col!=pivot)
        exact[pivot]=rem((co-other)/s.Integer(int(Araw[row,pivot])))
    assert all(rem(sum(s.Integer(int(Araw[row,col]))*exact[col]
                        for col in np.nonzero(Araw[row])[0])-co)==0
               for row,co in enumerate(target))
    record={'margin':str(margin),'modulus':str(mod.as_expr()),
        'positive_small_root':str(root),'base_K':list(map(str,K)),
        'support_det_coefficient':str(lam/2),
        'coordinates_H':['z','t*z+v1','v2','v3'],
        'feature_powers':featurepowers,'gram_entries':
            [[i,j,str(value)] for (i,j),value in zip(entries,exact)],
        'pivot_columns':pivots,
        'active_monomial_powers':[monpowers[row] for row in active],
        'polynomial_identity_exact':True,
        'numerical_proposal_min_eigenvalue':best[0],
        'scope':'Exact polynomial identity only until rational-interval positive-definiteness replay succeeds.'}
    (OUT/'support_gram.json').write_text(json.dumps(record,indent=2)+'\n')
    return {'margin':str(margin),'feasible':True,'best_min_eigenvalue':best[0]}

if __name__=='__main__':print(json.dumps(acquire(),indent=2))
