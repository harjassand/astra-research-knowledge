"""Complete from-raw-table classical baseline with no intermediate disk save.

Uses positive sparse elimination until 500k current edges, followed by bounded
dense positive symmetric rank-one updates. All mass is transferred exactly in
real arithmetic; source rates are HTST at the specified reduced temperature.
"""
from pathlib import Path
import argparse,json,math,os,resource,sys,time
sys.dont_write_bytecode=True
import numpy as np
from scipy import sparse
from scipy.linalg.blas import dsyr
from scipy.sparse.csgraph import connected_components
from positive_elimination import eliminate

HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent

def load_model(temperature):
    st=time.perf_counter();data=ROOT/"workers/lj38_acquisition_luna/full-network"
    mi=np.loadtxt(data/"min.data");ts=np.loadtxt(data/"ts.data");parse=time.perf_counter()-st
    ep=ts[:,3:5].astype(np.int64)-1;sel=ep[:,0]!=ep[:,1];ep=ep[sel];ts=ts[sel]
    # All parallel saddles are aggregated by sparse COO-to-CSR conversion.
    beta=1/temperature;e0,s0=mi[0,:2]
    cs=np.exp(-beta*(ts[:,0]-e0)-(ts[:,1]-s0)/2)/ts[:,2]
    a=sparse.csr_matrix((np.r_[cs,cs],(np.r_[ep[:,0],ep[:,1]],np.r_[ep[:,1],ep[:,0]])),shape=(len(mi),len(mi)))
    nc,labels=connected_components(a,directed=False);mask=labels==np.bincount(labels).argmax()
    ids=np.flatnonzero(mask)+1;a=a[mask,:][:,mask];upper=sparse.triu(a,format="coo")
    w=np.exp(-beta*(mi[mask,0]-e0)-(mi[mask,1]-s0)/2)/mi[mask,2]
    return np.column_stack((upper.row,upper.col)),upper.data,w,ids,{"parse_seconds":parse,"total_model_seconds":time.perf_counter()-st,
              "archive_nodes":len(mi),"nonself_saddle_rows":len(ts),"component_nodes":len(w),"component_pairs":len(upper.data),
              "components":nc,"source_tables":"official archived min.data/ts.data, all nonself saddles"}

def finish(core,seconds,reverse=False,shrink=64):
    st=time.perf_counter();p,c,w=core["pairs"],core["c"],core["w"].copy();n=len(w)
    assert n<5000
    source,target=int(core["source"]),int(core["target"])
    order=np.argsort(np.bincount(p.ravel(),minlength=n),kind="stable")
    if reverse:order=order[::-1]
    order=np.r_[[k for k in order if k not in (source,target)],[source,target]]
    remap=np.empty(n,dtype=np.int64);remap[order]=np.arange(n)
    q=np.sort(remap[p],axis=1)
    a=np.zeros((n,n),order="F");a[q[:,0],q[:,1]]=c;w=w[order]
    initial_n=n;removed=0;local=0
    while len(w)-local>2:
        if time.perf_counter()-st>seconds:raise TimeoutError("dense core time limit")
        k=local;v=np.r_[a[:k,k],0.,a[k,k+1:]].copy();den=math.fsum(v)
        w+=w[k]*(v/den);w[k]=0.
        a=dsyr(1/den,v,a=a,lower=0,overwrite_a=1)
        a[:k,k]=0.;a[k,k:]=0.;np.fill_diagonal(a,0.)
        local+=1;removed+=1
        if local>=shrink and len(w)-local>2:
            a=np.array(a[local:,local:],order="F");w=w[local:];local=0
    return float(a[-2,-1]),float(w[-2]),float(w[-1]),{"seconds":time.perf_counter()-st,"initial_nodes":initial_n,"reverse_order":reverse}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--temperature",type=float,default=.2);ap.add_argument("--source",type=int,default=1)
    ap.add_argument("--target",type=int,default=7);ap.add_argument("--edge-cap",type=int,default=500000)
    ap.add_argument("--seconds",type=float,default=52.);ap.add_argument("--reverse",action="store_true");ap.add_argument("--tag",default="")
    args=ap.parse_args();st=time.perf_counter();usage0=resource.getrusage(resource.RUSAGE_SELF)
    p,c,w,ids,load=load_model(args.temperature);z=math.fsum(w)
    source=int(np.flatnonzero(ids==args.source)[0]);target=int(np.flatnonzero(ids==args.target)[0])
    sparse_st=time.perf_counter()
    stage,core=eliminate(p,c,w,source,target,args.seconds-(time.perf_counter()-st),args.edge_cap,return_core=True)
    stage["including_in_memory_core_export_seconds"]=time.perf_counter()-sparse_st
    cap,ns,nt,ds=finish(core,args.seconds-(time.perf_counter()-st),args.reverse)
    result={"status":"complete","method":"classical positive star-mesh/mass transfer; sparse dynamic minimum degree + dense BLAS symmetric rank one",
            "source_archive_id":args.source,"target_archive_id":args.target,"temperature":args.temperature,
            "component_Z":z,"capacity_omitting_1_over_2pi":cap,"N_source_to_target":ns,"N_target_to_source":nt,
            "MFPT_source_to_target_raw":ns/cap,"MFPT_target_to_source_raw":nt/cap,
            "MFPT_source_to_target_HTST":2*math.pi*ns/cap,"MFPT_target_to_source_HTST":2*math.pi*nt/cap,
            "nu_HTST":cap/z/(2*math.pi),"relative_mass_drift":(ns+nt)/z-1,
            "total_from_raw_tables_seconds":time.perf_counter()-st,"model_phase":load,"sparse_phase":stage,"dense_phase":ds,
            "peak_rss_bytes_macos":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "limits":{"seconds":args.seconds,"sparse_current_edges":args.edge_cap,"dense_core_nodes":5000},
            "arithmetic":"float64 approximate; all updates nonnegative; no directed-rounding certificate"}
    usage1=resource.getrusage(resource.RUSAGE_SELF)
    result["process_cpu_seconds_in_timed_pipeline"]=(usage1.ru_utime+usage1.ru_stime)-(usage0.ru_utime+usage0.ru_stime)
    result["thread_environment"]={k:os.environ.get(k) for k in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","VECLIB_MAXIMUM_THREADS")}
    name=f"classical_T{args.temperature}_{args.source}_{args.target}_cap{args.edge_cap}"+("_reverse" if args.reverse else "")+args.tag
    (HERE/(name+".json")).write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2),flush=True)
if __name__=="__main__":main()
