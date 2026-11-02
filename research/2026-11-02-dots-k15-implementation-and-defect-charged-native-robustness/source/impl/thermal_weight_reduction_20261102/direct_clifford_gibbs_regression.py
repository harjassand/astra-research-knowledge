#!/usr/bin/env python3
"""Exhaust every GL(3,2) edge-basis change; test exact termwise and full Gibbs transport."""
from pathlib import Path
import itertools,json,math
import numpy as np
OUT=Path(__file__).parent

def gf_rank(a):
 a=a.copy();r=0
 for c in range(a.shape[1]):
  hits=[i for i in range(r,a.shape[0]) if a[i,c]]
  if not hits:continue
  p=hits[0];a[[r,p]]=a[[p,r]]
  for i in range(a.shape[0]):
   if i!=r and a[i,c]:a[i]^=a[r]
  r+=1
 return r

def inverse(a):
 n=len(a);b=np.concatenate((a.copy(),np.eye(n,dtype=int)),axis=1)
 for j in range(n):
  p=next(i for i in range(j,n) if b[i,j]);b[[j,p]]=b[[p,j]]
  for i in range(n):
   if i!=j and b[i,j]:b[i]^=b[j]
 return b[:,n:]

def vec(x,n):return np.array([(x>>j)&1 for j in range(n)],dtype=int)
def num(v):return sum(int(b)<<j for j,b in enumerate(v))
def X(u,n):
 out=np.zeros((1<<n,1<<n));u=num(u)
 for j in range(1<<n):out[j^u,j]=1
 return out

def Z(v,n):return np.diag([(-1)**(num(v)&j).bit_count() for j in range(1<<n)])
def gibbs(H,beta):
 vals,U=np.linalg.eigh(H);w=np.exp(-beta*(vals-vals.min()));return (U*w)@U.T/w.sum()
n=4;sX=np.array([1,1,1,0]);sZ=[np.array([1,1,0,0]),np.array([0,1,1,0])];J=[1.3,.7,2.1]
Sold=[X(sX,n)]+[Z(v,n) for v in sZ];Hold=sum(Jj*(np.eye(1<<n)-S)/2 for Jj,S in zip(J,Sold))
betas=[.01,.2,1.,7.];rhos=[gibbs(Hold,b) for b in betas];count=0;checks=0;errH=0.;errG=0.;maxsupport=0
for bits in itertools.product(range(2),repeat=9):
 ae=np.array(bits,dtype=int).reshape(3,3)
 if gf_rank(ae)!=3:continue
 A=np.eye(n,dtype=int);A[:3,:3]=ae;Ai=inverse(A);W=np.zeros((1<<n,1<<n))
 for j in range(1<<n):W[num((A@vec(j,n))%2),j]=1
 Snew=[X((Ai@sX)%2,n)]+[Z((A.T@v)%2,n) for v in sZ]
 for Sn,So in zip(Snew,Sold):
  assert np.array_equal(W@Sn@W.T,So);checks+=1
 Hnew=sum(Jj*(np.eye(1<<n)-S)/2 for Jj,S in zip(J,Snew))
 errH=max(errH,float(np.abs(Hnew-W.T@Hold@W).max()))
 for beta,rho in zip(betas,rhos):errG=max(errG,float(np.abs(gibbs(Hnew,beta)-W.T@rho@W).max()))
 for j in range(3):
  maxsupport=max(maxsupport,int(A[:,j].sum()),int(Ai.T[:,j].sum()))
 count+=1
assert count==168 and errH<1e-12 and errG<1e-12 and maxsupport==3
path_cases=[]
for d in [1,2,3,4]:
 maxrow=0;cnt=0
 for perm in itertools.permutations(range(d)):
  cols=[(1<<perm[j])|(1<<perm[j+1]) for j in range(d-1)]
  deg=[sum((c>>j)&1 for c in cols) for j in range(d)];maxrow=max(maxrow,max(deg,default=0));cnt+=1
 path_cases.append({'degree':d,'permutations_tested':cnt,'max_face_row_weight':maxrow})
 assert maxrow<=2
out={'status':'PASS','edge_GL3_matrices':count,'termwise_check_conjugacies':checks,'full_Gibbs_states_tested':count*len(betas),'inverse_temperatures':betas,'largest_Hamiltonian_entry_error':errH,'largest_full_Gibbs_entry_error':errG,'maximum_single_data_Pauli_hook':maxsupport,'parity_path_cases':path_cases,'conservative_resource_ledger':{'historical_K_certificate':180,'governing_untouched_K_certificate':15,'optional_reencoded_K_certificate':13,'governing_untouched_total_qubit_incidence':16,'optional_total_qubit_incidence':16,'governing_untouched_overlap':196,'optional_overlap':196,'untouched_to_historical_peak_ratio':(15/180)**3,'optional_to_untouched_peak_ratio':(13/15)**3,'historical_optional_to_180_peak_ratio':(13/180)**3,'optional_to_untouched_clock_matrix_unit_ratio':(13/15)**2,'source_temperature_penalty':1,'added_data_qubits':0},'scope':'Exact Clifford/full-Gibbs identities; geometry bounds supplied separately, not inferred from this finite Hamiltonian.'}
(OUT/'direct_clifford_gibbs_regression.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
