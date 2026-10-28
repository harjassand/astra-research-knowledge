"""Exercise the acquired local kernel on overlapping and reversed gate placements."""
import sys
sys.dont_write_bytecode=True
from itertools import product
import json,time
import numpy as np
import sympy as S
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]

def run():
 t=time.monotonic();data=json.loads((BASE/'results'/'EXACT_REPAIRED_KERNEL.json').read_text());N=len(data['local_states']);d=3;n=3
 states=np.array([[[complex(S.sympify(v)) for v in row] for row in M] for M in data['local_states']])
 U=np.array([[complex(S.sympify(v)) for v in row] for row in data['gate']]);K=np.zeros((N*N,N*N))
 for col in data['kernels']:
  a,b=col['input']
  for i,j,p in col['transitions']:K[i*N+j,a*N+b]=float(S.Rational(p))
 assert np.max(abs(K.sum(axis=0)-1))<1e-13
 basis=list(product(range(d),repeat=n));index={v:i for i,v in enumerate(basis)}
 initial=(2,0,1);rho=np.zeros((d**n,d**n),complex);rho[index[initial],index[initial]]=1
 hidden=np.zeros((N,)*n);hidden[initial]=1
 records=[]
 for pair in ((0,1),(1,2),(0,2),(2,0),(1,0),(0,1)):
  axes=list(pair)+[i for i in range(n) if i not in pair]
  tmp=np.transpose(hidden,axes);hidden=np.transpose((K@tmp.reshape(N*N,-1)).reshape((N,)*n),np.argsort(axes))
  full=np.zeros_like(rho)
  for i,out in enumerate(basis):
   for j,inp in enumerate(basis):
    if all(out[k]==inp[k] for k in range(n) if k not in pair):
     full[i,j]=U[d*out[pair[0]]+out[pair[1]],d*inp[pair[0]]+inp[pair[1]]]
  rho=full@rho@full.conj().T
  for site in pair:
   new=np.empty_like(rho)
   for i,out in enumerate(basis):
    for j,inp in enumerate(basis):
     swapped_out=list(out);swapped_in=list(inp);swapped_out[site]=inp[site];swapped_in[site]=out[site]
     pt=rho[index[tuple(swapped_out)],index[tuple(swapped_in)]]
     tr=0j
     if out[site]==inp[site]:
      for value in range(d):
       a=list(out);b=list(inp);a[site]=b[site]=value;tr+=rho[index[tuple(a)],index[tuple(b)]]
     new[i,j]=(1.8*tr-pt)/4.4
   rho=new
  expanded=np.einsum('abc,aij,bkl,cmn->ikmjln',hidden,states,states,states,optimize=True).reshape(d**n,d**n)
  error=float(np.max(abs(expanded-rho)));assert error<1e-12
  records.append(dict(gate_pair=list(pair),full_density_error=error,hidden_mass=float(hidden.sum()),quantum_trace=float(np.trace(rho).real)))
 result=dict(qutrits=n,gates=len(records),checked_hidden_configurations=N**n,
  scope='Implementation replay; the exact one-step intertwining is what certifies arbitrary width/depth.',records=records,
  elapsed_seconds=time.monotonic()-t)
 (BASE/'results'/'CIRCUIT_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(qutrits=n,gates=len(records),max_full_density_error=max(r['full_density_error'] for r in records),elapsed_seconds=result['elapsed_seconds']),indent=2))

if __name__=='__main__':run()
