"""Finite binary compiler interface. No dense unitary or exponentially long label list."""
import numpy as np,json
from algebra_compiler_v1 import basis,compile_algebra,gate_rows

def inverse_gates(gates):
 out=[]
 for g in reversed(gates):out.extend([g]*3 if g[0]=='S' else[g])
 return out

def conjugate_gates(gates):
 out=[]
 for g in gates:out.extend([g]*3 if g[0]=='S' else[g])
 return out

def compile_frame(rows,n,k0):
 if not (isinstance(n,int) and isinstance(k0,int) and n>=1 and 1<=k0<=n):raise ValueError('Require integer n>=1 and 1<=k0<=n.')
 A=np.asarray(rows)
 if A.size==0:A=np.zeros((0,2*n),dtype=np.uint8)
 if A.ndim!=2 or A.shape[1]!=2*n or not np.all((A==0)|(A==1)):raise ValueError('Rows must be binary, width2n.')
 A=basis(A.astype(np.uint8))
 if len(A):out=compile_algebra(A,n);a=out['a'];b=out['b'];dec=out['gates']
 else:a=b=0;dec=[]
 cost=a+b;g=n-k0
 if cost>g:return dict(status='abort_cost_exceeds_promise',n=n,k0=k0,g=g,rank=len(A),cost=cost)
 enc=inverse_gates(dec);probe=conjugate_gates(enc)
 return dict(status='compiled',n=n,k0=k0,g=g,rank=len(A),a=a,b=b,cost=cost,basis=A.tolist(),decoder_gates=dec,encoder_gates=enc,probe_reference_gates=probe,gauge_mixing_bits=g,service_private_pad_bits=2*k0)

def logical_label(v,frame):
 if frame['status']!='compiled':raise ValueError('Cannot use abortedframe.')
 n=frame['n'];g=frame['g'];A=np.asarray(v,dtype=np.uint8).reshape(1,2*n).copy()
 for gate in frame['decoder_gates']:gate_rows(A,gate,n)
 return np.concatenate((A[0,g:n],A[0,n+g:])).tolist()

def run():
 rng=np.random.default_rng(202610290036);checks=[]
 for n in [1,2,8,32,128]:
  k0=max(1,n//2);g=n-k0;A=[]
  for j in range(g):
   for c in [j,n+j]:v=np.zeros(2*n,dtype=np.uint8);v[c]=1;A.append(v)
  A=np.array(A,dtype=np.uint8).reshape(-1,2*n)
  if n>1:
   for _ in range(10*n):
    c,t=rng.choice(n,2,replace=False);gate_rows(A,('CX',int(c),int(t)),n);gate_rows(A,('H',int(c)),n);gate_rows(A,('S',int(t)),n)
  f=compile_frame(A,n,k0);assert f['status']=='compiled'
  for row in A:assert not any(logical_label(row,f))
  # Gate inverse identity in binarysymplecticrepresentation.
  E=np.eye(2*n,dtype=np.uint8)
  for gate in f['encoder_gates']+f['decoder_gates']:gate_rows(E,gate,n)
  assert np.array_equal(E,np.eye(2*n,dtype=np.uint8))
  empty=compile_frame([],n,k0);assert empty['rank']==0
  checks.append(dict(n=n,k0=k0,g=g,rank=f['rank'],decoder_gates=len(f['decoder_gates']),encoder_gates=len(f['encoder_gates']),probe_reference_gates=len(f['probe_reference_gates'])))
 # Full2-qubit noise cannot promiseoneprotectedlogicalqubit.
 bad=compile_frame(np.eye(4,dtype=np.uint8),2,1);assert bad['status']=='abort_cost_exceeds_promise'
 print(json.dumps(dict(checks=checks,explicit_abort=bad),indent=2))
if __name__=='__main__':run()
