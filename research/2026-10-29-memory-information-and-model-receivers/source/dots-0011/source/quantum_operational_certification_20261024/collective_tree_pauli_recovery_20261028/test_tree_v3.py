#!/usr/bin/env python3
"""Ordinary product-Pauli acquisition and exact rational global oracle guard."""
import numpy as np,json,math
from fractions import Fraction as F
from pathlib import Path
H=Path(__file__).parent
# Alphabet I,X,Y,Z; row a is the character of measurement axis a.
CHAR=np.array([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]],dtype=np.int8)
n=8;N=2**22;seed=202610282259;delta=F(1,400)
rng=np.random.default_rng(seed)
# Source truth is confined to generator and posthoc diagnostics.
pi=np.array([.7,.1,.1,.1]);T=.99*np.eye(4)+.01*np.ones((4,4))/4
one=np.zeros((n,4),np.int64);two=np.zeros((n-1,4,4),np.int64)
for start in range(0,N,16384):
 m=min(16384,N-start);err=np.zeros((m,n),np.int8);u0=rng.integers(0,10,size=m);err[:,0]=np.where(u0<7,0,u0-6)
 for j in range(1,n):
  u=rng.integers(0,400,size=m);old=err[:,j-1];err[:,j]=np.where(u<397,old,(old+u-396)%4)
 axes=rng.integers(1,4,size=(m,n));signs=rng.integers(0,2,size=(m,n))*2-1
 outcomes=signs*CHAR[axes,err]
 # Learner input: axes, input signs, measured output signs only.
 y=signs*outcomes
 numer=1+3*CHAR[axes[:,:,None],np.arange(4)[None,None,:]]*y[:,:,None]
 # Per-symbol estimator numer/4 in {1,-1/2}.
 one+=np.sum(numer,axis=0)
 two+=np.einsum('mja,mjb->jab',numer[:,:-1,:].astype(np.int64),numer[:,1:,:].astype(np.int64))
np.savez_compressed(H/'sufficient_counts_v3.npz',one=one,two=two)
p1=[[F(int(x),4*N) for x in row] for row in one]
p2=[[[F(int(x),16*N) for x in row] for row in edge] for edge in two]
clip=lambda x:max(F(0),min(F(1),x))
lo1=[[clip(v-delta) for v in row] for row in p1];hi1=[[clip(v+delta) for v in row] for row in p1]
lo2=[[[clip(v-delta) for v in row] for row in e] for e in p2];hi2=[[[clip(v+delta) for v in row] for row in e] for e in p2]
assert min(v for row in lo1 for v in row)>0
lower=[[[lo2[j][a][b]/hi1[j][a] for b in range(4)] for a in range(4)] for j in range(n-1)]
upper=[[[min(F(1),hi2[j][a][b]/lo1[j][a]) for b in range(4)] for a in range(4)] for j in range(n-1)]
# Proposal is arbitrary data-only positive-factor MAP; confidence guard is exact.
point=[[[max(F(1,10**12),p2[j][a][b])/max(F(1,10**12),p1[j][a]) for b in range(4)] for a in range(4)] for j in range(n-1)]
def maximize(root,trans,exclude=None):
 states={(a,exclude is not None and a!=exclude[0]):(root[a],(a,)) for a in range(4)}
 for j in range(n-1):
  nxt={}
  for (a,diff),(val,word) in states.items():
   for b in range(4):
    key=(b,diff or (exclude is not None and b!=exclude[j+1]));item=(val*trans[j][a][b],word+(b,))
    if key not in nxt or item[0]>nxt[key][0]:nxt[key]=item
  states=nxt
 valid=[v for (_,diff),v in states.items() if exclude is None or diff]
 return max(valid,key=lambda x:x[0])
_,candidate=maximize([max(F(1,10**12),v) for v in p1[0]],point)
low=lo1[0][candidate[0]]
for j in range(n-1):low*=lower[j][candidate[j]][candidate[j+1]]
up,competitor=maximize(hi1[0],upper,candidate)
# Rigorous rational Hoeffding failure bound using exp(x)>=sum_{k=0}^80 x^k/k!.
M=4*n+16*(n-1);x=2*N*delta**2/F(9,4);term=F(1);partial=F(1)
for k in range(1,81):term*=x/k;partial+=term
failure=2*M/partial
truth=pi[candidate[0]]
for j in range(n-1):truth*=T[candidate[j],candidate[j+1]]
result={'n':n,'N_full_channel_calls':N,'native_qubit_exposures':n*N,'ordinary_single_qubit_preparations':n*N,'ordinary_single_qubit_readouts':n*N,'seed':seed,'delta':str(delta),'coefficient_count':M,'rigorous_failure_bound':str(failure),'failure_float':float(failure),'candidate':candidate,'candidate_probability_lower':str(low),'candidate_lower_float':float(low),'competitor_upper':str(up),'competitor_upper_float':float(up),'worst_upper_competitor':competitor,'guard_passes':low>up,'posthoc_true_candidate_probability':float(truth),'learner_inputs':'axes, preparation signs and measured output signs only; no error labels, pi or T','confidence_scope':'fixed stationary Pauli source with known tree distribution promise; ordinary independent full-channel calls'}
# Division-free score D*p(x), with D the common product of internal marginals.
# Here each chain internal vertex has one child. Pair factors multiplied by
# node product over the THREE unselected state marginals; no inverse occurs.
def poly_trans(marg,edge):
 out=[]
 for j in range(n-1):
  out.append([[edge[j][a][b]*math.prod(marg[j][c] for c in range(4) if c!=a) for b in range(4)] for a in range(4)])
 return out
poly_low_trans=poly_trans(lo1,lo2);poly_up_trans=poly_trans(hi1,hi2)
poly_low=lo1[0][candidate[0]]
for j in range(n-1):poly_low*=poly_low_trans[j][candidate[j]][candidate[j+1]]
poly_up,poly_competitor=maximize(hi1[0],poly_up_trans,candidate)
result.update({'division_free_candidate_lower':str(poly_low),'division_free_competitor_upper':str(poly_up),'division_free_ratio_lower_to_upper':float(poly_low/poly_up),'division_free_passes':poly_low>poly_up,'division_free_worst_competitor':poly_competitor,'generator':'exact rational categorical laws via uniform integer draws; no floating CDF threshold'})
(H/'results_v3.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
