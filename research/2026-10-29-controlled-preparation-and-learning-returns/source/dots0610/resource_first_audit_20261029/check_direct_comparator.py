import numpy as np,json,math
from pathlib import Path
rng=np.random.default_rng(295081);I=np.eye(2);sig=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
def kron(xs):
 a=np.ones((1,1))
 for x in xs:a=np.kron(a,x)
 return a
E=np.zeros((16,2));E[[5,6,9,10],0]=[.5,-.5,-.5,.5];E[[3,12,5,6,9,10],1]=np.array([2,2,-1,-1,-1,-1])/(2*np.sqrt(3));P=E@E.T
rows=[]
for h in [1,2,3]:
 # Calculate H acting on code columns directly, without square physical H.
 n=4*h;V=kron([E]*h);K=2**h
 for case in range(10):
  hs=rng.normal(size=(n,3));hs[0]=0;HV=np.zeros(V.shape,complex)
  # Tensor reshape physical rows; apply individual Pauli along its axis.
  tensor=V.reshape([2]*n+[K])
  for i in range(n):
   for a in range(3):
    action=np.tensordot(sig[a],tensor,axes=(1,i));action=np.moveaxis(action,0,i).reshape(V.shape)
    HV+=hs[i,a]*action/2
  variance=np.linalg.norm(HV,'fro')**2/K
  blocks=hs.reshape(h,4,3);formula=np.sum((blocks-blocks.mean(axis=1,keepdims=True))**2)/3
  assert abs(variance-formula)<1e-10
  rows.append({'n':n,'case':case,'residual':abs(variance-formula)})
assert 64*math.pi**2/360000<1/512
Path(__file__).with_suffix('.json').write_text(json.dumps({'block_covariance_checks':rows,'scope':'Direct-code covariance and sufficient constant, not hardware performance comparison.'},indent=2))
print('PASS',len(rows),'n4,n8,n12 direct covariance cases')
