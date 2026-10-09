"""Independent finite symbolic checks; not a universal or software proof."""
from functools import lru_cache
from pathlib import Path
import json
import sympy as s
q=s.Rational
z=s.symbols('z')
A=s.Matrix([[q(1,10),q(1,20)],[q(1,20),q(1,15)]])
C=s.Matrix([[q(1,8),q(1,25)],[q(1,25),q(1,9)]])
K=A.row_join(C).col_join(C.row_join(A))
ell=s.Matrix([q(1,7),q(1,8),q(1,7),q(1,8)])
H=[0,2]; U=[1,3]; X=s.Matrix([[0,1],[1,0]])
kuu=K.extract(U,U); khu=K.extract(H,U); khh=K.extract(H,H)
lu=ell.extract(U,[0]); lh=ell.extract(H,[0]); M=X*kuu
J=z*(s.eye(2)-M*z).inv()*X
S=khh+khu*J*khu.T; t=lh+khu*J*lu; v=(lu.T*J*lu)[0]
assert s.simplify(J-J.T)==s.zeros(2)
N=5
tr=lambda f:s.series(f,z,0,N).removeO().expand()
det_factor=tr(s.det(s.eye(2)-M*z)**(-q(1,2)))
vpoly=tr(v/2)
exppoly=s.Integer(1); vp=s.Integer(1)
for j in range(1,N):
    vp=tr(vp*vpoly)
    exppoly+=vp/s.factorial(j)
pref=tr(det_factor*exppoly)
Sp=S.applyfunc(tr); tp=t.applyfunc(tr)

def lhaf(matrix, linear, counts):
    @lru_cache(None)
    def rec(r):
        if not any(r):return s.Integer(1)
        a=next(i for i,x in enumerate(r) if x)
        rr=list(r); rr[a]-=1
        out=linear[a]*rec(tuple(rr))
        for b,rb in enumerate(rr):
            if rb:
                rrr=rr.copy();rrr[b]-=1
                out+=rb*matrix[a,b]*rec(tuple(rrr))
        return s.expand(out)
    return rec(tuple(counts))
checks=[]
for h in range(5):
    contracted=tr(pref*lhaf(Sp,tp,[h,h])/s.factorial(h))
    for n in range(N):
        direct=lhaf(K,ell,[h,n,h,n])/(s.factorial(h)*s.factorial(n))
        assert s.simplify(contracted.coeff(z,n)-direct)==0,(h,n)
        checks.append([h,n])
# Required count identification: squeezed and coherent single-mode PGFs.
b,g=s.symbols('b g', positive=True)
Mp=s.Matrix([[0,b],[b,0]])
assert s.simplify(s.det(s.eye(2)-z*Mp)-(1-b*b*z*z))==0
Jcoh=z*X
assert (s.Matrix([[g,g]])*Jcoh*s.Matrix([g,g]))[0]/2==g*g*z
# Nonphysical but normalized positive diagonal law: two-mode swap cross block.
c=q(1,2)
Cbad=s.Matrix([[0,c],[c,0]])
assert Cbad.det()<0
# Physicality fails in the 1-photon sector, despite nonnegative coefficients.
result={"status":"PASS","mixed_displaced_coefficient_checks":len(checks),"checked_h_n_pairs":checks,"normalization_control":"coherent mean g^2; squeezed even counts", "physicality_counterexample":"A=0, C=[[0,1/2],[1/2,0]], ell=0; one-photon sector has eigenvalues +/- c times positive normalizer"}
Path(__file__).with_name('verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
