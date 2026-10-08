"""Numerical diagnostic: twirl a top star eigenstate for the d=5 dual Q.
This is finite floating evidence only; exact algebraic computation is separate.
"""
import numpy as np
D=5
w=np.exp(2j*np.pi/D)
X=np.roll(np.eye(D,dtype=complex),1,axis=0)
Z=np.diag([w**j for j in range(D)])
def W(a,b):
    return (w**((3*a*b)%D))*np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b)
S=[(0,2),(1,0),(1,1),(2,4),(2,1),(2,3)]
I=np.eye(D,dtype=complex)
H=np.zeros((D**3,D**3),complex)
for a,b in S:
    U=W(a,b); Ud=U.conj().T
    H += np.kron(np.kron(U.T,Ud),I)+np.kron(np.kron(Ud.T,U),I)
    H += np.kron(np.kron(U.T,I),Ud)+np.kron(np.kron(Ud.T,I),U)
H=(H+H.conj().T)/2
vals,vecs=np.linalg.eigh(H)
psi=vecs[:,-1]
rho=np.outer(psi,psi.conj())
# Twirl over the 25 Weyl displacements, conjugating all three factors.
rhot=np.zeros_like(rho)
for a in range(D):
  for b in range(D):
    U=W(a,b)
    V=np.kron(np.kron(U.conj(),U),U)
    rhot += V@rho@V.conj().T/ D**2
# Parity and output swap average.
P=np.zeros((D,D),complex)
for j in range(D): P[(-j)%D,j]=1
Vpar=np.kron(np.kron(P.conj(),P),P)
Tswap=np.zeros((D**3,D**3),complex)
for r in range(D):
 for a in range(D):
  for b in range(D):
   ix=(r*D+a)*D+b; jx=(r*D+b)*D+a
   Tswap[jx,ix]=1
rhot=(rhot+Vpar@rhot@Vpar.conj().T+Tswap@rhot@Tswap.conj().T+Vpar@Tswap@rhot@Tswap.conj().T@Vpar.conj().T)/4
# Partial trace B from RAB.
tensor=rhot.reshape(D,D,D,D,D,D) # r,a,b,r',a',b'
rhoRA=np.einsum('rab r a b ->',[]) if False else np.einsum('ra b r2a b ->',[]) if False else None
# explicit correct einsum: preserve r,a,rp,ap and trace b=bp
rhoRA=np.einsum('rabscb->rasc',tensor) # tensor labels r a b s c d ; this string typo guard follows
# Reshape rho_RA as J_{r a,s c}; normalized Choi J=(id⊗Phi)(|Omega><Omega|).
Smat=np.zeros((D*D,D*D),complex)
for i in range(D):
 for j in range(D):
  block=D*rhoRA[i,:,j,:]
  for a in range(D):
   for c in range(D):
    Smat[a*D+c,i*D+j]=block[a,c]
# Hilbert-Schmidt superoperator eigenvalues and Weyl transfer coefficients.
print('lambda_max(H)', vals[-1], 'trace(Q)', 12, 'star dual difference', vals[-1]-12)
print('marginals trace', np.trace(rhoRA), 'marginal unital residual', np.linalg.norm(np.einsum('ra sa->rs',rhoRA)-I/D))
print('Choi hermiticity',np.linalg.norm(rhoRA-rhoRA.conj().transpose(2,3,0,1)))
print('superoperator HS selfadjoint residual',np.linalg.norm(Smat-Smat.conj().T))
print('superoperator positive min eigenvalue',np.linalg.eigvalsh((Smat+Smat.conj().T)/2).min())
lam=[]
for a in range(D):
 for b in range(D):
  if (a,b)==(0,0): continue
  U=W(a,b)
  image=(Smat@U.reshape(-1)).reshape(D,D)
  lam.append(np.trace(U.conj().T@image)/D)
print('transfer min/max', min(l.real for l in lam),max(l.real for l in lam),'max imaginary',max(abs(l.imag) for l in lam))
print('distinct transfer values',sorted({round(l.real,9) for l in lam}))
print('trace rhoRA^2',np.trace(rhoRA@rhoRA).real)
