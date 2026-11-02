import itertools,json,sys,numpy as np
from scipy.special import xlogy
sys.path.insert(0,'producer-workspace/consequential_alternative_20261102')
from flagged_repetition import rep_data,evaluate
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);pauli=[I,X,Y,Z]
def entropy(a):
 e=np.linalg.eigvalsh(a);e=np.maximum(e,0);return float(-np.sum(xlogy(e,e))/np.log(2))
def brute(n,w,p,lam):
 d=2**n;psi=np.zeros(2*d,complex);psi[0]=np.sqrt(lam);psi[-1]=np.sqrt(1-lam);out=0.
 for flags in itertools.product(range(len(w)),repeat=n):
  wf=np.prod(w[list(flags)]);rb=np.zeros((2*d,2*d),complex)
  for pars in itertools.product(range(4),repeat=n):
   prob=np.prod([p[f,a] for f,a in zip(flags,pars)]);u=np.eye(1)
   for a in pars:u=np.kron(u,pauli[a])
   phi=np.kron(I,u)@psi;rb+=prob*np.outer(phi,phi.conj())
  b=rb[:d,:d]+rb[d:,d:];out+=wf*(entropy(b)-entropy(rb))
 return out
w=np.array([.37,.63]);p=np.array([[.8,.09,.03,.08],[.48,.12,.17,.23]])
results=[]
for n in [1,2,3]:
 for l in [.1,.3,.5]:
  a=evaluate(rep_data(n,w,p,3),l);b=brute(n,w,p,l);results.append(dict(n=n,lam=l,formula=a,density=b,difference=a-b))
print(json.dumps(results,indent=2));json.dump(results,open('producer-workspace/repetition_density_validation.json','w'),indent=2)
