#!/usr/bin/env python3
"""Finite algebra and geometric regressions; not a semantic threshold proof."""
import numpy as np,json,heapq
from scipy.linalg import expm
# Read qubit R, copied hub qubit C, write qubit W. All indices R,C,W.
I=np.eye(2); X=np.array([[0,1],[1,0]],complex); H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2)
P=[np.diag([1,0]),np.diag([0,1])]
Ucopy=sum(np.kron(np.kron(P[a],np.linalg.matrix_power(X,a)),I) for a in range(2))
Uwrite=sum(np.kron(np.kron(I,P[a]),np.linalg.matrix_power(X,a)) for a in range(2))
Uclean=Uwrite@Ucopy
Udirty=Uwrite@np.kron(np.kron(I,H),I)@Ucopy
# Input space R,W embeds C=0. Trace C using separately resolved terminal Kraus.
def ks(U):
 return [np.array([[U[(r*2+c)*2+w,(rr*2+0)*2+ww] for rr in range(2) for ww in range(2)] for r in range(2) for w in range(2)]) for c in range(2)]
def ch(K,O): return sum(k@O@k.conj().T for k in K)
def adj(K,O): return sum(k.conj().T@O@k for k in K)
Kc,Kd=ks(Uclean),ks(Udirty)
pop=max(np.linalg.norm(adj(Kd,np.kron(p,I))-np.kron(p,I)) for p in P)
plus=np.array([1,1],complex)/np.sqrt(2); zero=np.array([1,0],complex)
v=np.kron(plus,zero); rho=np.outer(v,v.conj())
clean=ch(Kc,rho); dirty=ch(Kd,rho)
# Off diagonal read block confirms we do not claim dirty pinching/identity.
# Geometry: a frozen cross; the center's inconsistent value is inaccessible.
a=1; R=6; L=10
V={(x,y) for x in range(-L,L+1) for y in range(-L,L+1)}
F={(0,0),(1,0),(-1,0),(0,1),(0,-1)}
c={p:sum(p) for p in F}; c[0,0]=25
C=V-F
nb=lambda p:[(p[0]+dx,p[1]+dy) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]]
u={p:10**9 for p in C}; heap=[]
for f in F:
 for p in nb(f):
  if p in C and c[f]+1<u[p]:u[p]=c[f]+1;heapq.heappush(heap,(u[p],p))
while heap:
 d,p=heapq.heappop(heap)
 if d!=u[p]:continue
 for z in nb(p):
  if z in C and d+1<u[z]:u[z]=d+1;heapq.heappush(heap,(d+1,z))
h={p:sum(p) for p in C}; initial_deficit=sum(u[p]-h[p] for p in C)
updates=0;sweeps=0
while any(h[p]<u[p] for p in C):
 changed=0
 for p in sorted(C):
  vals=[h[z] if z in C else c[z] for z in nb(p) if z in V]
  if h[p]<u[p] and all(h[p]<=v for v in vals):h[p]+=1;updates+=1;changed+=1
 assert changed>0
 sweeps+=1
S=[p for p in C if abs(p[0])+abs(p[1])==R]
violation=max(abs(u[p]-u[z])-abs(p[0]-z[0])-abs(p[1]-z[1]) for p in S for z in S)
ball={p for p in V if abs(p[0])+abs(p[1])<=R}
ext={p:min(u[z]+abs(p[0]-z[0])+abs(p[1]-z[1]) for z in S) for p in ball}
edge_violation=max(abs(ext[p]-ext[z])-1 for p in ball for z in nb(p) if z in ball)
report={'scope':'Finite algebra/geometry diagnostics only', 'read_only':{'dirty_population_projector_error':float(pop),'clean_read_cross_block_norm':float(np.linalg.norm(clean[:2,2:])),'dirty_read_cross_block_norm_nonzero_expected':float(np.linalg.norm(dirty[:2,2:]))},'height':{'sites':len(V),'frozen':len(F),'inaccessible_center_value':25,'accessible_height_range':2,'R':R,'initial_total_deficit':initial_deficit,'legal_increments':updates,'sweeps':sweeps,'sphere_Lipschitz_violation':violation,'extension_edge_violation':edge_violation,'extension_matches_sphere':all(ext[p]==u[p] for p in S)}}
assert pop<1e-12 and np.linalg.norm(clean[:2,2:])<1e-12
assert updates==initial_deficit and violation<=0 and edge_violation<=0
print(json.dumps(report,indent=2))
