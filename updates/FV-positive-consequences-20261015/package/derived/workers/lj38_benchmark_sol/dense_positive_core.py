"""Finish a sparse positive-elimination checkpoint with BLAS symmetric rank one.

Dense storage is limited to the already reduced core (normally <4000 nodes).
Classical positive Schur updates only: no cancellation-prone inverse/solve.
"""
from pathlib import Path
import argparse,json,math,resource,time
import numpy as np
from scipy.linalg.blas import dsyr

HERE=Path(__file__).resolve().parent
def main():
    ap=argparse.ArgumentParser();ap.add_argument("checkpoint");ap.add_argument("--seconds",type=float,default=52.)
    ap.add_argument("--shrink",type=int,default=64);ap.add_argument("--reverse",action="store_true")
    args=ap.parse_args();st=time.perf_counter(); z=np.load(HERE/args.checkpoint)
    p=z["pairs"];c=z["c"];w=z["w"].astype(np.float64);indices=z["component_indices"]
    source=int(z["source"]);target=int(z["target"]);n=len(w)
    assert n<5000, "Refuse a large dense core"
    a=np.zeros((n,n),order="F");a[p[:,0],p[:,1]]=c
    # Reorder once by original core degree; terminals are always retained.
    degree=np.bincount(p.ravel(),minlength=n)
    order=np.argsort(degree,kind="stable")
    if args.reverse: order=order[::-1]
    order=np.r_[[k for k in order if k not in (source,target)],[source,target]]
    a=np.array((a+a.T)[np.ix_(order,order)],order="F");w=w[order];indices=indices[order]
    mass0=np.sum(w,dtype=np.longdouble); initial_n=n; removed=0;local=0;snapshots=[];next_snap=5.
    status="complete";setup=time.perf_counter()-st
    while len(w)-local>2:
        elapsed=time.perf_counter()-st
        if elapsed>args.seconds: status="time_limit";break
        k=local
        # Upper triangle is the authoritative symmetric copy.
        v=np.r_[a[:k,k],0.,a[k,k+1:]].copy()
        den=math.fsum(v)
        if den<=0: raise ValueError("Nonpositive conductance pivot")
        w += w[k]*(v/den); w[k]=0.
        a=dsyr(1./den,v,a=a,lower=0,overwrite_a=1)
        a[:k,k]=0.;a[k,k:]=0.;np.fill_diagonal(a,0.)
        local+=1;removed+=1
        if local>=args.shrink and len(w)-local>2:
            a=np.array(a[local:,local:],order="F");w=w[local:];indices=indices[local:];local=0
        if elapsed>next_snap:
            row={"seconds":elapsed,"remaining_nodes":initial_n-removed};snapshots.append(row);print(json.dumps(row),flush=True);next_snap=elapsed+5.
    result={"status":status,"core_initial_nodes":initial_n,"removed_nodes":removed,"seconds":time.perf_counter()-st,
            "setup_seconds":setup,"relative_mass_drift":float(np.sum(w,dtype=np.longdouble)/mass0-1),
            "initial_core_mass":str(mass0),"final_core_mass":str(np.sum(w,dtype=np.longdouble)),
            "reverse_order":args.reverse,"progress":snapshots,
            "peak_rss_bytes_macos":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "dense_memory_limit_nodes":5000,"time_limit_seconds":args.seconds}
    if status=="complete":
        cap=a[-2,-1]; ns,nt=w[-2:]; factor=2*math.pi
        result.update({"source_component_index":int(indices[-2]),"target_component_index":int(indices[-1]),
                       "capacity_omitting_1_over_2pi":str(cap),"N_source_to_target":str(ns),"N_target_to_source":str(nt),
                       "nu_HTST":str(cap/mass0/factor),"MFPT_source_to_target_HTST":str(ns/cap*factor),
                       "MFPT_target_to_source_HTST":str(nt/cap*factor),"commute_HTST":str(mass0/cap*factor)})
    name=args.checkpoint.removesuffix(".npz")+("_dense_reverse" if args.reverse else "_dense")
    (HERE/(name+".json")).write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2),flush=True)
if __name__=="__main__":main()
