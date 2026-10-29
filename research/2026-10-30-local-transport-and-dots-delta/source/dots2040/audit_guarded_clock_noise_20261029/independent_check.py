import numpy as np, json
from itertools import combinations
from pathlib import Path
# Import only the supplied physical MODEL, independently form observables/generators.
ns={};exec(Path('producer-workspace/hardcore_test.py').read_text(),ns)
V,H,W,dim,neigh= [ns[k] for k in ['V','H','W','dim','neigh']]
kron=ns['kron'];I3=np.eye(3);P0=np.diag([1,0,0]);Id=np.eye(dim)
def aux(a,x):return kron([np.eye(4)]+[a if j==x else I3 for j in range(3)])
Q=[aux(I3-P0,x) for x in range(3)];P=[Id-q for q in Q]
J=[]
for x in range(3):
 js=[]
 for s in (1,2):
  a=np.zeros((3,3));a[0,s]=1;js.append(aux(a,x))
 J.append(js)
def dual(A):
 return 1j*(H@A-A@H)+sum(j.conj().T@A@j-(j.conj().T@j@A+A@j.conj().T@j)/2 for js in J for j in js)
R=[Q[x]-V[x]@V[x].conj().T for x in range(3)]
B=[]
for x in range(3):
 G=Id.copy()
 for y in neigh[x]:G=G@P[y]
 B.append(Q[x]-V[x]@V[x].conj().T@G)
out={'R_decay_residual':max(float(np.linalg.norm(dual(r)+r)) for r in R), 'edge_decay_residual':max(float(np.linalg.norm(dual(Q[x]@Q[y])+2*Q[x]@Q[y])) for x,y in [(0,1),(1,2)]),'B_commutator':max(float(np.linalg.norm(a@b-b@a)) for a in B for b in B)}
Pg=Id.copy()
for b in B:Pg=Pg@(Id-b)
out['good_image_residual']=float(np.linalg.norm(Pg-W@W.conj().T))
out['product_drift_max_eigenvalues']={}
for r in range(1,4):
 for S in combinations(range(3),r):
  A=Id.copy()
  for x in S:A=A@B[x]
  d=dual(A)+r*A
  out['product_drift_max_eigenvalues'][str(S)]=float(np.linalg.eigvalsh(d).max())
# Genuine-vs-formal event distinction: total generator 0 is CPTP but killing a canceled jump isn't positive.
j=np.array([[0.,1.],[0.,0.]])
rho=np.diag([0.,1.]);dt=.01
out['formal_killed_state_min_eigenvalue']=float(np.linalg.eigvalsh(rho-dt*j@rho@j.T).min())
assert out['R_decay_residual']<1e-12 and out['edge_decay_residual']<1e-12 and out['good_image_residual']<1e-12
assert max(out['product_drift_max_eigenvalues'].values())<1e-12
Path('producer-workspace/independent_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
