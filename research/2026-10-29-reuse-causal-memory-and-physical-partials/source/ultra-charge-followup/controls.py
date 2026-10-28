"""Ordinary model controls for A's EXACT Floquet target.

Retain the diagonal U contribution. HF is an approximation to the physical
density step, not an alternative exact simulator or a claimed lower bound.
"""
import hashlib
import json
import time
from pathlib import Path
import numpy as np
from scipy.linalg import hadamard

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'a_noise_geometry'/'EXECUTION.json'


def hop(C,offset):
    c=15/17; s=8/17
    for i in range(offset,len(C)-1,2):
        j=i+1
        a=C[i,:].copy(); b=C[j,:].copy()
        C[i,:]=c*a-1j*s*b; C[j,:]=-1j*s*a+c*b
        a=C[:,i].copy(); b=C[:,j].copy()
        C[:,i]=c*a+1j*s*b; C[:,j]=1j*s*a+c*b


def hf_derivative(C,U,diag):
    # Density-density Hartree-Fock including exact onebody U_ii/2.
    F=-U*C
    np.fill_diagonal(F,U@C.diagonal().real-diag*C.diagonal().real+diag/2)
    dephase=-C.copy(); np.fill_diagonal(dephase,0)
    return -1j*(F@C-C@F)+dephase


def run(d,steps):
    m=d['modes']; rank=m//2; h=d['density_step_h']; cycles=d['cycles']
    U=hadamard(m)/np.sqrt(m); diag=U.diagonal().copy()
    C=np.diag([1.]*rank+[0.]*(m-rank)).astype(complex)
    G=C.copy(); phase=np.exp(-.5j*h*diag)
    save={r['cycle'] for r in d['checkpoints']}; rows=[]
    start=time.perf_counter()
    for k in range(cycles+1):
        if k in save:
            rows.append({'cycle':k,'quartic_removed_diagU_retained':float(np.trace(G[:rank,:rank]).real/rank),
                         'time_dependent_Hartree_Fock':float(np.trace(C[:rank,:rank]).real/rank),
                         'HF_hermiticity_error':float(np.linalg.norm(C-C.conj().T)),
                         'HF_particle_trace_error':float(abs(np.trace(C)-rank)),
                         'HF_eigenvalue_range':[float(np.linalg.eigvalsh(C).min()),float(np.linalg.eigvalsh(C).max())]})
        if k==cycles: break
        hop(C,0); hop(C,1); hop(G,0); hop(G,1)
        G*=phase[:,None]*phase[None,:].conj()
        saved=G.diagonal().copy(); G*=np.exp(-h); np.fill_diagonal(G,saved)
        dt=h/steps
        for j in range(steps):
            a=hf_derivative(C,U,diag)
            b=hf_derivative(C+dt*a/2,U,diag)
            c=hf_derivative(C+dt*b/2,U,diag)
            e=hf_derivative(C+dt*c,U,diag)
            C+=dt*(a+2*b+2*c+e)/6
    return {'RK4_substeps_per_density_step':steps,'seconds_after_setup':time.perf_counter()-start,'rows':rows}


def main():
    start=time.perf_counter(); raw=SOURCE.read_bytes(); d=json.loads(raw)
    coarse=run(d,16); fine=run(d,32)
    diff=max(abs(a['time_dependent_Hartree_Fock']-b['time_dependent_Hartree_Fock']) for a,b in zip(coarse['rows'],fine['rows']))
    out={'source':str(SOURCE),'source_sha256':hashlib.sha256(raw).hexdigest(),
         'model':'Same U, Gamma=I, initial Fock and exact hopping rotations; diagonal U retained in BOTH controls',
         'meaning':'Approximation comparison ONLY; ordinary global-feedback exact method already attains the same target.',
         'coarse':coarse,'fine':fine,'max_checkpoint_HF_refinement_change':diff,
         'source_trajectory_last_mean':d['checkpoints'][-1]['left_fraction_mean'],
         'total_seconds_after_imports':time.perf_counter()-start,
         'numerical_scope':'complex128/RK4 convergence diagnostic; not directed integration or physical evidence'}
    (ROOT/'CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('coarse','fine')},indent=2))
    print(json.dumps(fine['rows'][-1],indent=2))


if __name__=='__main__': main()
