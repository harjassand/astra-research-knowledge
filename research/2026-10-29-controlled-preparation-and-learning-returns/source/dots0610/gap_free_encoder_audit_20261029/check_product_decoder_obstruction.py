import numpy as np,math,json
from itertools import product
from pathlib import Path
E4=np.zeros((16,2));E4[[5,6,9,10],0]=[.5,-.5,-.5,.5];E4[[3,12,5,6,9,10],1]=np.array([2,2,-1,-1,-1,-1])/(2*np.sqrt(3))
sign4=np.array([(-1)**sum((x>>(3-i))&1 for i in [0,2]) for x in range(16)]);E4=sign4[:,None]*E4
Q,_=np.linalg.qr(E4,mode='complete');comp=Q[:,2:];ds=[E4.T]+[np.outer([1.,0.],v) for v in comp.T]
assert np.linalg.norm(sum(d.T@d for d in ds)-np.eye(16))<1e-12
rows=[]
for h in [1,2]:
 n=4*h;K=2**h;E=E4
 if h==2:E=np.kron(E4,E4)
 dicke=np.array([1/math.sqrt(math.comb(n,n//2)) if x.bit_count()==n//2 else 0 for x in range(2**n)])
 v=E.T@dicke;w=v@v;UE=E-2*np.outer(dicke,v);fe=0
 for ii in product(range(15),repeat=h):
  d=ds[ii[0]] if h==1 else np.kron(ds[ii[0]],ds[ii[1]])
  fe+=abs(np.trace(d@UE))**2/K**2
 lower=4*w*(K-1)/K**2
 assert 1-fe>=lower-1e-12
 rows.append({'h':h,'actual_tensor_local_reset_error':1-fe,'all_left_inverse_decoder_lower_bound':lower,'w':w})
Path(__file__).with_suffix('.json').write_text(json.dumps({'cases':rows,'scope':'Actual tensor local decoder fixtures; general arbitrary-left-inverse statement is proved algebraically.'},indent=2));print(rows)
