"""Close vector/cost provenance: fresh pspace=0 solve and saved exact vector."""
import time
START=time.perf_counter()
import json
import hashlib
from pathlib import Path
import platform
import resource
import numpy as np
import pyscf
from pyscf import fci,lib
from pyscf.tools import fcidump

BASE=Path(__file__).resolve().parent


def main():
    out={'import_seconds':time.perf_counter()-START,'pyscf_version':pyscf.__version__,'platform':platform.platform(),'threads_requested':1,'effective_blas_threads':'UNKNOWN','effective_omp_threads':'unavailable in installed wheel'}
    lib.num_threads(1)
    t=time.perf_counter();path=BASE/'source/data/N2.STO3G.FCIDUMP'
    d=fcidump.read(str(path),molpro_orbsym=True,verbose=False)
    out['parse_seconds']=time.perf_counter()-t
    out['input_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    nelec=(d['NELEC']//2,d['NELEC']//2)
    fs=fci.direct_spin1_symm.FCI()
    fs.orbsym=np.asarray(d['ORBSYM']);fs.wfnsym=0
    fs.pspace_size=0;fs.conv_tol=1e-10;fs.max_cycle=100
    calls=[0];fn=fs.contract_2e
    def contract(*args,**kw):
        calls[0]+=1
        return fn(*args,**kw)
    fs.contract_2e=contract
    t=time.perf_counter()
    energy,vec=fs.kernel(d['H1'],d['H2'],d['NORB'],nelec,ecore=d['ECORE'])
    out['solver_seconds']=time.perf_counter()-t
    out.update(pspace_size=0,tolerance=1e-10,energy_hartree=float(energy),converged=bool(fs.converged),contract_2e_calls=calls[0])
    t=time.perf_counter();np.save(BASE/'fast_vector.npy',vec)
    out['vector_save_seconds']=time.perf_counter()-t
    out['vector_path']=str(BASE/'fast_vector.npy')
    out['vector_sha256']=hashlib.sha256((BASE/'fast_vector.npy').read_bytes()).hexdigest()
    old=np.load(BASE/'reference_vector.npy')
    if np.vdot(old,vec)<0:old=-old
    out['norm_difference_to_first_run_vector']=float(np.linalg.norm(vec-old))
    t=time.perf_counter();data=np.load(BASE/'hamiltonian.npz');H=data['H'];addr=data['addresses'];v=vec.ravel()[addr]
    e=float(v@(H@v)/(v@v));out['saved_H_rayleigh_hartree']=e
    out['saved_H_residual_norm']=float(np.linalg.norm(H@v-e*v))
    out['validation_seconds']=time.perf_counter()-t
    out['elapsed_seconds']=time.perf_counter()-START
    out['peak_rss_bytes_macos']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    out['scope']='actual fresh fast-solver vector and measured solver acquisition cost; numerical residual is a diagnostic, certificate comes from separate replay'
    (BASE/'FAST_VECTOR_REPLAY.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2),flush=True)


if __name__=='__main__':main()
