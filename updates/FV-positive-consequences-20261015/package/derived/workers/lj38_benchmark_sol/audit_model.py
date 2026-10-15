"""Audit acquired LJ38 tables; construct sparse, all-saddle HTST component.

This script uses only supplied tables. It does not infer missing transitions or
validate a physical rate model. Conductances omit a common 1/(2*pi), explicitly
retained in metadata, so HTST time = (w/c time)*2*pi.
"""
from pathlib import Path
import hashlib, json, math, resource, sys, time
import numpy as np
from scipy import sparse, special
from scipy.sparse.csgraph import connected_components

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "workers/lj38_acquisition_luna/full-network"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    started = time.perf_counter()
    minima = np.loadtxt(DATA / "min.data")
    saddles = np.loadtxt(DATA / "ts.data")
    parse_s = time.perf_counter() - started
    assert minima.shape == (100000, 6) and saddles.shape == (138888, 8)
    assert np.isfinite(minima).all() and np.isfinite(saddles).all()
    for a in (minima[:, 2], saddles[:, 2], saddles[:, 3:5]):
        assert np.equal(a, np.floor(a)).all()
    assert (minima[:, 2] > 0).all() and (saddles[:, 2] > 0).all()
    endpoints = saddles[:, 3:5].astype(np.int64) - 1
    assert endpoints.min() >= 0 and endpoints.max() < len(minima)
    nonself = endpoints[:, 0] != endpoints[:, 1]
    ep = np.sort(endpoints[nonself], axis=1)
    pairs, inverse, counts = np.unique(ep, axis=0, return_inverse=True, return_counts=True)
    n = len(minima)
    adj = sparse.csr_matrix((np.ones(2*len(pairs)),
           (np.r_[pairs[:,0],pairs[:,1]], np.r_[pairs[:,1],pairs[:,0]])), shape=(n,n))
    nc, labels = connected_components(adj, directed=False)
    sizes = np.bincount(labels)
    retained = labels == sizes.argmax()
    ids = np.flatnonzero(retained)
    remap = np.full(n, -1, dtype=np.int64)
    remap[ids] = np.arange(len(ids))
    pair_keep = retained[pairs[:,0]]
    rp = remap[pairs[pair_keep]]
    ts_keep = nonself & retained[endpoints[:,0]]
    barrier = saddles[:,0,None] - minima[endpoints,0]
    deg = np.diff(adj.indptr)
    terminals = {}
    for fname in ("min.A", "min.B"):
        rows = np.fromstring((DATA / fname).read_text(), dtype=np.int64, sep=" ")
        assert rows[0] == len(rows)-1 and len(np.unique(rows[1:])) == len(rows)-1
        terminals[fname] = {"declared_count":int(rows[0]), "min_id":int(rows[1:].min()),
                           "max_id":int(rows[1:].max()), "retained_count":int(retained[rows[1:]-1].sum())}
    report = {
        "minima":len(minima), "transition_state_rows":len(saddles),
        "files":{f:sha(DATA/f) for f in ("min.data","ts.data","min.A","min.B","pathdata")},
        "parse_seconds":parse_s, "self_transition_rows":int((~nonself).sum()),
        "distinct_nonself_pairs":len(pairs), "parallel_pairs":int((counts>1).sum()),
        "parallel_excess_saddles":int((counts-1).sum()), "max_saddles_for_pair":int(counts.max()),
        "exact_duplicate_full_ts_rows":int(len(saddles)-len(np.unique(saddles,axis=0))),
        "exact_duplicate_full_min_rows":int(len(minima)-len(np.unique(minima,axis=0))),
        "components":int(nc), "largest_component_nodes":len(ids),
        "largest_component_distinct_pairs":int(pair_keep.sum()),
        "largest_component_nonself_saddle_rows":int(ts_keep.sum()),
        "isolated_nodes":int((deg==0).sum()), "component_sizes_largest_20":sorted(sizes.tolist(),reverse=True)[:20],
        "degree_max":int(deg.max()), "degree_percentiles":np.percentile(deg,[0,25,50,75,90,95,99,100]).tolist(),
        "negative_barrier_count":int((barrier<0).sum()), "minimum_barrier":float(barrier.min()),
        "nonself_minimum_barrier":float(barrier[nonself].min()), "nonself_zero_barrier_count":int((barrier[nonself]==0).sum()),
        "max_endpoint_id":int(endpoints.max()+1), "terminal_files":terminals,
        "lowest_energy_minima":[{"id":int(j+1),"energy":float(minima[j,0]),"hessian_log_product":float(minima[j,1]),
                                "point_group_order":int(minima[j,2]),"retained":bool(retained[j])}
                                for j in np.argsort(minima[:,0])[:12]],
        "rate_convention":"k_(j<-i) = (o_i/o_TS)/(2*pi)*exp[(S_i-S_TS)/2-beta*(E_TS-E_i)]; parallel saddles summed; self-transition rows excluded",
        "mass_convention":"w_i = exp[-beta*(E_i-E_0)-(S_i-S_0)/2]/o_i, with E_0,S_0 of archive minimum ID 1",
        "conductance_convention":"c_TS = exp[-beta*(E_TS-E_0)-(S_TS-S_0)/2]/o_TS; omits common 1/(2*pi); pair conductances sum all saddle contributions",
        "mass_policy":"all 71887 states in terminal component retained in component partition function; archive partition also recorded separately; disconnected archive mass is not part of component commute identity",
        "temperatures":{}
    }
    np.savez_compressed(HERE/"audited_tables.npz",minima=minima,saddles=saddles,pairs=pairs,
                        pair_inverse=inverse,nonself=nonself,retained=retained,component_ids=ids,rpairs=rp)
    e0,s0 = minima[0,:2]
    for temp in (0.2, 0.1, 0.05, 0.02):
        beta = 1/temp
        lw = -beta*(minima[:,0]-e0) -(minima[:,1]-s0)/2 -np.log(minima[:,2])
        lc = -beta*(saddles[:,0]-e0) -(saddles[:,1]-s0)/2 -np.log(saddles[:,2])
        lq = -beta*barrier +(minima[endpoints,1]-saddles[:,1,None])/2 +np.log(minima[endpoints,2]/saddles[:,2,None]) -math.log(2*math.pi)
        lzfull = float(special.logsumexp(lw))
        lzcomp = float(special.logsumexp(lw[retained]))
        lzexcluded = float(special.logsumexp(lw[~retained]))
        info = {"beta":beta,"component_log_Z":lzcomp,"archive_log_Z":lzfull,
                "excluded_log_Z":lzexcluded,
                "component_mass_fraction":float(np.exp(lzcomp-lzfull)),
                "excluded_mass_fraction":float(np.exp(lzexcluded-lzfull)),
                "log_w_range":[float(lw.min()),float(lw.max())],
                "log_c_TS_range_nonself":[float(lc[nonself].min()),float(lc[nonself].max())],
                "log_rate_range_nonself":[float(lq[nonself].min()),float(lq[nonself].max())],
                "float64_zero_weights":int((np.exp(lw)==0).sum()),
                "float64_zero_conductances_nonself":int((np.exp(lc[nonself])==0).sum()),
                "float64_zero_rates_nonself":int((np.exp(lq[nonself])==0).sum())}
        report["temperatures"][str(temp)]=info
        if temp in (0.2,0.1):
            c = np.bincount(inverse,weights=np.exp(lc[nonself]),minlength=len(pairs))[pair_keep]
            w = np.exp(lw[retained])
            pairrates = c[:,None]/w[rp]/(2*math.pi)
            # Independent directional HTST sum comparison, before reversibility simplification.
            rr = np.exp(lq[nonself])
            endpoint_order = endpoints[nonself,0] <= endpoints[nonself,1]
            rr = np.where(endpoint_order[:,None],rr,rr[:,::-1])
            qr = np.stack([np.bincount(inverse,weights=rr[:,k],minlength=len(pairs))[pair_keep] for k in (0,1)],axis=1)
            info["max_rate_formula_relative_difference"] = float(np.max(np.abs(pairrates/qr-1)))
            info["component_Z"] = float(math.fsum(w))
            info["component_positive_c_minmax"]=[float(c.min()),float(c.max())]
            np.savez_compressed(HERE/f"model_T{temp}.npz",pairs=rp,c=c,w=w,ids=ids+1,
                                temperature=temp,beta=beta,htst_time_multiplier=2*math.pi,
                                all_archive_log_Z=lzfull,component_log_Z=lzcomp)
    report["total_audit_model_seconds"]=time.perf_counter()-started
    report["peak_rss_bytes_macos"]=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    (HERE/"MODEL_AUDIT.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))

if __name__ == "__main__": main()
