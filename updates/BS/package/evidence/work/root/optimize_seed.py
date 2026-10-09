import sys
sys.path.insert(0,'work/vendor')
import numpy as np,json
from scipy.optimize import linprog
from fractions import Fraction as F
j=json.load(open('work/hidden_equilibrium/certificate.txt'))
v=np.array([[float(F(x)) for x in r] for r in j['points']]);z=np.array([[float(F(x)) for x in r] for r in j['farkas_z']]);fac=np.array([[float(F(x)) for x in r] for r in j['facets']]);edges=[(i,k) for i in range(5) for k in range(5) if i!=k]
H=np.column_stack([np.ones(5),v]);N=np.linalg.svd(H.T)[2][3:]
v0=v-v.mean(0)
def gen(x):
 Q=np.zeros((5,5))
 for r,(i,k) in zip(x,edges): Q[i,k]=r;Q[i,i]-=r
 return Q
def eq(x):
 Q=gen(x);A=v0.T@Q@v0
 return np.r_[Q.sum(0)[:4],(N@Q@v).ravel(),A[0,1]-A[1,0]]
Aeq=np.column_stack([eq(u) for u in np.eye(20)])
objective=np.array([.1*z[i]@(v[k]-v[i]) for i,k in edges])
Aub=np.array([[int(i==s) for i,k in edges] for s in range(5)])
print('rank',np.linalg.matrix_rank(Aeq))
results=[]
for eta in [.05,.1,.125,.15,.2]:
 kappa=eta*fac[:,0].sum();r=linprog(-objective,A_ub=Aub,b_ub=np.full(5,1-kappa),A_eq=Aeq,b_eq=np.zeros(len(Aeq)),bounds=[(.0002,None)]*20,method='highs')
 if not r.success: print(r.message);continue
 print('eta',eta,'gamma',-r.fun,'gain',-r.fun/.005976777578630566,'active',np.flatnonzero(r.x>.000201).tolist())
 results.append(dict(eta=eta,gamma=-r.fun,rates=r.x.tolist(),eq_residual=float(abs(Aeq@r.x).max()),status='floating LP exploration, not certified new seed'))
json.dump(results,open('work/root/SEED_OPTIMIZATION.json','w'),indent=2)
