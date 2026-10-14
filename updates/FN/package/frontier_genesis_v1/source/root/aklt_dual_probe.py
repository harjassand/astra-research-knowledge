"""Independent root probe of an exactly feasible local quantum-response dual.

Explicit AKLT MPS supplies ground state; dense arrays are validation only.
Core Thomson/Hylleraas duality is established mathematics, not a novelty claim.
"""
from pathlib import Path
import itertools
import json
import math
import time
import numpy as np

def ground_mps(n):
    a=[np.array([[0,math.sqrt(2/3)],[0,0]],complex),
       np.diag([-1/math.sqrt(3),1/math.sqrt(3)]).astype(complex),
       np.array([[0,0],[-math.sqrt(2/3),0]],complex)]
    psi=np.array([np.trace(np.linalg.multi_dot([a[s] for s in word]))
                  for word in itertools.product(range(3),repeat=n)])
    return psi/np.linalg.norm(psi)

sz=np.diag([1,0,-1]).astype(complex)
sp=math.sqrt(2)*np.array([[0,1,0],[0,0,1],[0,0,0]],complex)
sm=sp.T.conj()
dot=np.kron(sz,sz)+(np.kron(sp,sm)+np.kron(sm,sp))/2
p2=(dot@dot+3*dot+2*np.eye(9))/6
assert np.linalg.norm(p2@p2-p2)<1e-13

def local(op,sites,vec,n):
    other=[j for j in range(n) if j not in sites]
    perm=list(sites)+other
    arr=np.asarray(vec).reshape([3]*n).transpose(perm).reshape(3**len(sites),-1)
    out=(op@arr).reshape([3]*n).transpose(np.argsort(perm))
    return out.reshape(-1)

def local_dual_columns(psi,n,bond,r,offset=0):
    # Contiguous periodic block starts at first site of bond. Outside Schmidt
    # support is exactly the MPS-conditioned environment in this finite probe.
    sites=[(bond-offset+j)%n for j in range(r)]
    other=[j for j in range(n) if j not in sites]
    perm=sites+other
    arr=psi.reshape([3]*n).transpose(perm).reshape(3**r,-1)
    _,s,vh=np.linalg.svd(arr,full_matrices=False)
    keep=s>1e-11
    env=vh[keep].T
    inside=np.kron(np.eye(3**offset),np.kron(p2,np.eye(3**(r-offset-2))))
    evals,evecs=np.linalg.eigh(inside)
    columns=[]
    for u in evecs[:,evals>.5].T:
        for v in env.T:
            columns.append(np.outer(u,v).reshape([3]*n).transpose(np.argsort(perm)).reshape(-1))
    w=np.stack(columns,axis=1)
    assert np.linalg.norm(w.conj().T@w-np.eye(w.shape[1]))<1e-10
    return w

def run(n):
    t0=time.monotonic()
    psi=ground_mps(n)
    d=len(psi)
    def act(x):
        return sum(local(p2,[j,(j+1)%n],x,n) for j in range(n))
    assert np.linalg.norm(act(psi))<1e-12
    b=local(sz,[0],psi,n)
    b-=psi*np.vdot(psi,b)
    # Dense references up to N6; beyond that use a separately labeled implicit
    # correction-vector CG reference, without claiming a certified error bound.
    if n<=6:
        h=np.column_stack([act(np.eye(d)[:,j]) for j in range(d)])
        ev,u=np.linalg.eigh(h)
        keep=ev>1e-10
        exact=float(np.sum(np.abs(u[:,keep].conj().T@b)**2/ev[keep]).real)
        reference={'method':'dense eigensolve','matvecs_for_dense_matrix':d}
    else:
        x=np.zeros_like(b)
        residual=b.copy(); direction=residual.copy()
        rr=float(np.vdot(residual,residual).real)
        for iteration in range(1,1001):
            hd=act(direction)+psi*np.vdot(psi,direction)
            alpha=rr/float(np.vdot(direction,hd).real)
            x+=alpha*direction; residual-=alpha*hd
            new=float(np.vdot(residual,residual).real)
            if new<1e-24: break
            direction=residual+(new/rr)*direction; rr=new
        exact=float(np.vdot(b,x).real)
        reference={'method':'implicit correction-vector CG numerical reference',
                   'matvecs':iteration,'residual':math.sqrt(new),'certified_error_bound':False}
    rows=[]
    for r,all_offsets in [(2,False),(3,False),(3,True)]:
        groups=[]
        for j in range(n):
            w=np.concatenate([local_dual_columns(psi,n,j,r,offset)
                              for offset in range(r-1 if all_offsets else 1)],axis=1)
            if all_offsets:
                # Two placements contribute to the SAME physical row w_j.
                # Orthonormalizing the union charges its actual Hilbert norm.
                uu,ss,_=np.linalg.svd(w,full_matrices=False)
                w=uu[:,ss>1e-11]
            groups.append(w)
        a=np.concatenate(groups,axis=1)
        c,_,rank,_=np.linalg.lstsq(a,b,rcond=1e-11)
        residual=float(np.linalg.norm(a@c-b))
        dual=float(np.vdot(c,c).real)
        rows.append({'block_size':r,'all_contiguous_block_placements':all_offsets,
            'columns':a.shape[1],'rank':int(rank),
            'feasibility_residual':residual,'dual_norm':dual,
            'numerically_feasible_only':residual<1e-10,
            'upper_bound_claim':'NO exact/rational feasibility proof in this floating calculation; placement bases orthonormalized within each physical row',
            'dual_over_exact':dual/exact})
    return {'n':n,'hilbert_dimension':d,'ground_residual':float(np.linalg.norm(act(psi))),
            'exact_response_reference':exact,'reference_status':reference,'dual_probes':rows,
            'wall_seconds':time.monotonic()-t0}

if __name__=='__main__':
    result={'scope':'dense finite AKLT exploratory validation; no scalable exact completion or novelty established',
            'rows':[run(n) for n in [4,5,6,7,8]]}
    Path(__file__).with_name('aklt_dual_probe.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
