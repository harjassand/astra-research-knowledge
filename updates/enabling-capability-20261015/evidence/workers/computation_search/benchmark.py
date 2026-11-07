"""Measure real N2 FCIDUMP, strong PySCF FCI, and omitted-space certificates.

All numbers are floating-point diagnostics until a separate outward-rounded
certificate is checked. No physical experimental accuracy is asserted.
"""
import time
START=time.perf_counter()
import json
import hashlib
from pathlib import Path
import platform
import resource
import sys
import numpy as np
import scipy
from scipy import linalg, sparse
from scipy.sparse.linalg import eigsh
import pyscf
from pyscf import fci, lib
from pyscf.tools import fcidump

BASE=Path(__file__).resolve().parent
lib.num_threads(1)
OUTPUT={"scope":"finite-basis N2 at 1.1 Angstrom, STO-3G, 14 electrons, Ms=0, Ag sector; printed FCIDUMP is computational input truth", "versions":{"python":sys.version,"pyscf":pyscf.__version__,"numpy":np.__version__,"scipy":scipy.__version__,"platform":platform.platform()},"import_seconds":time.perf_counter()-START,"threads_requested":1,"effective_omp_threads":"OpenMP unavailable in installed PySCF wheel","effective_blas_threads":"UNKNOWN"}


def save():
    OUTPUT["elapsed_seconds"]=time.perf_counter()-START
    OUTPUT["peak_rss_bytes_macos"]=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    (BASE/"BENCHMARK.json").write_text(json.dumps(OUTPUT,indent=2))


def report(name,value):
    OUTPUT[name]=value
    save()
    print(name,json.dumps(value),flush=True)


