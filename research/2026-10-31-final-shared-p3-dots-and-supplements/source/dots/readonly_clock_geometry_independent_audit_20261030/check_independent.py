"""Independent nondemolition and finite-graph/sphere checks; not native dynamics."""
import numpy as np, heapq, json, random
rng=np.random.default_rng(4123); rr=random.Random(4123)
# 3-level read, copy, and writable register. Forward copies are unchanged controls.
q=3; I=np.eye(q); P=[np.diag([int(a==b) for b in range(q)]) for a in range(q)]
X=np.roll(I,1,axis=0)
copy=sum(np.kron(np.kron(P[a],np.linalg.matrix_power(X,a)),I) for a in range(q))
write=sum(np.kron(np.kron(I,P[a]),np.linalg.matrix_power(X,a)) for a in range(q))
z=rng.normal(size=(q,q))+1j*rng.normal(size=(q,q)); fault,_=np.linalg.qr(z)
dirty=write@np.kron(np.kron(I,fault),I)@copy
clean=write@copy
# Embed copy=0; trace copy at terminal.
def kraus(U):
 return [np.array([[U[(a*q+c)*q+w,(aa*q+0)*q+ww] for aa in range(q) for ww in range(q)] for a in range(q) for w in range(q)]) for c in range(q)]
K=kraus(dirty)
comm=max(np.linalg.norm(k@np.kron(p,I)-np.kron(p,I)@k) for k in K for p in P)
pop=max(np.linalg.norm(sum(k.conj().T@np.kron(p,I)@k for k in K)-np.kron(p,I)) for p in P)
# A selected copy=0 branch has a nonidentity effect even though it preserves labels.
branch_effect=K[0].conj().T@K[0]
branch_nonidentity=float(np.linalg.norm(branch_effect-np.eye(q*q)))
assert comm<1e-12 and pop<1e-12 and branch_nonidentity>.1
# Clean copy retained until reset kills every read off-diagonal block.
plus=np.ones(q)/np.sqrt(q); zero=I[:,0]; v=np.kron(plus,zero);rho=np.outer(v,v)
out=sum(k@rho@k.conj().T for k in kraus(clean))
clean_cross=max(np.linalg.norm(out[a*q:(a+1)*q,b*q:(b+1)*q]) for a in range(q) for b in range(q) if a!=b)
# If the last copy is transferred to W, terminal reset fails to pinch jointly.
swap=np.zeros((q*q,q*q))
for a in range(q):
 for b in range(q):swap[b*q+a,a*q+b]=1
badcopy=np.kron(I,swap)@copy
outbad=sum(k@rho@k.conj().T for k in kraus(badcopy))
bad_cross=max(np.linalg.norm(outbad[a*q:(a+1)*q,b*q:(b+1)*q]) for a in range(q) for b in range(q) if a!=b)
assert clean_cross<1e-12 and bad_cross>.3

# Random connected finite graphs with known feasible initial heights.
def distances(adj,start):
 d={start:0};todo=[start]
 for x in todo:
  for y in adj[x]:
   if y not in d:d[y]=d[x]+1;todo.append(y)
 return d
n_cases=150; total_updates=0;max_updates=0
for _ in range(n_cases):
 n=rr.randrange(3,18);adj={i:set() for i in range(n)}
 for i in range(1,n):
  j=rr.randrange(i);adj[i].add(j);adj[j].add(i)
 for i in range(n):
  for j in range(i):
   if rr.random()<.12:adj[i].add(j);adj[j].add(i)
 h0=distances(adj,rr.randrange(n));h={x:rr.choice([-1,1])*0+h0[x] for x in range(n)}
 F=set(rr.sample(range(n),rr.randrange(1,n)));C=set(range(n))-F;c={f:h[f] for f in F}
 # All C components meet F because the full graph is connected.
 u={x:10**8 for x in C}; heap=[]
 for f in F:
  for x in adj[f]&C:
   if c[f]+1<u[x]:u[x]=c[f]+1;heapq.heappush(heap,(u[x],x))
 while heap:
  d,x=heapq.heappop(heap)
  if d!=u[x]:continue
  for y in adj[x]&C:
   if d+1<u[y]:u[y]=d+1;heapq.heappush(heap,(d+1,y))
 deficit=sum(u[x]-h[x] for x in C);updates=0
 while any(h[x]<u[x] for x in C):
  elig=[x for x in C if h[x]<u[x] and all(h[x]<=h[y] for y in adj[x])]
  assert elig
  x=rr.choice(elig);h[x]+=1;updates+=1
  assert all(abs(h[i]-h[j])<=1 for i in C for j in adj[i])
 assert updates==deficit and all(h[x]==u[x] for x in C)
 total_updates+=updates;max_updates=max(max_updates,updates)

# Punctured Z^2 exterior. u is computed by a multi-source shortest-path fill.
nb=lambda p: [(p[0]+1,p[1]),(p[0]-1,p[1]),(p[0],p[1]+1),(p[0],p[1]-1)]
n_sphere=24;max_sphere=0;max_ext=0
for case in range(n_sphere):
 a=rr.randrange(1,4);balla=[(x,y) for x in range(-a,a+1) for y in range(-a,a+1) if abs(x)+abs(y)<=a]
 F=set(rr.sample(balla,rr.randrange(1,len(balla)+1)))
 # Frozen values from a globally 1-Lipschitz field; values inside F need not
 # participate when inaccessible from the unbounded component.
 cv={p:p[0] for p in F};D=max(cv.values())-min(cv.values());R=D+3*a+1;L=R+2*a+3
 V={(x,y) for x in range(-L,L+1) for y in range(-L,L+1)}
 C={(L,L)};todo=[(L,L)]
 for x in todo:
  for y in nb(x):
   if y in V and y not in F and y not in C:C.add(y);todo.append(y)
 u={x:10**8 for x in C};heap=[]
 for f in F:
  for x in nb(f):
   if x in C and cv[f]+1<u[x]:u[x]=cv[f]+1;heapq.heappush(heap,(u[x],x))
 while heap:
  d,x=heapq.heappop(heap)
  if d!=u[x]:continue
  for y in nb(x):
   if y in C and d+1<u[y]:u[y]=d+1;heapq.heappush(heap,(d+1,y))
 S=[(x,y) for x,y in C if abs(x)+abs(y)==R]
 l1=lambda x,y:abs(x[0]-y[0])+abs(x[1]-y[1])
 vio=max(abs(u[x]-u[y])-l1(x,y) for x in S for y in S)
 assert vio<=0;max_sphere=max(max_sphere,vio)
 B={(x,y) for x,y in V if abs(x)+abs(y)<=R}
 U={z:min(u[x]+l1(x,z) for x in S) for z in B}
 assert all(U[x]==u[x] for x in S)
 e=max(abs(U[x]-U[y])-1 for x in B for y in nb(x) if y in B)
 assert e<=0;max_ext=max(max_ext,e)

print(json.dumps({'scope':'Finite algebra and geometry only; no physical service, root range, or DATA cut.',
 'read_q':q,'read_sector_commutator':float(comm),'CPTP_population_error':float(pop),
 'selected_branch_nonidentity_effect':branch_nonidentity,'clean_cross_block':float(clean_cross),
 'lost_copy_counterexample_cross_block':float(bad_cross),
 'finite_graph_cases':n_cases,'legal_increments':total_updates,'maximum_case_increments':max_updates,
 'exterior_sphere_cases':n_sphere,'sphere_Lipschitz_violation':max_sphere,'extension_edge_violation':max_ext},indent=2))
