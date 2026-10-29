"""Exact two-site leased Kraus update regression on edges 0->1->2."""
import numpy as np
from functools import reduce
from itertools import product
kron=lambda xs:reduce(np.kron,xs)
edges=[(0,1),(1,2)];m=2
labels=[['R','C0:1','C0:2','D0','T0'],['R','P0','C1:1','C1:2','D1','T1'],['R','P1']]
abstract=[['R','C0','D0','T0'],['R','P0','C1','D1','T1'],['R','P1']]
dims=[len(l) for l in labels];dc=np.prod(dims);dd=8
amp=[np.diag([1,np.sqrt(.7)]),np.array([[0,np.sqrt(.3)],[0,0]])]
CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
Ks=[[np.kron(a,np.eye(4)) for a in amp],[np.kron(np.eye(2),CNOT@np.kron(np.eye(2),a)) for a in amp]]
def cm(acts):
    return kron([np.outer(np.eye(dims[i])[:,labels[i].index(acts[i][0])],np.eye(dims[i])[:,labels[i].index(acts[i][1])]) if i in acts else np.eye(dims[i]) for i in range(3)])
def transition(c,e,typ):
    a,b=edges[e];c=list(c)
    if typ=='start' and (c[a],c[b])==('R','R'):c[a],c[b]=f'C{e}',f'P{e}'
    elif typ=='unstart' and (c[a],c[b])==(f'C{e}',f'P{e}'):c[a],c[b]='R','R'
    elif typ=='emit' and c[a]==f'C{e}':c[a]=f'D{e}'
    elif typ=='release' and (c[a],c[b])==(f'D{e}',f'P{e}'):c[a],c[b]=f'T{e}','R'
    elif typ=='unrelease' and (c[a],c[b])==(f'T{e}','R'):c[a],c[b]=f'D{e}',f'P{e}'
    elif typ=='final' and c[a]==f'T{e}':c[a]='R'
    else:return None
    return tuple(c)
configs=[('R','R','R')]
for c in configs:
 for e in range(2):
  for typ in ['start','unstart','emit','release','unrelease','final']:
   out=transition(c,e,typ)
   if out is not None and out not in configs:configs.append(out)
nc=len(configs);W=np.zeros((dd*dc,dd*nc))
for j,c in enumerate(configs):
    pending=[e for e,(a,b) in enumerate(edges) if c[a]==f'C{e}']
    for ss in product([1,2],repeat=len(pending)):
        out=list(c);K=np.eye(dd)
        for e,s in zip(pending,ss):out[edges[e][0]]=f'C{e}:{s}';K=Ks[e][s-1]@K
        v=kron([np.eye(dims[i])[:,labels[i].index(out[i])] for i in range(3)])
        for d in range(dd):W[:,d*nc+j]+=np.kron(K[:,d],v)
H=np.zeros((dd*dc,dd*dc));Hc=np.zeros((nc,nc));jumps=[]
for e,(a,b) in enumerate(edges):
    A=sum(np.kron(Ks[e][s-1],cm({a:(f'C{e}:{s}','R'),b:(f'P{e}','R')})) for s in [1,2])
    B=np.kron(np.eye(dd),cm({a:(f'T{e}',f'D{e}'),b:('R',f'P{e}')}))
    H+=A+A.T+B+B.T
    for j,c in enumerate(configs):
     for typ in ['start','unstart','release','unrelease']:
      out=transition(c,e,typ)
      if out is not None:Hc[configs.index(out),j]+=1
    for s in [1,2]:
        L=np.kron(np.eye(dd),cm({a:(f'D{e}',f'C{e}:{s}')}))
        bc=np.zeros((nc,nc))
        for j,c in enumerate(configs):
            out=transition(c,e,'emit')
            if out is not None:bc[configs.index(out),j]=1
        jumps.append((L,np.kron(Ks[e][s-1],bc)))
    L=np.kron(np.eye(dd),cm({a:('R',f'T{e}')}));bc=np.zeros((nc,nc))
    for j,c in enumerate(configs):
        out=transition(c,e,'final')
        if out is not None:bc[configs.index(out),j]=1
    jumps.append((L,np.kron(np.eye(dd),bc)))
res={'legal_clock_configs':nc,'physical_dimension':dd*dc,'isometry':float(np.linalg.norm(W.T@W-np.eye(dd*nc))),
'H_intertwiner':float(np.linalg.norm(H@W-W@np.kron(np.eye(dd),Hc))),
'jump_intertwiners':[float(np.linalg.norm(L@W-W@Lsmall)) for L,Lsmall in jumps]}
assert res['isometry']<1e-12 and res['H_intertwiner']<1e-12 and max(res['jump_intertwiners'])<1e-12
print(res)
