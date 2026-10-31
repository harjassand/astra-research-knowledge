"""Finite-matrix check of the exact hard-core clock construction.
Not a simulation-algorithm implementation or proof of a query lower bound.
"""
from pathlib import Path
import json,numpy as np
from scipy.linalg import expm
bits=[1,0,1,1];N=len(bits);Gamma=1.;ds=2*(N+1);db=2;d=ds*db
A=np.zeros((ds,ds),complex)
for j in range(N):
 for b in range(2):A[2*(j+1)+(b^bits[j]),2*j+b]=1
sm=np.array([[0,1],[0,0]],complex);rows=[]
for lam in [1.,100.]:
 g=np.sqrt(Gamma*lam);mean=1/Gamma+1/(2*lam);T=4*N*mean
 H=g*(np.kron(A,sm.conj().T)+np.kron(A.conj().T,sm));J=2*np.sqrt(lam)*np.kron(np.eye(ds),sm);jj=J.conj().T@J;I=np.eye(d)
 L=-1j*(np.kron(I,H)-np.kron(H.T,I))+np.kron(J.conj(),J)-.5*(np.kron(I,jj)+np.kron(jj.T,I))
 rho=np.zeros((d,d),complex);rho[0,0]=1
 out=(expm(T*L)@rho.reshape(-1,order='F')).reshape(d,d,order='F')
 diag=np.diag(out).real.reshape(N+1,2,2);complete=float(diag[N].sum());parity=int(np.bitwise_xor.reduce(bits));wrong=float(diag[N,1-parity].sum());success=float(diag[N,parity].sum()+.5*(1-complete))
 assert abs(np.trace(out)-1)<1e-9 and complete>=.75-1e-10 and wrong<1e-10
 rows.append({'lambda':lam,'Gamma':Gamma,'T':T,'GammaT':Gamma*T,'cycle_mean_formula':mean,'completed_clock_probability':complete,'wrong_completed_parity_probability':wrong,'parity_success_with_fair_coin_fallback':success,'trace':float(np.trace(out).real)})
result={'scope':'finite exact-matrix diagnostic only','bits':bits,'rows':rows}
print(json.dumps(result,indent=2));Path(__file__).with_name('activity_clock_checks.json').write_text(json.dumps(result,indent=2)+'\n')
