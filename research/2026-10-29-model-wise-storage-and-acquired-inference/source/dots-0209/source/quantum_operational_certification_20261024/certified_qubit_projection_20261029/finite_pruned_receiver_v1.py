"""Exact fixed-column qubit POVM pruning and default-label sampler.
The mathematical channel identity is for exact coins; finite cap is paid.
"""
from fractions import Fraction as F
from math import gcd,lcm
from certified_projection_v1 import psd_exact,scale

def dependence(columns):
 """Primitive integer null vector for <=5 original four-coordinate columns."""
 n=len(columns);A=[[columns[j][i] for j in range(n)] for i in range(4)]
 pivots=[];row=0
 for col in range(n):
  pick=next((i for i in range(row,4) if A[i][col]),None)
  if pick is None:continue
  A[row],A[pick]=A[pick],A[row];q=A[row][col];A[row]=[x/q for x in A[row]]
  for i in range(4):
   if i!=row:
    q=A[i][col];A[i]=[a-q*b for a,b in zip(A[i],A[row])]
  pivots.append(col);row+=1
  if row==4:break
 free=next(j for j in range(n) if j not in pivots)
 c=[F(0)]*n;c[free]=F(1)
 for i,j in enumerate(pivots):c[j]=-A[i][free]
 D=lcm(*(x.denominator for x in c));ci=[int(x*D) for x in c]
 g=gcd(*ci);ci=[x//g for x in ci]
 assert all(sum(ci[j]*columns[j][i] for j in range(n))==0 for i in range(4))
 return ci

def split(columns,weights):
 active=[j for j,w in enumerate(weights) if w and any(columns[j])]
 if len(active)<=4:return None
 chosen=active[:5];d=dependence([columns[j] for j in chosen]);c=[0]*len(columns)
 for j,x in zip(chosen,d):c[j]=x
 plus=min(weights[j]/c[j] for j in active if c[j]>0)
 minus=max(weights[j]/c[j] for j in active if c[j]<0)
 p=-minus/(plus-minus)
 endpoints=[[w-t*x for w,x in zip(weights,c)] for t in [plus,minus]]
 assert 0<p<1 and all(w>=0 for end in endpoints for w in end)
 return p,endpoints,c

def draw_below(d,rng,cap=128):
 assert d>0;b=(d-1).bit_length()
 for j in range(cap):
  x=rng.getrandbits(b)
  if x<d:return x,False,(j+1)*b
 return 0,True,cap*b

def compact_default(known,effects,A,rng,cap=128):
 K=A-len(known)
 if not K:return list(known),effects,{'cap_failures':0,'bits':0,'draws':0}
 z,failed,bits=draw_below(K,rng,cap)
 for a in sorted(known):
  if a<=z:z+=1
  else:break
 assert 0<=z<A and z not in known
 return list(known)+[z],effects,{'cap_failures':int(failed),'bits':bits,'draws':1}

def prune(labels,columns,rng,cap=128):
 w=[F(1) if any(c) else F(0) for c in columns];stats={'cap_failures':0,'bits':0,'draws':0,'max_null_integer_bits':0}
 while True:
  branch=split(columns,w)
  if branch is None:break
  p,ends,c=branch;u,failed,bits=draw_below(p.denominator,rng,cap)
  choice=0 if u<p.numerator else 1
  w=ends[choice];stats['cap_failures']+=failed;stats['bits']+=bits;stats['draws']+=1
  stats['max_null_integer_bits']=max(stats['max_null_integer_bits'],max(abs(x).bit_length() for x in c))
 out=[(label,scale(weight,col)) for label,col,weight in zip(labels,columns,w) if weight and any(col)]
 assert len(out)<=4 and all(psd_exact(e) for _,e in out)
 assert [sum(e[j] for _,e in out) for j in range(4)]==[1,0,0,0]
 return out,stats

def enumerate_exact(columns,weights=None,prob=F(1)):
 """Small-instance validator only, NOT the operational algorithm."""
 if weights is None:weights=[F(1) if any(c) else F(0) for c in columns]
 branch=split(columns,weights)
 if branch is None:
  yield prob,weights;return
 p,ends,c=branch
 yield from enumerate_exact(columns,ends[0],prob*p)
 yield from enumerate_exact(columns,ends[1],prob*(1-p))
