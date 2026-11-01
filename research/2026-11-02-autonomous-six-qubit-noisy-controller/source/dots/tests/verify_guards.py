#!/usr/bin/env python3
"""Exhaustive combinatorial audit; no quantum hardware simulation."""
import itertools,json

def inv(x): return sum((1-x[i])*x[j] for i in range(len(x)) for j in range(i+1,len(x)))
def steps(c,b):
 x=tuple(z^b for z in c); M=len(c); out=[]
 for j in range(M):
  left=1 if j==0 else x[j-1]; right=0 if j==M-1 else x[j+1]
  if (left,x[j],right)==(1,0,0):
   d=list(c); d[j]^=1; out.append(('wall',j+1,tuple(d),b))
 if x[-1]==1: out.append(('mode',None,c,1-b))
 return out
rows=[]
for M in range(1,13):
 states=legal=invalid=sorts=0; max_inc=0; max_mode_inc=0; max_bad_enabled=0; ratio=0
 for b in (0,1):
  for c in itertools.product((0,1),repeat=M):
   states+=1;x=tuple(z^b for z in c);r=sum(x);I=inv(x); st=steps(c,b)
   valid=I==0
   assert valid==(x==(1,)*r+(0,)*(M-r))
   if valid:
    legal+=1;assert len(st)==1
    typ,j,d,bp=st[0];xp=tuple(z^bp for z in d)
    if r<M: assert typ=='wall' and j==r+1 and bp==b and sum(xp)==r+1
    else: assert typ=='mode' and bp==1-b and sum(xp)==0
    assert inv(xp)==0
   else:
    invalid+=1;max_bad_enabled=max(max_bad_enabled,len(st))
   N01=sum(x[i:i+2]==(0,1) for i in range(M-1))
   assert N01>0 if I else N01==0
   assert I<=max(1,M*M//4)*N01
   if N01:ratio=max(ratio,I/N01)
   for i in range(M-1):
    if x[i:i+2]==(0,1):
     d=list(c);d[i],d[i+1]=d[i+1],d[i];xp=tuple(z^b for z in d)
     assert sum(xp)==r and inv(xp)==I-1;sorts+=1
   for typ,j,d,bp in st:
    xp=tuple(z^bp for z in d); delta=inv(xp)-I
    if typ=='wall':
     assert sum(xp)==r+1 and bp==b
     assert abs(delta)<=M-1;max_inc=max(max_inc,delta)
    else:
     assert sum(xp)==M-r
     assert delta==r*(M-r)-2*I
     assert abs(delta)<=M*M//4;max_mode_inc=max(max_mode_inc,delta)
    if delta>0:assert I>0
   # Each separately labelled source-to-target map is injective, including mode direction.
 for label in [('wall',j,b) for j in range(1,M+1) for b in (0,1)]+[('mode',None,b) for b in (0,1)]:
  seen=set()
  for c in itertools.product((0,1),repeat=M):
   for typ,j,d,bp in steps(c,label[2]):
    if (typ,j)==label[:2]:
     target=(d,bp);assert target not in seen;seen.add(target)
 assert legal==2*(M+1)
 rows.append(dict(M=M,states=states,legal=legal,invalid=invalid,sorting_edges=sorts,max_positive_wall_delta=max_inc,max_positive_mode_delta=max_mode_inc,max_invalid_enabled=max_bad_enabled,max_I_over_N01=ratio))
print(json.dumps(dict(status='PASS',rows=rows),indent=2))
