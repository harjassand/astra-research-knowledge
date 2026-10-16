"""Exact identity/rounding tests plus separately labelled mpmath diagnostics."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import sys,itertools,json,random,math
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import mpmath as mp
sys.path.insert(0,os.environ.get('PAIR_CERTIFICATE_BASE',str(Path(__file__).resolve().parent/'original_dependencies')))
from rigorous_pair_certificate import pair_H,EnclosedSurvival
from exterior_certificate import PathSurvival

def wedge(L):
 n=len(L);pairs=list(itertools.combinations(range(n),2));idx={p:i for i,p in enumerate(pairs)};B=np.zeros((len(pairs),len(pairs)),dtype=object)
 for j,(x,y) in enumerate(pairs):
  for z in range(n):
   if z!=y:B[idx[tuple(sorted((z,y)))],j]+=int(L[z,x])*(1 if z<y else -1)
   if z!=x:B[idx[tuple(sorted((x,z)))],j]+=int(L[z,y])*(1 if x<z else -1)
 return B

identities=0;diagnostics=[];mp.mp.dps=90
for rates in [[0,0,0],[1,10,100,1000,10000],[7,3,11,2],[1,1,1,1,1,1],[0,7,0,2]]:
 n=len(rates)+1;L=np.zeros((n,n),dtype=object)
 for i,r in enumerate(rates):L[i,i]+=r;L[i+1,i+1]+=r;L[i,i+1]-=r;L[i+1,i]-=r
 H,ei=pair_H(n,[(i,i+1) for i in range(n-1)],rates)
 assert np.array_equal(H,wedge(L));identities+=1
 ob=PathSurvival(rates,75)
 for t in [F(0),F(1,2**20),F(1,8),F(1,2),F(1)]:
  lo,hi=ob.at(t);E=mp.expm(-mp.mpf(t.numerator)/t.denominator*mp.matrix(H.tolist()));true=[sum(E[i,j] for j in range(len(H))) for i in ei]
  margin=min(min(v-mp.mpf(l)/ob.D,mp.mpf(h)/ob.D-v) for v,l,h in zip(true,lo,hi))
  assert margin>=-mp.mpf('1e-80')
  diagnostics.append(dict(rates=rates,t=str(t),smallest_interval_margin=str(margin)))
# Independently test the claimed rounding bound against exact rational powers.
rates=[1,3,2];n=4;Q=1<<18;N=1<<5
L=np.zeros((n,n),dtype=object)
for i,r in enumerate(rates):L[i,i]+=r;L[i+1,i+1]+=r;L[i,i+1]-=r;L[i+1,i]-=r
P=np.eye(n,dtype=object)*Q-L*(Q//N);pow=[P]
for j in range(5):pow.append((pow[-1]@pow[-1])//Q)
exact=[[F(int(P[i,j]),Q) for j in range(n)] for i in range(n)]
def mm(A,B):return [[sum((a*b for a,b in zip(row,col)),F(0)) for col in zip(*B)] for row in A]
T=[[F(i==j) for j in range(n)] for i in range(n)];round_checks=0
for k in range(N+1):
 if k:T=mm(T,exact)
 M=np.eye(n,dtype=object)*Q;h=k;j=0
 while h:
  if h&1:M=(M@pow[j])//Q
  h>>=1;j+=1
 for i in range(n):
  dif=[T[i][j]-F(int(M[i,j]),Q) for j in range(n)]
  assert min(dif)>=0 and sum(dif)<=F(k*n,Q)
 round_checks+=1
# Certificate input rejects noninteger and negative rates.
for bad in [[1,F(1,2)],[1,-1]]:
 try:PathSurvival(bad)
 except AssertionError:pass
 else:raise AssertionError('invalid input accepted')
result=dict(exact_generator_identity_checks=identities,exact_rounding_checks=round_checks,input_rejection_tests=2,high_precision_diagnostics=diagnostics,
 scope='integer generator and rational rounding checks are exact; mpmath exponential agreement is a diagnostic, not used in the certificate')
Path(__file__).with_name('verification_receipt.json').write_text(json.dumps(result,indent=2));print('PASS exact identities',identities,'rounding',round_checks,'mpmath diagnostics',len(diagnostics))
