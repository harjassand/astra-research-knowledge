#!/usr/bin/env python3
"""Local connected ladder realization of symmetry-filtered embedded two-hardcore-memory eigenstate.
Two parallel semi-infinite legs, onsite 3, rung +2, intra-leg hopping -1/2.
Two memories each couple locally to both sites of first rung through nonnegative real hoppings.
All computations are finite-volume consistency checks of an analytically reducible infinite ladder.
"""
import numpy as np, math, json, sys
from scipy.linalg import eigh
sys.path.insert(0,'/mnt/data')
from astra_symmetry_filtered_CZ_protocol import build_two
from astra_symmetry_filtered_embedded_pair import evaluate

def build_ladder(n,g):
    d=2+2*n
    mat=np.diag(np.r_[3.,3.,np.full(2*n,3.)])
    t=(math.sqrt(2)+1)*g/2
    s=(math.sqrt(2)-1)*g/2
    a,b=2,2+n
    mat[0,a]=mat[a,0]=t;mat[1,b]=mat[b,1]=t
    mat[0,b]=mat[b,0]=s;mat[1,a]=mat[a,1]=s
    for j in range(n):
        mat[a+j,b+j]=mat[b+j,a+j]=2.
    for j in range(n-1):
        mat[a+j,a+j+1]=mat[a+j+1,a+j]=-.5
        mat[b+j,b+j+1]=mat[b+j+1,b+j]=-.5
    return mat

def build_two_general(mat):
    n=len(mat)
    basis=[(i,j) for i in range(n) for j in range(i,n) if (i,j) not in [(0,0),(1,1)]]
    lookup={a:i for i,a in enumerate(basis)}
    res=np.zeros((len(basis),len(basis)))
    for idx,(i,j) in enumerate(basis):
        res[idx,idx]=mat[i,i]+mat[j,j]
        if i==j:
            for k in range(n):
                if k==i or abs(mat[k,i])<1e-14:continue
                res[lookup[tuple(sorted((i,k)))],idx]+=math.sqrt(2)*mat[k,i]
        else:
            for site,other in ((i,j),(j,i)):
                for k in range(n):
                    if k==site or abs(mat[k,site])<1e-14:continue
                    to=tuple(sorted((k,other)))
                    if to in lookup:res[lookup[to],idx]+=(math.sqrt(2) if k==other else 1)*mat[k,site]
    assert np.linalg.norm(res-res.T)<1e-12
    return res,basis

def check(g=.2,n=8):
    h=build_ladder(n,g)
    h2,basis=build_two_general(h)
    one,Evec=eigh(h)
    spec=evaluate(g,n)
    D,V=eigh(h2)
    p=np.zeros(len(basis));p[basis.index((0,1))]=1
    overlaps=(V.T@p)**2
    idx=np.argmax(overlaps)
    assert abs(D[idx]-spec['pole'])<1e-10
    perm=np.r_[1,0,np.arange(2+n,2+2*n),np.arange(2,2+n)]
    S=np.zeros_like(h2)
    ii={q:k for k,q in enumerate(basis)}
    for idx2,(i,j) in enumerate(basis):S[ii[tuple(sorted((perm[i],perm[j])))],idx2]=1
    assert np.linalg.norm(S@h2-h2@S)<1e-10
    sym_eval=np.sum(V[:,idx]*(S@V[:,idx]))
    assert sym_eval>.9999999
    result=dict(n=n,g=g,total_two_particle_dimension=len(basis),
      all_hoppings_real=True,minimum_offdiag_port_coupling=float((math.sqrt(2)-1)*g/2),
      max_offdiag_port_coupling=float((math.sqrt(2)+1)*g/2),
      pair_energy_from_full_ladder=float(D[idx]),pair_energy_from_parity_resolvent=spec['pole'],
      pair_overlap_from_full_ladder=float(overlaps[idx]),pair_residue=spec['bare_pair_overlap_squared'],
      exact_symmetry_commutator=float(np.linalg.norm(S@h2-h2@S)),
      parity_of_pair=float(sym_eval),onebody_min=float(np.min(one)),
      two_particle_min=float(np.min(D)),
      protected_even_gap=spec['isolated_pair_gap'])
    return result
if __name__=='__main__':
    r=[check(g,n=8) for g in (.1,.2,.4)]
    with open('/mnt/data/astra_local_ladder_embedded_pair_audit_results.json','w') as f:json.dump(r,f,indent=2)
    print(json.dumps(r,indent=2))
