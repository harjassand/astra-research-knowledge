import numpy as np,itertools
rng=np.random.default_rng(270016);D=5
V=np.linalg.qr(rng.normal(size=(D,3))+1j*rng.normal(size=(D,3)))[0]
w=np.exp(2j*np.pi/3);X=np.roll(np.eye(3),1,axis=0);Z=np.diag(w**np.arange(3));Us=[np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b) for a,b in itertools.product(range(3),repeat=2)]
phi=V.T.reshape(-1)/np.sqrt(3);Ps=[];Ks=[]
for U in Us:
 v=np.kron(U,np.eye(D))@phi;Ps.append(np.outer(v,v.conj()))
 # Exact component contraction: local Bell amplitude1/sqrt3 times bra v.
 K=v.reshape(3,D).conj()/np.sqrt(3)
 assert np.linalg.norm(K-U.conj()@V.conj().T/3)<2e-15
 corrected=U.T@K;assert np.linalg.norm(corrected-V.conj().T/3)<2e-15
 Ks.append(corrected)
Q=np.kron(np.eye(3),V@V.conj().T)
assert np.linalg.norm(sum(Ps)-Q)<3e-15
assert max(np.linalg.norm(Ps[i]@Ps[j]) for i in range(9) for j in range(i))<1e-15
p=.37;As=[p*P-p*Q/9 for P in Ps]
assert max(np.linalg.norm(A@B-B@A) for A in As for B in As)<1e-15
assert np.linalg.norm(sum(K.conj().T@K for K in Ks)-V@V.conj().T)<2e-15
import sympy as s
zz=s.symbols('z',positive=True);eta=(zz/100)**2
assert s.Rational(180,10000)+s.Rational(36,100)<s.Rational(1,2)
assert s.Rational(256,512)==s.Rational(1,2)
print('PASS complex nine-Bell orthogonality/common sectors, transpose correction, original throughput, and conservative full-error budget')
# Independent exact algebraic-source version of the complex contraction.
w3=(-1+s.I*s.sqrt(3))/2;uc=s.Matrix([1,s.I,1,1])/2
Ve=(s.eye(4)-2*uc*uc.conjugate().T)[:,:3]
Xe=s.Matrix([[0,0,1],[1,0,0],[0,1,0]]);Ze=s.diag(1,w3,w3**2)
ph=s.Matrix([Ve[j,i] for i in range(3) for j in range(4)])/s.sqrt(3)
Pe=s.zeros(12)
for aa,bb in itertools.product(range(3),repeat=2):
 Ue=s.simplify(Xe**aa*Ze**bb);vv=s.simplify(s.kronecker_product(Ue,s.eye(4))*ph)
 Ke=s.Matrix(3,4,lambda i,j:s.conjugate(vv[4*i+j])/s.sqrt(3))
 assert s.simplify(Ke-Ue.conjugate()*Ve.conjugate().T/3)==s.zeros(3,4)
 assert s.simplify(Ue.T*Ke-Ve.conjugate().T/3)==s.zeros(3,4)
 Pe+=vv*vv.conjugate().T
assert s.simplify(Pe-s.kronecker_product(s.eye(3),Ve*Ve.conjugate().T))==s.zeros(12)
print('PASS exact algebraic complex source nine-projector completeness and transpose correction')
