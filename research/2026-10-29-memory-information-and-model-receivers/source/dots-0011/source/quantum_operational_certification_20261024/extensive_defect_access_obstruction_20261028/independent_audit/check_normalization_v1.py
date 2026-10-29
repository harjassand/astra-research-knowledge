import math,json,numpy as np
from pathlib import Path
count=0;worst=0

def partitions(k,r,cap=None):
 if r==0:
  if k==0:yield []
  return
 for a in range(min(k, k if cap is None else cap),-1,-1):
  for z in partitions(k-a,r-1,a):yield [a]+z
for r in range(1,6):
 for k in range(1,31):
  for p in partitions(k,r):
   l=[p[i]+r-1-i for i in range(r)]
   dim=math.factorial(k)*math.prod(l[i]-l[j] for i in range(r) for j in range(i+1,r))//math.prod(math.factorial(x) for x in l)
   H=-sum((x/k)*math.log2(x/k) for x in p if x)
   b=(r-1)*(r+2)/2
   lower=k*H-b*math.log2(k+r)
   assert lower<=math.log2(dim)+1e-11 and math.log2(dim)<=k*H+1e-11
   count+=1
# Missing-input-isotropy counterexample (author now corrected).
F=np.array([[np.sqrt(2),0]]);C=np.array([[0],[1]])
assert np.allclose(F@F.T,[[2]]) and np.allclose(np.trace(F.T@F)/2,1)
assert np.allclose(F@C,0)
# Explicit large-reference, unit-scale code-specific rows for several dimensions.
err=0
for N in [2,4,8,16]:
 for K in [1,2,3]:
  d=N*K;fs=[]
  for i in range(N):
   f=np.zeros((d,d));f[i*K:(i+1)*K,i*K:(i+1)*K]=np.sqrt(N)*np.eye(K);fs.append(f)
  C=np.kron(np.ones((N,1))/np.sqrt(N),np.eye(K));B=np.concatenate(fs,axis=1);W=np.concatenate([f@C for f in fs],axis=1)
  err=max(err,np.max(abs(B@B.T-N*np.eye(d))),np.max(abs(W-np.eye(d))))
assert err<1e-12
out={'hook_dimension_partition_checks':count,'input_isotropy_counterexample_verified':True,'structured_flag_code_fixtures':12,'max_norm_identity_error':err,'scope':'Exact finite formulas and floating matrix checks; not a universal decoding lower bound or source acquisition.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
