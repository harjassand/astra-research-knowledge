import json
import math
import numpy as np

H = np.diag([1.0,2.0])
E = np.array([[0.5,1/(2*math.sqrt(2))],[1/(2*math.sqrt(2)),0.75]])
R = 1/math.sqrt(2)*np.array([[1.0,1/math.sqrt(2)],[0.0,1.0]])
T = np.linalg.inv(R)
C = math.log((1+math.sqrt(17))/2)
alpha = 5/6*math.log(4)
sstar = math.log(1+math.sqrt(5))
assert np.allclose(R.T@R,E)
assert C < alpha < sstar
rows=[]
for n in range(1,10):
 En=np.array([[1.]])
 Tn=np.array([[1.]])
 for _ in range(n):
  En=np.kron(En,E)
  Tn=np.kron(Tn,T)
 energies=np.array([n+i.bit_count() for i in range(2**n)])
 for Q in range(n,2*n+1):
  ids=np.flatnonzero(energies<=Q)
  small=En[np.ix_(ids,ids)]
  p=np.linalg.eigvalsh(small)[0]
  inv=np.linalg.norm(Tn[:,ids],2)**2
  assert abs(p*inv-1)<1e-8, (n,Q,p,inv)
  rate=-math.log(p)/Q
  assert rate <= C+1e-8
  rows.append({'n':n,'Q':Q,'lambda_min':float(p),'exponent':rate,'compression_inverse_error':abs(p*inv-1)})
res={'E':E.tolist(),'R':R.tolist(),'H':H.tolist(),'C':C,'alpha':alpha,'s_star':sstar,'best_tested':max(rows,key=lambda x:x['exponent']),'checks':rows}
print(json.dumps({k:v for k,v in res.items() if k!='checks'},indent=2))
with open('work/agents/hard_energy/variational/sw/counterexample/check.json','w') as f:
 json.dump(res,f,indent=2)
