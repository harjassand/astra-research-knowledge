"""Exact algebra fixture. Run with Python + SymPy; no randomness or solver oracle."""
import sympy as S
import json, pathlib
D,K=3,2

def ptr(X):
    return S.Matrix(D,D,lambda a,b: sum(X[o*D+a,o*D+b] for o in range(K)))
def vec(M):
    return S.Matrix([M[o,i] for o in range(M.rows) for i in range(M.cols)])
def hs(A,B):
    return S.simplify(S.trace(A.conjugate().T*B))
def z(M):
    return all(S.simplify(x)==0 for x in M)
def outer(v): return v*v.conjugate().T
R0=S.Matrix([[1,0,0],[0,1,0]])
R1=S.Matrix([[0,0,0],[0,0,1]])
r0,r1=vec(R0),vec(R1)
C=outer(r0)+outer(r1)
v0,v1=r0/S.sqrt(2),r1
P=outer(v0)+outer(v1)
basis=[outer(v0),outer(v1),(v0*v1.T+v1*v0.T)/S.sqrt(2),S.I*(v0*v1.T-v1*v0.T)/S.sqrt(2)]
Gram=S.Matrix(4,4,lambda a,b:hs(ptr(basis[a]),ptr(basis[b])))
assert Gram==S.diag(S.Rational(1,2),1,S.Rational(1,2),S.Rational(1,2))
assert ptr(C)==S.eye(3)
assert z(C*P-C)
rows=[]
for s in [S.Rational(1,5),S.Rational(3,5),S.Rational(4,5),S.Rational(12,13)]:
    p=1-s*s
    E0=S.Matrix([[1,0],[0,s],[0,0]])
    E1=S.Matrix([[0,0],[0,0],[0,S.sqrt(p)]])
    assert E0.T*E0+E1.T*E1==S.eye(2)
    H=sum((outer(vec(E.T)) for E in [E0,E1]),S.zeros(6))
    Y=S.diag(1+s,s*(1+s),p)
    Q=S.kronecker_product(S.eye(2),Y)-H
    mu=min(2*s,s*(1+s),1+s,p)
    assert z(Q*C)
    assert all(x>=0 for x in (Q-mu*(S.eye(6)-P)).eigenvals())
    assert sorted(Q.eigenvals().items(),key=lambda a:float(a[0]))
    Fe=hs(H,C)/4
    assert Fe==(1+s)/2
    assert S.trace(Y)==hs(H,C)
    # Independently compute Kraus entanglement fidelity.
    FeK=sum(abs(S.trace(R*E))**2 for R in [R0,R1] for E in [E0,E1])/4
    assert S.simplify(FeK-Fe)==0
    # Exact PSD/TP competitors: replacement channels and rotated receiver.
    swap=S.Matrix([[0,1,0],[1,0,0],[0,0,1]])
    V=S.kronecker_product(S.eye(2),swap)
    competitors=[S.kronecker_product(S.diag(1,0),S.eye(3)),S.kronecker_product(S.diag(0,1),S.eye(3)), V*C*V.T]
    for other in competitors:
      for alpha in [S.Rational(1,7),S.Rational(1,2),S.Integer(1)]:
        X=(1-alpha)*C+alpha*other
        assert ptr(X)==S.eye(3)
        t=hs(S.eye(6)-P,X)
        Z=X-P*X*P
        dist=hs(X-C,X-C)
        assert hs(Z,Z)<=2*3*t-t*t
        assert dist<=5*(6*t-t*t)
        assert hs(H,C-X)>=mu*dist/30
    rows.append({'s':str(s),'p':str(p),'mu':str(mu),'Fe':str(Fe),'Q_eigenvalues':{str(a):b for a,b in Q.eigenvals().items()}})
# Exact TP normalization on a deliberately non-TP rank-2 PSD proposal.
L=S.kronecker_product(S.eye(2),S.diag(2,3,4))
Cr=L*C*L
M=ptr(Cr)
T=S.kronecker_product(S.eye(2),S.diag(S.Rational(1,2),S.Rational(1,3),S.Rational(1,4)))
assert T*Cr*T==C
assert M==S.diag(4,9,16)
# Physical unknown orientation fixture: rational orthogonal non-Pauli qutrit rotation.
U=S.Matrix([[S.Rational(3,5),0,-S.Rational(4,5)],[0,1,0],[S.Rational(4,5),0,S.Rational(3,5)]])
assert U.T*U==S.eye(3)
W=S.kronecker_product(S.eye(2),U) # vec(R U.T) = (I tensor U) vec(R)
Cu=W*C*W.T
Hu=W*H*W.T
Yu=U*Y*U.T
Qu=S.kronecker_product(S.eye(2),Yu)-Hu
assert ptr(Cu)==S.eye(3)
assert z(Qu*Cu)
assert hs(Hu,Cu)==hs(H,C)
Hu_native=sum((outer(vec((U*E).T)) for E in [E0,E1]),S.zeros(6))
assert Hu_native==Hu
# Complex Choi convention and exact input dual-frame reconstruction.
Uc=S.diag(1,S.I,(3+4*S.I)/5)*U
assert z(Uc.conjugate().T*Uc-S.eye(3))
Ec=[Uc*E for E in [E0,E1]]
J=sum((outer(vec(E)) for E in Ec),S.zeros(6))
Hc=sum((outer(vec(E.conjugate().T)) for E in Ec),S.zeros(6))
Swap=S.zeros(6)
for o in range(3):
 for i in range(2): Swap[i*3+o,o*2+i]=1
assert z(Hc-Swap*J.T*Swap.T)
Rc=[R*Uc.conjugate().T for R in [R0,R1]]
Cc=sum((outer(vec(R)) for R in Rc),S.zeros(6))
assert z(ptr(Cc)-S.eye(3))
assert S.simplify(hs(Hc,Cc)/4-Fe)==0
states=[S.diag(1,0),S.diag(0,1),outer(S.Matrix([1,1]))/2,outer(S.Matrix([1,S.I]))/2]
GG=S.Matrix(4,4,lambda a,b:hs(states[a],states[b]))
dual=[sum((GG.inv()[a,b]*states[b] for b in range(4)),S.zeros(2)) for a in range(4)]
for a in range(4):
 for b in range(4): assert hs(dual[a],states[b])==int(a==b)
Jrec=sum((S.kronecker_product(sum((E*rho*E.conjugate().T for E in Ec),S.zeros(3)),dj.T) for rho,dj in zip(states,dual)),S.zeros(6))
assert z(J-Jrec)
out={'status':'exact symbolic fixture passed; not independent review','support_TP_Gram':str(Gram),'G':30,'fixtures':rows,'tested_competitor_mixtures':36,'normalization_fixture':'passed','unknown_orientation_fixture':'passed','complex_Choi_and_IC_dual_reconstruction':'passed'}
path=pathlib.Path(__file__).with_suffix('.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
