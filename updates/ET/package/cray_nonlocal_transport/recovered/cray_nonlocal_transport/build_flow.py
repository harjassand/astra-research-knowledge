"""Construct a rational legal source--sink module on a 6x3 KA rectangle.
Numeric solves propose flows; an integer spanning-tree repair makes divergence exact.
"""
from pathlib import Path
import time,json
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import LinearOperator,cg
from scipy.sparse.csgraph import connected_components
ROOT=Path(__file__).parent
start=time.perf_counter();N=1<<18;w=6;h=3
sites=[(x,y) for y in range(h) for x in range(w)]; ix={z:i for i,z in enumerate(sites)}
phys=[(ix[(x,y)],ix[(x+dx,y+dy)]) for x,y in sites for dx,dy in [(1,0),(0,1)] if (x+dx,y+dy)in ix]
nb={i:[ix[(x+dx,y+dy)] for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)] if (x+dx,y+dy)in ix] for i,(x,y)in enumerate(sites)}
s=np.arange(N,dtype=np.int32); us=[];vs=[];bids=[]
for j,(a,b) in enumerate(phys):
 t=s^(1<<a)^(1<<b)
 mask=(s<t)&(((s>>a)^(s>>b))&1).astype(bool)
 for z,other in [(a,b),(b,a)]:
  envmask=sum(1<<v for v in nb[z] if v!=other)
  mask &= ((s&envmask)!=envmask)
 u=s[mask];us.append(u);vs.append(t[mask]);bids.append(np.full(len(u),j,dtype=np.int8))
u=np.concatenate(us);v=np.concatenate(vs);bid=np.concatenate(bids);E=len(u)
adj=coo_matrix((np.r_[np.arange(E)+1,np.arange(E)+1],(np.r_[u,v],np.r_[v,u])),shape=(N,N)).tocsr()
ncomp,comp=connected_components(adj,directed=False);sizes=np.bincount(comp)
# integer demand d = (port_left-port_right) * good(left reservoir)*good(right reservoir)
# Five forbidden fully occupied sets: four outer sides and the four
# nearest neighbors of the port. This gate is independent of port occupation.
gate=[pattern for pattern in range(256) if all((pattern & mask)!=mask for mask in (7,41,90,148,224))]
allowed=np.zeros(256,bool);allowed[gate]=True
off=[(x,y)for y in range(-1,2)for x in range(-1,2)if(x,y)!=(0,0)]
a=ix[(1,1)];b=ix[(4,1)]
la=sum(((s>>ix[(x+1,y+1)])&1)<<j for j,(x,y)in enumerate(off))
ra=sum(((s>>ix[(x+4,y+1)])&1)<<j for j,(x,y)in enumerate(off))
d=((((s>>a)&1)-((s>>b)&1))*allowed[la]*allowed[ra]).astype(np.int64)
assert np.all(np.bincount(comp,weights=d)==0)
# A microscopic bond is shared by four modules within a block, and one
# module if it crosses the boundary. Optimize the actual assembly majorant.
overlap=np.array([1 if (sites[a][0]==2 and sites[b][0]==3) else 4 for a,b in phys],dtype=np.int8)
cost=overlap[bid]; conductance=1.0/cost
deg=np.bincount(np.r_[u,v],weights=np.r_[conductance,conductance],minlength=N).astype(float)
L=coo_matrix((np.r_[-conductance,-conductance,deg],(np.r_[u,v,s],np.r_[v,u,s])),shape=(N,N)).tocsr()
def pmean(x):return np.bincount(comp,weights=x,minlength=ncomp)[comp]/sizes[comp]
def mv(x):return L@x+pmean(x)
def pre(x):
 y=x/np.maximum(deg,1)
 return y-pmean(y)+pmean(x)
A=LinearOperator((N,N),matvec=mv,dtype=float)
M=LinearOperator((N,N),matvec=pre,dtype=float)
it=[0]
def cb(x):it[0]+=1
pot,info=cg(A,d.astype(float),M=M,rtol=2e-11,atol=0,maxiter=3000,callback=cb)
print('solve',info,'iterations',it[0],'edges',E,'residual',float(np.max(abs(L@pot-d))),flush=True)
# build deterministic spanning forest from adjacency, with edge labels
parent=np.full(N,-1,np.int32); pedge=np.full(N,-1,np.int32); order=[]
for root in range(N):
 if parent[root]>=0:continue
 parent[root]=root;queue=[root]
 for x in queue:
  for pos in range(adj.indptr[x],adj.indptr[x+1]):
   y=int(adj.indices[pos])
   if parent[y]<0:parent[y]=x;pedge[y]=int(adj.data[pos])-1;queue.append(y)
 order.extend(queue)
D=1<<40
flow=np.rint(conductance*(pot[u]-pot[v])*D).astype(np.int64)
r=d*D
np.add.at(r,u,-flow);np.add.at(r,v,flow)
maxinitial=int(np.max(abs(r)))
for x in reversed(order):
 y=int(parent[x])
 if y==x:assert r[x]==0;continue
 e=int(pedge[x]);delta=int(r[x])
 flow[e]+=delta if int(u[e])==x else -delta
 r[y]+=delta;r[x]=0
r=d*D;np.add.at(r,u,-flow);np.add.at(r,v,flow)
assert not np.any(r)
counts=np.array([int(x).bit_count() for x in u],dtype=np.int8)
energy=[0]*19; weighted_energy=[0]*19
for n,f,c in zip(counts,flow,cost):
 energy[int(n)]+=int(f)**2
 weighted_energy[int(n)]+=int(c)*int(f)**2
np.savez_compressed(ROOT/'module_flow.npz',u=u,v=v,bond=bid,flow=flow)
meta={'width':w,'height':h,'ports':[a,b],'gate_offsets':off,'gate_allowed':gate,'denominator':D,'energy_squares_by_particle_count':[str(x)for x in energy],
      'weighted_energy_squares_by_particle_count':[str(x) for x in weighted_energy], 'overlap_by_bond':overlap.tolist(), 'physical_bonds':phys,
      'states':N,'configuration_edges':E,'components':ncomp,'nonzero_demands':int(np.count_nonzero(d)),'cg_status':int(info),'cg_iterations':it[0],
      'max_rounding_residual_numerator':maxinitial,'max_flow':float(np.max(abs(flow)))/D,'wall_seconds':time.perf_counter()-start}
(ROOT/'module_metadata.json').write_text(json.dumps(meta,indent=2))
print(json.dumps({k:v for k,v in meta.items()if k not in ['gate_allowed','energy_squares_by_particle_count','weighted_energy_squares_by_particle_count','physical_bonds','overlap_by_bond']},indent=2))
