"""Finite algebra diagnostics, not a native simulation or an all-size proof."""
import itertools, math, json
import numpy as np
from scipy.linalg import expm
n=0
for sizes in [(2,3),(1,2,3),(3,3,2)]:
  for thresholds in itertools.product(*[range(1,m+2) for m in sizes]):
    for counts in itertools.product(*[range(m+1) for m in sizes]):
      sieves=[]
      for k,t in zip(counts,thresholds):
        a=sum((-1)**(s-t)*math.comb(s-1,t-1)*math.comb(k,s) for s in range(t,k+1))
        assert a==int(k>=t)
        sieves.append(a)
      union=sum((-1)**(len(A)+1)*math.prod(sieves[i] for i in A)
                for z in range(1,len(sizes)+1) for A in itertools.combinations(range(len(sizes)),z))
      assert union==int(any(k>=t for k,t in zip(counts,thresholds)))
      n+=1
U=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)
tau=0.73
H=math.pi/(2*tau)*(np.eye(4)-U)
res=float(np.linalg.norm(expm(-1j*tau*H)-U,2))
assert res<1e-14
assert abs(np.linalg.norm(H,2)-math.pi/tau)<1e-14
print(json.dumps({'signed_group_union_fixtures':n,'cnot_endpoint_operator_residual':res,'status':'PASS','limit':'Finite algebra checks only; general proof is in binding completions.'},indent=2))
