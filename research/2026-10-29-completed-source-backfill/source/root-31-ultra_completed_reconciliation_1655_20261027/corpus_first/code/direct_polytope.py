"""Direct physical-state positive realization via complex diagonal dominance."""
import sys
sys.dont_write_bytecode=True
import json,time
from pathlib import Path
from fractions import Fraction as F
import sympy as S
from exact_instrument import *
from compile_classical import coordinates,enc,formatf
BASE=Path(__file__).resolve().parents[1]

def library():
 states=[]; index={}
 for i in range(D):
  v=S.eye(D)[:,i]; index[i,i,0]=len(states); states.append(projector(v))
 for i in range(D):
  for j in range(i+1,D):
   for z in (1,-1,I,-I):
    v=S.eye(D)[:,i]+z*S.eye(D)[:,j]
    index[i,j,z]=len(states); states.append(projector(v)/2)
 return states,index

def positive_coordinates(Y,index):
 coeff=[S.Rational(0)]*len(index); residual=[Y[i,i] for i in range(D)]
 for i in range(D):
  for j in range(i+1,D):
   r=S.re(Y[i,j]); t=S.im(Y[i,j])
   for value,z in ((r,1 if r>=0 else -1),(t,-I if t>=0 else I)):
    coeff[index[i,j,z]]+=2*abs(value)
    residual[i]-=abs(value); residual[j]-=abs(value)
 for i in range(D):
  assert residual[i]>=0,residual
  coeff[index[i,i,0]]+=residual[i]
 assert all(c>=0 for c in coeff)
 return coeff

def acquire():
 t=time.monotonic(); maps=model(); states,index=library(); kernels=[]
 for mp in maps:
  K=S.zeros(len(states))
  for j,rho in enumerate(states):
   Y=branch(mp['A'],rho); cs=positive_coordinates(Y,index)
   assert clean(sum((c*r for c,r in zip(cs,states)),S.zeros(D)))==Y
   for i,c in enumerate(cs): K[i,j]=c
  kernels.append(K)
 for x in range(2):
  norm=sum((kernels[i] for i,m in enumerate(maps) if m['x']==x),S.zeros(len(states)))
  assert all(sum(norm[:,j])==1 for j in range(len(states)))
 p0=[S.Rational(1,D) if j<D else S.Rational(0) for j in range(len(states))]
 assert sum((c*r for c,r in zip(p0,states)),S.zeros(D))==S.eye(D)/D
 result=dict(classical_states=len(states),controls=2,outcomes=2,
  exact_intertwining_columns=len(states)*len(maps),
  sparse_edges=[sum(c!=0 for c in k) for k in kernels],
  arbitrary_filter_formula='complex diagonal dominance; valid for every positive input in d<=5',
  d3_residual_lower_bound='(3-sqrt(5))/10 times input trace',
  elapsed_seconds=time.monotonic()-t)
 artifact=dict(result=result,states=[enc(coordinates(r)) for r in states],
  initial=[str(c) for c in p0],
  kernels=[[[str(c) for c in row] for row in k.tolist()] for k in kernels],
  maps=[dict(x=m['x'],a=m['a']) for m in maps])
 (BASE/'results'/'DIRECT_CLASSICAL_MODEL.json').write_text(json.dumps(artifact,separators=(',',':'))+'\n')
 (BASE/'results'/'DIRECT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))

if __name__=='__main__': acquire()
