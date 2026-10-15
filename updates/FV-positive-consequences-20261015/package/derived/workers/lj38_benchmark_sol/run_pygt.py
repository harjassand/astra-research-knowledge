"""Bounded execution of pinned, unmodified PyGT with phase/progress receipts."""
from pathlib import Path
import argparse,json,math,resource,signal,sys,time,traceback
import numpy as np
from scipy import sparse

HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/"workers/baseline_code_luna/PyGT"))
import PyGT

class Limit(Exception):pass
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--mode",choices=("loader","full","core","fixture"),default="full")
    ap.add_argument("--temperature",default="0.2");ap.add_argument("--source",type=int,default=1);ap.add_argument("--target",type=int,default=2)
    ap.add_argument("--seconds",type=float,default=54.);ap.add_argument("--block",type=int,default=50)
    ap.add_argument("--dense-core",action="store_true")
    args=ap.parse_args();st=time.perf_counter();phase="imported";progress=[];last=st;calls=0
    result={"mode":args.mode,"source_archive_id":args.source,"target_archive_id":args.target,
            "temperature":float(args.temperature),"block":args.block,"time_limit_seconds":args.seconds,
            "pinned_source_commit":"fa0e106958d9948209daff04360290d50de82572",
            "runtime_module_version":PyGT.__version__}
    def timeout(*_):raise Limit("wall-clock limit")
    signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,args.seconds)
    original=PyGT.GT.singleGT
    def monitored(rm,B,tau,*a,**kw):
        nonlocal last,calls
        calls+=1;now=time.perf_counter()
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if rss>1500000000:raise Limit("1.5GB observed peak-RSS limit")
        if now-last>5:
            row={"seconds":now-st,"nodes":len(tau),"nnz":int(B.nnz) if sparse.issparse(B) else int(np.count_nonzero(B)),
                 "singleGT_calls":calls,"peak_rss_bytes_macos":rss}
            progress.append(row);print(json.dumps(row),flush=True);last=now
        return original(rm,B,tau,*a,**kw)
    PyGT.GT.singleGT=monitored
    try:
        if args.mode in ("loader","fixture"):
            phase="official_load_ktn"
            data=ROOT/"workers/lj38_acquisition_luna/full-network"
            B,K,tau,n,u,s,emin,retained=PyGT.io.load_ktn(str(data),beta=1/float(args.temperature),
                                                        Nmax=400 if args.mode=="fixture" else None)
            result.update({"loader_seconds":time.perf_counter()-st,"retained_nodes":int(n),"K_nnz":int(K.nnz),
                           "branching_column_sum_max_error":float(np.max(np.abs(np.ravel(B.sum(axis=0))-1)))})
            np.savez_compressed(HERE/f"pygt_{args.mode}_T{args.temperature}.npz",K_data=K.data,K_indices=K.indices,
                                K_indptr=K.indptr,shape=K.shape,tau=tau,u=u,s=s,emin=emin,retained=retained)
            if args.mode=="loader":
                expected=np.load(HERE/f"model_T{args.temperature}.npz");p=expected["pairs"];c=expected["c"];w=expected["w"]
                q=c[:,None]/w[p]/(2*math.pi)
                cmp=sparse.csr_matrix((np.r_[q[:,0],q[:,1]],(np.r_[p[:,1],p[:,0]],np.r_[p[:,0],p[:,1]])),shape=K.shape)
                result["max_relative_rate_difference_to_independent_loader"]=float(np.max(np.abs(K.data/cmp.data-1)))
                result["max_relative_stationary_mass_difference"]=float(np.max(np.abs(np.exp(-1/float(args.temperature)*u+s)/np.exp(s[0])/w* w[0]-1)))
            else:
                result["fixture_note"]="Original supplied tables restricted to endpoints<400 by official Nmax, not the full scientific benchmark"
        else:
            phase="matched_input_build"
            model=np.load(HERE/f"model_T{args.temperature}.npz")
            if args.mode=="core":
                z=np.load(HERE/f"positive_T{args.temperature}_{args.source}_{args.target}_float64_checkpoint.npz")
                p,c,w=z["pairs"],z["c"],z["w"];source=int(z["source"]);target=int(z["target"])
            else:
                p,c,w=model["pairs"],model["c"],model["w"]
                source=int(np.flatnonzero(model["ids"]==args.source)[0]);target=int(np.flatnonzero(model["ids"]==args.target)[0])
            n=len(w);q=c[:,None]/w[p]/(2*math.pi)
            K=sparse.csr_matrix((np.r_[q[:,0],q[:,1]],(np.r_[p[:,1],p[:,0]],np.r_[p[:,0],p[:,1]])),shape=(n,n))
            tau=1/np.ravel(K.sum(axis=0));B=K@sparse.diags(tau)
            result.update({"input_build_seconds":time.perf_counter()-st,"initial_nodes":n,"initial_nnz":int(B.nnz)})
            if args.dense_core:
                assert args.mode=="core" and n<5000
                B=B.toarray()
            phase="pinned_PyGT_compute_MFPT"
            # compute_MFPT(i,j) returns i<-j, then j<-i, per pinned doc/code.
            reverse,forward=PyGT.mfpt.compute_MFPT(source,target,B,tau,block=args.block,screen=False)
            result.update({"MFPT_source_to_target_HTST":float(forward),"MFPT_target_to_source_HTST":float(reverse),
                           "nu_HTST":float(1/(forward+reverse))})
        result["status"]="complete"
    except Limit as exc:
        result.update({"status":"resource_limit","reason":str(exc)})
    except Exception as exc:
        result.update({"status":"error","exception":repr(exc),"traceback":traceback.format_exc()})
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
        result.update({"last_phase":phase,"total_seconds":time.perf_counter()-st,"singleGT_calls":calls,"progress":progress,
                       "peak_rss_bytes_macos":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
        name=f"pygt_{args.mode}_T{args.temperature}_{args.source}_{args.target}_block{args.block}"+("_dense" if args.dense_core else "")
        (HERE/(name+".json")).write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2),flush=True)
if __name__=="__main__":main()
