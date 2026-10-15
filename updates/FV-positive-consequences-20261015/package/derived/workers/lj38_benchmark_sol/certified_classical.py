"""Classical positive GT trial potentials, checked by the shared Decimal verifier.

This adds no candidate reductions: every original component state and saddle
is represented by exact classical elimination/back-substitution in real
arithmetic. The independent certificate accounts for all float errors against
the source-decimal HTST model. Maximum wall budget 55 seconds.
"""
from pathlib import Path
import json,math,os,resource,signal,sys,time,traceback
sys.dont_write_bytecode=True
import numpy as np
from scipy import sparse
from scipy.linalg.blas import dsyr
from positive_elimination import eliminate

HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
import source_decimal_verifier as verifier

class Budget(Exception):pass
def finish_witness(core,deadline):
    st=time.perf_counter();p,c,w=core["pairs"],core["c"],core["w"].copy();n=len(w)
    assert n<5000
    s,t=int(core["source"]),int(core["target"])
    order=np.argsort(np.bincount(p.ravel(),minlength=n),kind="stable")
    order=np.r_[[k for k in order if k not in (s,t)],[s,t]]
    remap=np.empty(n,dtype=np.int64);remap[order]=np.arange(n)
    q=np.sort(remap[p],axis=1);a=np.zeros((n,n),order="F");a[q[:,0],q[:,1]]=c;w=w[order]
    rec=[];loc=0;removed=0
    while len(w)-loc>2:
        if time.perf_counter()>deadline:raise Budget("55s budget")
        k=loc;v=np.r_[a[:k,k],0.,a[k,k+1:]];den=math.fsum(v)
        rec.append((w[k]/den,v[k+1:]/den))
        w+=w[k]*(v/den);w[k]=0
        a=dsyr(1/den,v,a=a,lower=0,overwrite_a=1);a[:k,k]=0;a[k,k:]=0;np.fill_diagonal(a,0)
        loc+=1;removed+=1
        if loc>=64 and len(w)-loc>2:
            a=np.array(a[loc:,loc:],order="F");w=w[loc:];loc=0
    cap=float(a[-2,-1]);ns=float(w[-2]);nt=float(w[-1]);pot=np.zeros((n,2));pot[-2]=[1/cap,ns/cap]
    for k in range(n-3,-1,-1):
        offset,prob=rec[k];pot[k]=prob@pot[k+1:];pot[k,1]+=offset
    ans=np.empty_like(pot);ans[order]=pot
    return ans,dict(seconds=time.perf_counter()-st,capacity=cap,N_source=ns,N_target=nt,
                    raw_MFPT=ns/cap,core_nodes=n,backsubstitution_records=len(rec))

def main():
    st=time.perf_counter();cpu=time.process_time();deadline=st+55
    def stop(*_):raise Budget("55s budget")
    signal.signal(signal.SIGALRM,stop);signal.setitimer(signal.ITIMER_REAL,55)
    out={"source_archive_id":1,"target_archive_id":7,"temperature":"0.2",
         "method":"classical positive star-mesh/mass transfer with exact-elimination back-substitution trials and shared source-Decimal residual certificate"}
    try:
        g,receipt=verifier.load_lj38(ROOT/"workers/lj38_acquisition_luna/full-network","0.2",True,80,1,7)
        out["model_phase"]=receipt
        agg_st=time.perf_counter()
        a=sparse.csr_matrix((np.r_[g.c,g.c],(np.r_[g.u,g.v],np.r_[g.v,g.u])),shape=(g.n,g.n));u=sparse.triu(a,format="coo")
        p=np.column_stack((u.row,u.col));c=u.data
        out["parallel_aggregation_seconds"]=time.perf_counter()-agg_st
        ss,core=eliminate(p,c,g.w,g.s,g.t,seconds=deadline-time.perf_counter(),edge_cap=500000,return_core=True,record=True)
        out["sparse_phase"]=ss
        pot,ds=finish_witness(core,deadline);out["dense_and_backsubstitution_phase"]=ds
        back_st=time.perf_counter();full=np.zeros((g.n,2));full[core["component_indices"]]=pot
        for k,neighbors,prob,offset in reversed(core["records"]):
            full[k]=prob@full[neighbors];full[k,1]+=offset
        out["sparse_backsubstitution_seconds"]=time.perf_counter()-back_st
        assert full[g.t,0]==0 and full[g.t,1]==0 and np.isfinite(full).all()
        ts=time.perf_counter();_,tree,_=verifier.select_partition(g,g.n);out["routing_tree_seconds"]=time.perf_counter()-ts
        out["certificate"]=verifier.interval_certificate(g,full[:,0],full[:,1],tree,80)
        out["HTST_time_interval"]=verifier.htst_time_interval(out["certificate"],80)
        out["status"]="complete"
        np.savez_compressed(HERE/"classical_witness_T0.2_1_7.npz",x=full[:,0],y=full[:,1],tree=tree,
                            source=g.s,target=g.t,n=g.n)
        out["witness_sha256"]=verifier.file_sha(HERE/"classical_witness_T0.2_1_7.npz")
    except Exception as exc:
        out.update(status="budget_limit" if isinstance(exc,Budget) else "error",exception=repr(exc),traceback=traceback.format_exc())
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
        out.update(total_from_source_model_seconds=time.perf_counter()-st,process_cpu_seconds=time.process_time()-cpu,
                   peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                   thread_environment={k:os.environ.get(k) for k in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","VECLIB_MAXIMUM_THREADS")},
                   time_limit_seconds=55,verifier_source_sha256=verifier.file_sha(Path(verifier.__file__)))
        (HERE/"CERTIFIED_CLASSICAL_T0.2_1_7.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2),flush=True)
if __name__=="__main__":main()