def main():
    t=time.perf_counter()
    path=BASE/"source/data/N2.STO3G.FCIDUMP"
    d=fcidump.read(str(path),molpro_orbsym=True,verbose=False)
    h1,eri,n,ne,ecore=d['H1'],d['H2'],d['NORB'],d['NELEC'],d['ECORE']
    os=np.asarray(d['ORBSYM'])
    nelec=(ne//2,ne//2)
    report("input",dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(),norb=n,nelec=nelec,ecore=ecore,orbsym_pyscf=os.tolist(),parse_seconds=time.perf_counter()-t))
    results=[]
    for pspace_size,tol in [(400,1e-10),(0,1e-10),(0,1e-6)]:
        fs=fci.direct_spin1_symm.FCI()
        fs.orbsym=os
        fs.wfnsym=0
        fs.pspace_size=pspace_size
        fs.conv_tol=tol
        fs.max_cycle=100
        calls=[0]
        fn=fs.contract_2e
        def contract(*args,**kw):
            calls[0]+=1
            return fn(*args,**kw)
        fs.contract_2e=contract
        t=time.perf_counter();e,v=fs.kernel(h1,eri,n,nelec,ecore=ecore)
        elapsed=time.perf_counter()-t
        results.append(dict(pspace_size=pspace_size,tolerance=tol,energy=float(e),converged=bool(fs.converged),wall_seconds=elapsed,contract_2e_calls=calls[0]))
        if len(results)==1:
            np.save(BASE/"reference_vector.npy",v)
            OUTPUT['reference_energy']=float(e)
        report("incumbent_fci",results)
    # Charge acquiring every entry of the symmetry-restricted determinant matrix.
    t=time.perf_counter()
    strs=fci.cistring.make_strings(range(n),nelec[0])
    ir=fci.direct_spin1_symm._gen_strs_irrep(strs,os)
    allowed=(ir[:,None]^ir[None,:]).ravel()==0
    hd=fci.direct_spin1.make_hdiag(h1,eri,n,nelec)
    hd_mask=hd.copy();hd_mask[~allowed]=np.inf
    count=int(allowed.sum())
    addr,H=fci.direct_spin1.pspace(h1,eri,n,nelec,hdiag=hd_mask,np=count)
    H+=np.eye(count)*ecore
    assert allowed[addr].all()
    assert np.isfinite(H).all()
    np.savez(BASE/"hamiltonian.npz",H=H,addresses=addr)
    report("full_matrix_acquisition",dict(full_determinants=int(hd.size),sector_determinants=count,wall_seconds=time.perf_counter()-t,matrix_bytes=H.nbytes,nonzero_count=int(np.count_nonzero(H)),symmetry_error=float(np.max(np.abs(H-H.T)))))
    t=time.perf_counter()
    evals=linalg.eigh(H,subset_by_index=[0,1],driver='evr',eigvals_only=True)
    report("dense_reference",dict(energies=evals.tolist(),wall_seconds=time.perf_counter()-t,fci_agreement=float(abs(evals[0]-OUTPUT['reference_energy']))))
    t=time.perf_counter()
    # Entrywise absolute-value relaxation: exact optimal scalar diagonal scaling.
    M=np.diag(np.diag(H)+np.abs(np.diag(H)))-np.abs(H)
    me,mv=eigsh(sparse.csr_matrix(M),k=1,which='SA',tol=1e-10)
    report("comparison_floor",dict(energy=float(me[0]),gap_to_true=float(evals[0]-me[0]),wall_seconds=time.perf_counter()-t))
    # Determinants are selected by computed residual/PT2 scores, never oracle v.
    order=np.argsort(np.diag(H));P=order[:1].tolist()
    cert=[]
    all_ids=np.arange(count)
    for size in [1,8,32,128,512]:
        t=time.perf_counter()
        while len(P)<size:
            p=np.asarray(P,dtype=int);q=np.setdiff1d(all_ids,p)
            ae,av=linalg.eigh(H[np.ix_(p,p)],subset_by_index=[0,0],driver='evr')
            r=H[np.ix_(q,p)]@av[:,0]
            den=np.maximum(np.diag(H)[q]-ae[0],1e-8)
            scores=(r*r)/den
            add=q[np.argsort(scores)[::-1][:min(size-len(P),max(1,len(P)))]]
            P.extend(add.tolist())
        p=np.asarray(P,dtype=int);q=np.setdiff1d(all_ids,p)
        A=H[np.ix_(p,p)];B=H[np.ix_(p,q)];C=H[np.ix_(q,q)]
        ae,av=linalg.eigh(A,subset_by_index=[0,0],driver='evr')
        a=float(ae[0]);u=av[:,0]
        res=B.T@u
        pt2=float(np.sum(res*res/(a-np.diag(C))))
        # Unscaled/optimally-scaled scalar complement lower bounds.
        Cabs=np.diag(np.diag(C)+np.abs(np.diag(C)))-np.abs(C)
        cg=float(np.min(np.diag(C)-np.sum(np.abs(C-np.diag(np.diag(C))),axis=1)))
        ce,cw=eigsh(sparse.csr_matrix(Cabs),k=1,which='SA',tol=1e-9)
        weight_floors=[]
        for wf in [1.,1e-2,1e-4,1e-6,1e-8,1e-10,1e-12]:
            w=np.maximum(np.abs(cw[:,0]),wf)
            bound=float(np.min(np.diag(C)-((np.abs(C)@w)-np.abs(np.diag(C))*w)/w))
            weight_floors.append((wf,bound))
        cl=max(x[1] for x in weight_floors)
        beta=float(min(np.linalg.norm(B,'fro'),np.sqrt(np.linalg.norm(B,1)*np.linalg.norm(B,np.inf))))
        lower=float((a+cl-np.sqrt((a-cl)**2+4*beta*beta))/2)
        row=dict(selected_size=len(P),complement_size=len(q),upper=a,upper_error=float(a-evals[0]),pt2_corrected=a+pt2,pt2_error=float(a+pt2-evals[0]),residual_norm=float(np.linalg.norm(res)),complement_gershgorin=cg,complement_scaled_floor=cl,complement_comparison_eigenvalue=float(ce[0]),weight_floors=weight_floors,coupling_bound=beta,lower=lower,interval_width=a-lower,wall_seconds=time.perf_counter()-t)
        cert.append(row)
        report("selected_space_diagnostics",cert)
    report("status",{"achievement":"NOT_ACHIEVED","certificate_status":"floating_point_diagnostics_only","next_gate":"tight lower bound, full cost and rounding certificate before promotion","chemical_accuracy_hartree":0.00159360143764})


if __name__=='__main__':
    main()
