import numpy as np,json
rng=np.random.default_rng(271118)
def rand(n,m):return rng.normal(size=(n,m))+1j*rng.normal(size=(n,m))
def rho(n):
 x=rand(n,n);x=x@x.conj().T;return x/np.trace(x)
def trA(X,s):return sum(X[i*s:(i+1)*s,i*s:(i+1)*s] for i in range(3))
def choi(E,s):
 return np.block([[E(np.eye(3,dtype=complex)[:,i:i+1]@np.eye(3,dtype=complex)[j:j+1,:]) for j in range(3)] for i in range(3)])/3
phi=np.eye(3).reshape(-1)/np.sqrt(3);Phi=np.outer(phi,phi)
maxerr=0;cases=0
for r in [1,2,3]:
 s=3*r+1
 for k in range(8):
  V=np.linalg.qr(rand(s,3*r))[0];sig=rho(r);tau=rho(s);p=.1+.8*rng.random()
  Es=lambda x:p*V@np.kron(x,sig)@V.conj().T
  En=lambda x:(1-p)*np.trace(x)*tau
  E=lambda x:Es(x)+En(x)
  Ks=[rand(3,s) for _ in range(2)];G=sum(K.conj().T@K for K in Ks);scale=min(1/np.sqrt(np.linalg.eigvalsh(G)[-1]),np.sqrt(3*r/np.trace(G).real))*.8;Ks=[scale*K for K in Ks]
  D=lambda x:sum(K@x@K.conj().T for K in Ks)
  Dadj=lambda x:sum(K.conj().T@x@K for K in Ks)
  F=np.block([[Dadj(np.eye(3)[:,i:i+1]@np.eye(3)[j:j+1,:]) for j in range(3)] for i in range(3)])/3
  J=choi(E,s);om=np.kron(np.eye(3)/3,E(np.eye(3)/3));H=J-3*om
  Cs=choi(lambda x:D(Es(x)),3);Cn=choi(lambda x:D(En(x)),3)
  ass=np.trace(Cs).real;an=np.trace(Cn).real;fs=np.trace(Phi@Cs).real;fn=np.trace(Phi@Cn).real
  vals=[abs(np.trace(J@F).real-fs-fn),abs(9*np.trace(om@F).real-ass-an),abs(fn-an/9),abs((2*p/3-np.trace(H@F).real)-(2*(p-ass)/3+ass-fs+2*an/9)),np.linalg.norm(trA(F,s)-sum(K.conj().T@K for K in Ks)/3)]
  maxerr=max(maxerr,*vals);assert max(vals)<1e-11;assert np.linalg.eigvalsh(F)[0]>-1e-12 and np.linalg.eigvalsh(F)[-1]<=1+1e-12;assert np.trace(F).real<=r+1e-12
  cases+=1
print(json.dumps({'status':'PASS numerical corroboration only','cases':cases,'max_identity_residual':maxerr,'scope':'arbitrary overlapping reset, direct CP decoder, normalization and exact loss identities'},indent=2))
