"""Exact spatial resolvent certificate for mean proposal walk length.
The finite torus is only an auxiliary upper bound, not a physical cutoff.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,time,json,numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(ROOT/'square_aklt_observable_join_20261105'))
from local_birth_oracle import LocalLoopBirthSampler,D
from open_trail_sampler import OpenTrailSampler
s=LocalLoopBirthSampler(0);n=len(s.states);L=s.side;g=s.g
z=np.load(ROOT/'square_aklt_loop_audit_20261105/trail_certificate_m6.npz');v=z['v'];V=np.tile(v,4)
xx,yy=np.indices((L,L));ix=np.zeros((4*n,3,L,L),dtype=np.int64);w=np.zeros((4*n,3),dtype=np.int64)
for o in range(4):
 for i,h in enumerate(s.states):
  row=o*n+i
  for j,d in enumerate(s.directions[i]):
   dx,dy=D[(d+o)%4];target=((o+h[1])%4)*n+int(s.to[i,j])
   ix[row,j]=target*L*L+((xx+dx)%L)*L+(yy+dy)%L;w[row,j]=s.w[i,j]
def apply(H):return (w[:,:,None,None]*H.reshape(-1)[ix]).sum(1)
# Choose an integer multiple of lifted Collatz V large enough for H>=g+QH.
slack=15*V-(w*V[(ix[:,:,0,0]//(L*L))]).sum(1)
assert min(slack)>0
C=max((15*int(g[i].max())+int(slack[i])-1)//int(slack[i]) for i in range(4*n))
H=np.broadcast_to(C*V[:,None,None],g.shape).copy();assert np.all(15*H>=15*g+apply(H))
start=time.monotonic()
for _ in range(500):
 nxt=(15*g+apply(H)+14)//15
 assert np.all(nxt<=H);H=nxt
assert np.all(15*H>=15*g+apply(H))
np.savez_compressed(HERE/'oracle_work_resolvent_m6_L16.npz',H=H)
R=max(r for _,h,r in s.options);num=F(0)
for i,h,r in s.options:
 b=3**(s.m-len(h)+r)*5**(R-r)
 if i<0:num+=b*s.scale*len(h)
 else:
  x=y=0
  for d in h:x+=D[d][0];y+=D[d][1]
  q=int(g[i,x%L,y%L]);hh=int(H[i,x%L,y%L])
  num+=b*(len(h)*q+hh-q)
loopE=num/s.total
p=OpenTrailSampler(0,target=(1,0));R=max(r for o,i,h,r in p.options);num=F(0)
for o,i,h,r in p.options:
 b=3**(p.m-len(h)+r)*5**(R-r)
 if i<0:num+=b*p.scale*len(h)
 else:
  x=y=0
  for d in h:x+=D[(d+o)%4][0];y+=D[(d+o)%4][1]
  x=(x-p.target[0])%L;y=(y-p.target[1])%L
  q=int(g[o*n+i,x,y]);hh=int(H[o*n+i,x,y]);num+=b*(len(h)*q+hh-q)
pathE=num/p.total
out={'iterations':500,'elapsed_seconds':time.monotonic()-start,'initial_integer_C':int(C),
 'loop_oracle_expected_walk_steps_upper':str(loopE),'loop_oracle_expected_walk_steps_decimal':float(loopE),
 'nearest_neighbor_path_expected_walk_steps_upper':str(pathE),'nearest_neighbor_path_expected_walk_steps_decimal':float(pathE),
 'query_loop_walk_steps_per_vertex_using_14_120548_calls':str(loopE*F(14120548,1000000)),
 'physical_attempt_expected_local_calls_upper':str((pathE+1)*F(14120548,1000000)),
 'scope':'Exact integer H>=g+QH verifies a walk-step expectation upper bound, including all rejected proposals. Finite matrices are proposal majorants, never physical length or space cutoffs. Does not assert wall-time or small bit complexity.'}
(HERE/'oracle_work_sharp_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
