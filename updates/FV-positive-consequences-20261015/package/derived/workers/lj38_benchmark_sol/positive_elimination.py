"""Classical stable positive star-mesh elimination, carrying all node masses.

For reversible CTMC conductance c and mass w, eliminating k gives
  c_ij <- c_ij + c_ik*c_kj/sum_l c_kl,
  w_j <- w_j + w_k*c_kj/sum_l c_kl.
At two terminals c_st=C, transformed w_s=N_st, w_t=Z-N_st. This is
classical reversible graph transformation, not the candidate algorithm.
Only bounded sparse dictionaries are used; no dense full graph is allocated.
"""
from pathlib import Path
import argparse,heapq,json,math,resource,time
import numpy as np

HERE=Path(__file__).resolve().parent

def eliminate(pairs,c,w,source,target,seconds=55.,edge_cap=2000000,dtype="float64",save_prefix=None,return_core=False,keep_extra=(),record=False):
    started=time.perf_counter()
    typ = np.longdouble if dtype=="longdouble" else float
    w=np.array(w,dtype=np.longdouble if dtype=="longdouble" else np.float64,copy=True)
    z0=np.sum(w,dtype=np.longdouble)
    n=len(w); adj=[{} for _ in range(n)]
    for (i,j),v in zip(pairs,c):
        adj[int(i)][int(j)]=typ(v); adj[int(j)][int(i)]=typ(v)
    edges=len(pairs); live=np.ones(n,dtype=bool)
    keep_set=set(keep_extra)|{source,target}
    heap=[(len(adj[k]),k) for k in range(n) if k not in keep_set]
    heapq.heapify(heap)
    setup_s=time.perf_counter()-started
    removed=0; updates=0; inserted=0; max_degree=0; peak_edges=edges;records=[]
    snapshots=[]; next_snapshot=2.
    status="complete"
    while heap:
        degree,k=heapq.heappop(heap)
        if not live[k] or degree!=len(adj[k]): continue
        elapsed=time.perf_counter()-started
        if elapsed>seconds or edges>edge_cap:
            status="time_limit" if elapsed>seconds else "edge_memory_limit"
            break
        neighbors=list(adj[k].items()); d=len(neighbors)
        max_degree=max(max_degree,d)
        if not d: raise ValueError("Disconnected retained component")
        den = sum((v for _,v in neighbors),typ(0)) if dtype=="longdouble" else math.fsum(v for _,v in neighbors)
        if record:
            records.append((k,np.array([j for j,_ in neighbors],dtype=np.int64),
                            np.array([v/den for _,v in neighbors]),w[k]/den))
        # Assign both symmetric copies from one rounded arithmetic operation.
        for ai,(i,ci) in enumerate(neighbors):
            w[i]+=w[k]*(ci/den)
            del adj[i][k]
            for j,cj in neighbors[ai+1:]:
                addition=min(ci,cj)*(max(ci,cj)/den)
                old=adj[i].get(j)
                value=addition if old is None else old+addition
                adj[i][j]=value; adj[j][i]=value
                updates+=1
                if old is None:
                    edges+=1; inserted+=1
        edges-=d
        adj[k].clear(); live[k]=False; w[k]=0
        for j,_ in neighbors:
            if j not in keep_set: heapq.heappush(heap,(len(adj[j]),j))
        removed+=1; peak_edges=max(peak_edges,edges)
        if elapsed>=next_snapshot:
            row={"seconds":elapsed,"remaining_nodes":int(n-removed),"edges":edges,
                 "current_degree":d,"max_elimination_degree":max_degree,"pair_updates":updates}
            snapshots.append(row); print(json.dumps(row),flush=True); next_snapshot=elapsed+2.
    elapsed=time.perf_counter()-started
    result={"status":status,"dtype":dtype,"source_component_index":source,"target_component_index":target,
            "seconds":elapsed,"graph_setup_seconds":setup_s,"initial_nodes":n,"initial_edges":len(pairs),
            "remaining_nodes":int(live.sum()),"remaining_edges":edges,"removed_nodes":removed,
            "pair_updates":updates,"new_fill_pairs":inserted,"max_elimination_degree":max_degree,
            "peak_edges":peak_edges,"initial_mass":str(z0),
            "final_mass":str(np.sum(w,dtype=np.longdouble)),
            "relative_mass_drift":float(np.sum(w,dtype=np.longdouble)/z0-1),
            "peak_rss_bytes_macos":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "limits":{"seconds":seconds,"undirected_edges":edge_cap},"progress":snapshots}
    if status=="complete" and len(keep_set)==2:
        cap=adj[source][target]
        factor=typ(2*np.pi)
        result.update({"capacity_omitting_1_over_2pi":str(cap),"N_source_to_target":str(w[source]),
                       "N_target_to_source":str(w[target]),"nu_HTST":str(cap/z0/factor),
                       "MFPT_source_to_target_HTST":str(w[source]/cap*factor),
                       "MFPT_target_to_source_HTST":str(w[target]/cap*factor),
                       "commute_HTST":str(z0/cap*factor),
                       "directional_sum_relative_to_commute":float((w[source]+w[target])/z0-1)})
    if save_prefix or return_core:
        keep=np.flatnonzero(live); remap=np.full(n,-1,dtype=np.int64); remap[keep]=np.arange(len(keep))
        rp=[]; rc=[]
        for i in keep:
            for j,ci in adj[i].items():
                if i<j: rp.append((remap[i],remap[j])); rc.append(ci)
        core={"pairs":np.array(rp,dtype=np.int64),"c":np.array(rc),"w":w[keep],
              "component_indices":keep,"source":remap[source],"target":remap[target]}
        if record:core["records"]=records
        if save_prefix: np.savez_compressed(str(save_prefix)+".npz",**core)
        if return_core: return result,core
    return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--temperature",default="0.2")
    ap.add_argument("--source",type=int,default=1); ap.add_argument("--target",type=int,default=2)
    ap.add_argument("--seconds",type=float,default=55.); ap.add_argument("--edge-cap",type=int,default=2000000)
    ap.add_argument("--dtype",choices=("float64","longdouble"),default="float64")
    ap.add_argument("--checkpoint",action="store_true")
    args=ap.parse_args(); st=time.perf_counter()
    model=np.load(HERE/f"model_T{args.temperature}.npz")
    source=int(np.flatnonzero(model["ids"]==args.source)[0]); target=int(np.flatnonzero(model["ids"]==args.target)[0])
    name=f"positive_T{args.temperature}_{args.source}_{args.target}_{args.dtype}"
    result=eliminate(model["pairs"],model["c"],model["w"],source,target,args.seconds,args.edge_cap,args.dtype,
                     HERE/(name+"_checkpoint") if args.checkpoint else None)
    result.update({"archive_source_id":args.source,"archive_target_id":args.target,"temperature":float(args.temperature),
                   "load_and_elimination_seconds":time.perf_counter()-st,
                   "method":"classical positive conductance graph transformation with mass transfer and dynamic minimum degree"})
    (HERE/(name+".json")).write_text(json.dumps(result,indent=2)+"\n"); print(json.dumps(result,indent=2),flush=True)
if __name__=="__main__": main()
