"""Independent clean one-resource native fixture with both ACTUAL reset monitors.
No direct dephasing substitute. Includes irreversible commit, acquisition abort,
C path, cleanup drive/z-reset, verification and ready return.
"""
import numpy as np,json
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve,eigs
from scipy.linalg import eigvalsh,eigh
states=[('I','f'),('A','o'),('C0','o'),('C1','o'),('Q0','f'),('Q0','o'),('Q0','z'),('Q1','f')]
n0=len(states);n=4*n0;I=np.eye(n);idx=lambda s,a,b:4*s+2*a+b
fam=[('I' if p=='I' else 'A' if p=='A' else 'C' if p[0]=='C' else 'Q') for p,l in states]
ids={f:[idx(s,a,b) for s in range(n0) if fam[s]==f for a in range(2) for b in range(2)] for f in ['I','A','C','Q']}
def trans(pairs,amp=1):
 X=np.zeros((n,n),complex)
 for dst,src in pairs:
  for a in range(2):
   for b in range(2):X[idx(dst,a,b),idx(src,a,b)]=amp
 return X
weak=trans([(1,0)]);weak+=weak.conj().T
H=trans([(3,2)],.9)+trans([(6,5)],.8)+trans([(7,4)],.7);H+=H.conj().T
for s in range(n0):
 for b in range(2):H[idx(s,0,b),idx(s,1,b)]=H[idx(s,1,b),idx(s,0,b)]=.83
 for a in range(2):H[idx(s,a,0),idx(s,a,1)]=H[idx(s,a,1),idx(s,a,0)]=.61
gamma,mu=1.2,.7
js=[trans([(2,1)],np.sqrt(gamma)),trans([(5,1)],np.sqrt(mu)),trans([(0,7)],np.sqrt(1.1)),trans([(4,6)],np.sqrt(.6))]
terminal=trans([(5,3)],np.sqrt(1.3));AT=terminal.conj().T@terminal
# Actual separately clock-label resolved hub monitor and lock-label resolved resource monitor.
for phase in sorted(set(p for p,l in states)):
 j=np.zeros((n,n),complex)
 for s,(p,l) in enumerate(states):
  if p==phase:
   for b in range(2):j[idx(s,0,b),idx(s,1,b)]=np.sqrt(1.17)
 js.append(j)
for lock in ['f','o','z']:
 j=np.zeros((n,n),complex)
 for s,(p,l) in enumerate(states):
  if l==lock:
   for a in range(2):j[idx(s,a,0),idx(s,a,1)]=np.sqrt(.93)
 js.append(j)
# Complete W=0 refresh self-emissions on every A/Q phase.
for phase in ['I','A','Q0','Q1']:
 js.append(trans([(s,s) for s,(p,l) in enumerate(states) if p==phase],np.sqrt(.4)))
def superop(eps):
 hh=H+eps*weak
 K=1j*(np.kron(I,hh)-np.kron(hh.T,I))
 for j in js:
  a=j.conj().T@j;K+=np.kron(j.T,j.conj().T)-.5*(np.kron(I,a)+np.kron(a.T,I))
 K-=.5*(np.kron(I,AT)+np.kron(AT.T,I))
 return csr_matrix(K)
K0=superop(0)
ev=eigs(K0,k=8,which='LR',return_eigenvectors=False,tol=1e-10,maxiter=20000)
Q=np.zeros((n,n),complex)
for s in range(n0):
 q=1 if fam[s] in ['I','Q'] else mu/(gamma+mu) if fam[s]=='A' else 0
 for a in range(2):
  for b in range(2):Q[idx(s,a,b),idx(s,a,b)]=q
assert np.linalg.norm(K0@Q.reshape(-1,order='F'))<1e-10
Z=np.diag([1 if fam[s]=='I' else -1 for s in range(n0) for _ in range(4)])
Rs=[];raw=[]
for eps in [.1,.05,.025,.0125]:
 K=superop(eps);r=spsolve(K,-I.reshape(-1,order='F')).reshape((n,n),order='F');r=(r+r.conj().T)/2
 rr=r[np.ix_(ids['I'],ids['I'])];odd=(r-Z@r@Z)/2
 forbidden=odd.copy();forbidden[np.ix_(ids['I'],ids['A'])]=0;forbidden[np.ix_(ids['A'],ids['I'])]=0
 raw.append([eps,float(np.trace(rr).real/len(ids['I'])),float(eigvalsh(r)[-1]),float(np.linalg.norm(forbidden))]);Rs.append(r)
# Extrapolate c0 from epsilon^2 times the idle average, permitting bounded even corrections.
x=np.array([r[0]**2 for r in raw]);y=np.array([r[0]**2*r[1] for r in raw]);c0=float(np.polynomial.polynomial.polyfit(x,y,3)[0])
C=max(row[2]-c0/row[0]**2 for row in raw)+2;b=.08/c0
cases=[]
for (eps,idle,rmax,forbidden),r in zip(raw,Rs):
 beta=b*eps**2;Rmax=c0/eps**2+C;s0=1-beta*Rmax;S=s0*I+beta*r
 e,u=eigh(S);assert e[0]>.5 and e[-1]<=1+1e-10
 sqrtS=(u*np.sqrt(e))@u.conj().T
 QAt=sqrtS@AT@sqrtS # virtual ready branch is exactly zero on terminal intensity
 cancellation=QAt-s0*AT
 off=r.copy()
 for f in ['I','A','C','Q']:off[np.ix_(ids[f],ids[f])]=0
 off[np.ix_(ids['I'],ids['A'])]=0;off[np.ix_(ids['A'],ids['I'])]=0
 cases.append({'epsilon':eps,'resolvent_residual':float(np.linalg.norm(superop(eps)@r.reshape(-1,order='F')+I.reshape(-1,order='F'))),'spectral_excess_over_leading_idle_pole':rmax-c0/eps**2,'idle_scaled_deviation':float(np.linalg.norm(r[np.ix_(ids['I'],ids['I'])]-c0/eps**2*np.eye(4))),'odd_forbidden_corner':forbidden,'all_non_IA_family_coherences':float(np.linalg.norm(off)),'C_resolvent_vs_reference':float(np.linalg.norm(r[np.ix_(ids['C'],ids['C'])]-Rs[-1][np.ix_(ids['C'],ids['C'])])),'terminal_commutator_remainder_over_eps2':float(np.linalg.norm(cancellation,2)/eps**2),'S_min':float(e[0]),'S_max':float(e[-1])})
 assert cases[-1]['resolvent_residual']<1e-7
 assert forbidden<1e-10 and cases[-1]['all_non_IA_family_coherences']<1e-10
 assert cases[-1]['C_resolvent_vs_reference']<1e-10
result={'controller_dimension':n,'main_clock_lock_states':states,'zero_drive_top_real_eigenvalues':sorted([float(z.real) for z in ev],reverse=True),'zero_drive_return_effect_residual':float(np.linalg.norm(K0@Q.reshape(-1,order='F'))),'extrapolated_leading_c0':c0,'fixed_excess_C_for_fixture':C,'cases':cases,'scope':'Independent finite actual-monitor regression; general proof is analytical, not inferred from these numbers'}
print(json.dumps(result,indent=2))
