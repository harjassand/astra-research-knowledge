import numpy as np,json,itertools,math
from scipy.linalg import eigh
from functools import reduce
P=[np.eye(2,dtype=complex),np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1,-1]).astype(complex)]
kron=lambda xs:reduce(np.kron,xs)
def perm_indices(n,p):return np.array([sum(((x>>(n-1-p[i]))&1)<<(n-1-i) for i in range(n)) for x in range(2**n)])
sing=np.array([0,1,-1,0])/np.sqrt(2);tp=np.array([1,0,0,0]);tm=np.array([0,0,0,1]);t0=np.array([0,1,1,0])/np.sqrt(2)
omega=(np.kron(tp,tm)-np.kron(t0,t0)+np.kron(tm,tp))/np.sqrt(3)
rows=[]
for n in [4,6,8]:
 d=2**n;J=[sum(kron([P[a] if i==j else P[0] for i in range(n)]) for j in range(n))/2 for a in range(1,4)];ev,Z=eigh(sum(A@A for A in J));Es=Z[:,ev<1e-8];Ps=Es@Es.conj().T;ds=Es.shape[1]
 p=list(range(n));p[0],p[1]=p[1],p[0];S=np.eye(d)[perm_indices(n,p)];PiM=(np.eye(d)-S)/2;PiP=(np.eye(d)+S)/2
 minus=kron([sing]*(n//2));plus=np.kron(omega,kron([sing]*((n-4)//2))) if n>4 else omega
 rm=np.zeros((d,d),complex);rp=rm.copy();cnt=0
 for p in itertools.permutations(range(2,n)):
  idx=perm_indices(n,[0,1]+list(p));vm=minus[idx];vp=plus[idx];rm+=np.outer(vm,vm.conj());rp+=np.outer(vp,vp.conj());cnt+=1
 rm/=cnt;rp/=cnt;pm=(n+2)/(4*(n-1));pp=1-pm
 errm=np.linalg.norm(rm-PiM@Ps/(pm*ds));errp=np.linalg.norm(rp-PiP@Ps/(pp*ds));errsum=np.linalg.norm(pm*rm+pp*rp-Ps/ds)
 assert max(errm,errp,errsum)<1e-11
 rows.append({'n':n,'singlet_dimension':ds,'p_minus':pm,'p_plus':pp,'minus_rank':round(pm*ds),'plus_rank':round(pp*ds),'spectator_permutations':cnt,'minus_branch_residual':float(errm),'plus_branch_residual':float(errp),'total_ensemble_residual':float(errsum)})
print(json.dumps({'checks':rows},indent=2))
