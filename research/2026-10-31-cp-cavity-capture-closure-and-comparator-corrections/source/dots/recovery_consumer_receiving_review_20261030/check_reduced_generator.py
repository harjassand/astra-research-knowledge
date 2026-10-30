import numpy as np,json
from scipy.linalg import expm
rng=np.random.default_rng(73112)
worst=1.; trace_res=0.; deriv_res=0.
def matrix_of(fn,d):
 out=[]
 for j in range(d):
  for i in range(d):
   e=np.zeros((d,d),complex);e[i,j]=1
   out.append(fn(e).reshape(-1,order='F'))
 return np.stack(out,axis=1)
def ptr(x):return np.trace(x.reshape(2,2,2,2),axis1=0,axis2=2)
for it in range(100):
 x=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));H=(x+x.conj().T)/8
 jumps=[(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))/8 for _ in range(3)]
 def L(x):
  y=-1j*(H@x-x@H)
  for a in jumps:
   aa=a.conj().T@a;y+=a@x@a.conj().T-(aa@x+x@aa)/2
  return y
 LB=matrix_of(lambda x:ptr(L(np.kron(np.eye(2)/2,x))),2)
 T=expm(.4*LB)
 blocks=[]
 for i in range(2):
  row=[]
  for j in range(2):
   e=np.zeros((2,2),complex);e[i,j]=1
   row.append((T@e.reshape(-1,order='F')).reshape(2,2,order='F'))
  blocks.append(row)
 C=np.block(blocks)
 worst=min(worst,float(np.linalg.eigvalsh(C)[0]))
 tr=np.array([1,0,0,1]); trace_res=max(trace_res,float(np.linalg.norm(tr@T-tr)))
 # Reduced one-step map has exactly the stated generator derivative.
 full=expm(1e-6*matrix_of(L,4))
 def reduced(x):return ptr((full@np.kron(np.eye(2)/2,x).reshape(-1,order='F')).reshape(4,4,order='F'))
 step=matrix_of(reduced,2)
 deriv_res=max(deriv_res,float(np.linalg.norm((step-np.eye(4))/1e-6-LB)))
assert worst>-1e-10 and trace_res<1e-10 and deriv_res<1e-4
print(json.dumps(dict(trials=100,min_reduced_semigroup_choi_eigenvalue=worst,max_trace_preservation_residual=trace_res,max_short_step_derivative_residual=deriv_res,scope='finite-dimensional channel-calculus regressions, not support theorem proof'),indent=2))
