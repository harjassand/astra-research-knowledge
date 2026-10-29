"""Literal CAR check, independent of mask hopping/sign formulas."""
import json
import time
from pathlib import Path
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import expm_multiply
from native import compile_hubbard, quantities

HERE=Path(__file__).resolve().parent


def annihilate(L,k):
    D=1<<(2*L)
    row=[];col=[];val=[]
    for m in range(D):
        if m>>k&1:
            row.append(m^(1<<k));col.append(m)
            val.append((-1)**((m&((1<<k)-1)).bit_count()))
    return sparse.csr_matrix((np.array(val,dtype=np.int64),(row,col)),shape=(D,D))


def zero(A):
    A.eliminate_zeros()
    return A.nnz==0


def main():
    tic=time.perf_counter();L=4;D=1<<(2*L)
    cs=[annihilate(L,k) for k in range(2*L)]
    I=sparse.eye(D,dtype=np.int64,format='csr')
    car_checks=0
    for i in range(2*L):
        for j in range(2*L):
            assert zero(cs[i]@cs[j].T+cs[j].T@cs[i]-(I if i==j else 0*I))
            car_checks+=1
    edges=[(0,1),(2,3),(0,2),(1,3)]
    ns=[c.T@c for c in cs]
    h=sparse.csr_matrix((D,D),dtype=np.int64)
    for i,j in edges:
        for spin in (0,L):
            h-=cs[spin+i].T@cs[spin+j]+cs[spin+j].T@cs[spin+i]
    for j in range(L):
        h+=8*ns[j]@ns[L+j]-4*(ns[j]+ns[L+j])
    eta=sum(((-1)**((j%2)+(j//2))*(cs[j].T@cs[L+j].T) for j in range(L)),0*h)
    assert zero(h@eta-eta@h)
    assert zero(eta@eta.T-eta.T@eta-sum(ns,-L*I))
    H,pairs,ms,off,r=compile_hubbard(2,2,4)
    raw=[];ph=[]
    for q,ss in enumerate(ms):
        raw.extend([int(u)+(int(d)<<L) for u in ss for d in ss])
        ph.extend([(-1)**(q*(q-1)//2)]*(len(ss)**2))
    ph=np.array(ph,dtype=np.int64)
    dense_native=h[np.array(raw)][:,np.array(raw)].toarray()
    pair=cs[0].T@cs[L].T
    dense_source=(pair+pair.T)[np.array(raw)][:,np.array(raw)].toarray()
    expected=ph[:,None]*(20*dense_native+dense_source)*ph[None,:]+20*r['shift']*np.eye(len(raw),dtype=int)
    assert np.array_equal(H.toarray(),expected)
    # Numerical full-physical evolution is a diagnostic, not the exact proof.
    # R = product of local eta rotations; verify both state and observables.
    y=(eta-eta.T)/(2j)
    vac=np.zeros(D,complex);vac[0]=1
    initial=expm_multiply(1j*np.pi/2*y,vac)
    physical=h.astype(float)+(ns[0]+ns[L]-I)/20
    original=expm_multiply(-1j*10*physical,initial)
    frame=expm_multiply(-1j*10*(H/20-r['shift']*sparse.eye(H.shape[0])),np.eye(1,H.shape[0],0).ravel())
    obs=quantities(frame,pairs,ms,off)
    orig_density=float(np.vdot(original,(ns[0]+ns[L]-I)@original).real)
    orig_y=float(np.vdot(original,(pair-pair.T)@original/(2j)).real)
    assert abs(orig_density-obs['density_excess_at_source'])<1e-10
    assert abs(orig_y-obs['eta_y_at_source'])<1e-10
    result=dict(exact_CAR_checks=car_checks,exact_eta_commutator=True,
                exact_eta_algebra=True,exact_all_hamiltonian_entries=True,
                balanced_dimension=len(raw),physical_dimension=D,
                full_physical_density_diagnostic=orig_density,
                rotated_density_diagnostic=obs['density_excess_at_source'],
                physical_eta_y_diagnostic=orig_y,rotated_eta_y_diagnostic=obs['eta_y_at_source'],
                status='PASS exact finite identities; exponential diagnostics are binary64 only',
                seconds=time.perf_counter()-tic)
    (HERE/'NATIVE_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
