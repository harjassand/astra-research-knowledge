"""Exact branch/support checks and a small-code refined-channel identity."""
import itertools, sympy as S
# Union of four-dimensional plaquettes incident to the eight edges at the origin.
origin=(0,)*4; incidences={}
for d in range(4):
 for sign in (-1,1):
  edge=list(origin)
  if sign==-1:edge[d]-=1
  for e in range(4):
   if e==d:continue
   for offset in (0,-1):
    anchor=edge.copy();anchor[e]+=offset
    face=(tuple(anchor),tuple(sorted((d,e))))
    incidences[face]=incidences.get(face,0)+1
assert len(incidences)==24 and set(incidences.values())=={2}
active=[];inactive=[]
for bits in itertools.product((0,1),repeat=8):
 incoming,outgoing=bits[:4],bits[4:]
 isactive=not any(incoming) and sum(outgoing) in (2,4)
 (active if isactive else inactive).append(bits)
assert len(active)==7 and len(inactive)==249
assert sum(sum(bits)%2==0 for bits in inactive)==121
# Two stabilized qubits and one untouched logical qubit.
I=S.eye(2);X=S.Matrix([[0,1],[1,0]]);p=[S.diag(1,0),S.diag(0,1)];k=S.kronecker_product
R={(a,b):k(p[a],p[b],I) for a,b in itertools.product(range(2),repeat=2)}
Q=k(X,X,I);Pactive=R[1,1];P0=S.eye(8)-Pactive
coarse=[P0,Q*Pactive]
refined=[(Q if key==(1,1) else S.eye(8))*r for key,r in R.items()]
def channel(Ks,A):return sum((K*A*K.H for K in Ks),S.zeros(8))
for i,j in itertools.product(range(8),repeat=2):
 A=S.zeros(8);A[i,j]=1
 assert channel(refined,A)==channel(coarse,channel(list(R.values()),A))
# Equality on each full-syndrome logical orbit, including logical coherences.
for a,b,i,j in itertools.product(range(2),repeat=4):
 A=S.zeros(8);A[4*a+2*b+i,4*a+2*b+j]=1
 assert channel(refined,A)==channel(coarse,A)
# Genuine full-input difference within the inactive aggregate.
A=S.zeros(8);A[2,4]=1
assert channel(coarse,A)==A and channel(refined,A)==S.zeros(8)
assert sum((K.H*K for K in refined),S.zeros(8))==S.eye(8)
print('PASS: 24-plaquette decision-check union; all pattern branches including inactive aggregate; exact C_ref=C D; all orbit logical matrix units; explicit coherence difference.')
