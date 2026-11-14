"""Actual CLN025 rate controls for static, timed, and binned representations.

The reversible one-dimensional MSM is an incumbent-style approximation, not a
validated molecular generator. Basin initial distributions differ slightly from
the direct first-arrival reference; all finite-record conventions are retained.
"""
from pathlib import Path
import json
import time
import numpy as np
from replay_kinetics import load_reference, complete_intervals, DT_US

HERE = Path(__file__).resolve().parent


def reversible_msm(records, bins, lag):
    n = bins+2
    counts = np.zeros((n,n),dtype=np.float64)
    for record in records:
        q = record["committor"]
        index = 1+np.minimum(bins-1,np.maximum(0,np.floor(q*bins).astype(int)))
        index[record["states"]=="A"] = 0
        index[record["states"]=="B"] = n-1
        counts += np.bincount(index[:-lag]*n+index[lag:],minlength=n*n).reshape(n,n)
    counts = (counts+counts.T)/2
    active = counts.sum(axis=1)>0
    assert active[0] and active[-1]
    c = counts[np.ix_(active,active)]
    p = c/c.sum(axis=1,keepdims=True)
    rates = []
    for source,target in [(0,len(c)-1),(len(c)-1,0)]:
        transient = np.array([i for i in range(len(c)) if i!=target])
        mfpt = np.linalg.solve(np.eye(len(transient))-p[np.ix_(transient,transient)],
                               np.full(len(transient),lag*DT_US))
        rates.append(float(1/mfpt[np.flatnonzero(transient==source)[0]]))
    return {"committor_bins":bins,"lag_ns":lag*DT_US*1000,
            "kAB_per_us":rates[0],"kBA_per_us":rates[1],
            "assumption":"Reversible Markov closure on supplied learned committor plus explicit basin labels; not independently certified."}


started=time.perf_counter()
records=load_reference()
ab,ba,_=complete_intervals(records)
reference=[float(1/ab.mean()),float(1/ba.mean())]
msm=[]
for bins in [10,30,100]:
    for lag in [1,10,100,1000]:
        row=reversible_msm(records,bins,lag)
        row["kAB_over_direct"]=row["kAB_per_us"]/reference[0]
        row["kBA_over_direct"]=row["kBA_per_us"]/reference[1]
        msm.append(row)

# Preserve the entire static ensemble exactly and remove only time ordering.
# This is an information control, not a plausible physical molecular dynamics.
rng=np.random.default_rng(20261015)
shuffled=[]
for record in records:
    permutation=rng.permutation(len(record["states"]))
    shuffled.append({"name":record["name"],"states":record["states"][permutation],
                     "committor":record["committor"][permutation]})
    assert np.array_equal(np.sort(shuffled[-1]["committor"]),np.sort(record["committor"]))
sa,sb,events=complete_intervals(shuffled)
result={"scope":"Actual high-dimensional molecular MD records as inputs; controls change representations only, not new physical evidence.",
        "direct_reference_per_us":{"kAB":reference[0],"kBA":reference[1]},
        "reversible_committor_msm":msm,
        "same_static_ensemble_time_order_removed":{"kAB_per_us":float(1/sa.mean()),
                                                 "kBA_per_us":float(1/sb.mean()),
                                                 "observed_switches":sum(e["n_observed_switches"] for e in events),
                                                 "all_committor_values_preserved_exactly":True,
                                                 "physical_dynamics_claim":False},
        "same_geometric_paths_clock_scaled_by_10":{"kAB_per_us":reference[0]/10,
                                                   "kBA_per_us":reference[1]/10,
                                                   "coordinates_and_committor_unchanged":True,
                                                   "physical_settings_changed_or_unspecified":True},
        "compute_seconds":time.perf_counter()-started}
(HERE/"CLOCK_REPRESENTATION_CONTROLS.json").write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
