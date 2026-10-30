import numpy as np, json
n=7; N=1<<n; generators=[0b1111000,0b1100110,0b1010101]
S=[0]
for g in generators:S += [v^g for v in S[:]]
P=np.zeros((N,N))
for g in S:
 for x in range(N): P[x^g,x]+=1/len(S)
zero=P[:,0]/np.sqrt(P[0,0]); es=[0]+[1<<i for i in range(n)]
allowed=np.stack([zero[np.arange(N)^e] for e in es],axis=1)
Q=allowed@allowed.T
res=0.; branches=0
for e in es:
 for z in range(N):
  phase=np.array([(-1)**((x&z).bit_count()) for x in range(N)])
  v=(phase*zero)[np.arange(N)^e]
  res=max(res,np.linalg.norm((np.eye(N)-Q)@P@v));branches+=1
assert res<1e-10
out=dict(result='PASS',code='7-qubit Steane CSS',tested_module_generators=branches,postselected_module_residual=float(res),twirled_effect_identity_residual=float(np.max(abs(np.diag(P)-1/8))),scope='DATA algebra only; no native prefix or autonomous window')
print(json.dumps(out,indent=2))
