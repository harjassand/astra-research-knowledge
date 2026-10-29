#!/usr/bin/env python3
"""Individual native excursions; no aggregate Binomial acquisition."""
from pathlib import Path
from fractions import Fraction
import hashlib,json,time,sys
import numpy as np
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"run"
N=1<<18
SEED=202610290701
SCALE=1<<20

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    start_time=time.perf_counter()
    rng=np.random.default_rng(SEED)
    # PRIVATE synthetic source: 5 ports, two hidden stars per cycle edge.
    # Each hidden star has weight16/15, forward entrance5/8, exit3/8.
    # Rate at each hidden state is1; rate at each port is32/15.
    p=5/8
    start=rng.integers(0,5,size=N,dtype=np.uint8)
    neighbor_sign=np.where(rng.integers(0,2,size=N)==0,-1,1)
    neighbor=((start.astype(np.int64)+neighbor_sign)%5).astype(np.uint8)
    native_hold=rng.exponential(scale=15/32,size=N)
    primary_star=rng.random(N)<p
    tau=rng.exponential(scale=1,size=N)
    self_return=rng.random(N)<np.where(primary_star,1-p,p)
    end=np.where(self_return,start,neighbor).astype(np.uint8)
    hold_hi=np.floor(native_hold*SCALE).astype(np.uint64)+1
    duration_hi=np.floor(tau*SCALE).astype(np.uint64)+1
    path=OUT/"native_record.npz"
    np.savez_compressed(path,start_port=start,end_port=end,
        native_hold_upper_ticks=hold_hi,interior_duration_upper_ticks=duration_hi)
    public={
      "version":"native-copositive-score-v1",
      "ports":5,
      "reversal":"All microscopic states are even; standard stationary CTMC reversal.",
      "source_class":"Finite irreducible stationary CTMC; each named port is one native state.",
      "preparation":"Independent exact reset to the sampled named port.",
      "selection":"Each port chosen uniformly; calibrated stationary departure fluxes are equal.",
      "port_weights_up_to_scale":["1"]*5,
      "native_port_rates":["32/15"]*5,
      "record":"One uninterrupted native state-changing departure and first return to the port set; direct returns would have zero interior time.",
      "zero_duration_direct_jump_mark":"A direct port jump has a separately resolved zero-tick marker; positive interior excursions have upper_ticks>=1. This fixture happens to produce no direct jumps.",
      "timestamp":"Each positive duration belongs to [(upper_ticks-1)/scale, upper_ticks/scale].",
      "timestamp_scale":SCALE,
      "interior_tail_contract":"P(tau>t)<=exp(-t/2) for every reset port and all t>=0.",
      "tail_purpose":"Needed only to convert per-departure entropy into entropy per time, not for the bounded-bin witness.",
      "predeclared_window":["0","1"],
      "predeclared_H":"H_ii=1, H_ij=-1 on a five-cycle, H_ij=1 otherwise.",
      "confidence_score_failure":"1/2000",
      "confidence_mean_failure":"1/2000",
      "mean_truncation":"24",
      "acquired_trials":N,
      "native_preparations":N,
      "physics_scope":"Synthetic numerical source; no physical experiment or independently acquired calibration."
    }
    (OUT/"PUBLIC_CONTRACT.json").write_text(json.dumps(public,indent=2)+"\n")
    private={
      "source_family":"Two mirror hidden stars per edge of a 5-cycle",
      "p":"5/8","q":"3/8","hidden_weight":"16/15","hidden_count":10,
      "hidden_rate":"1","port_count":5,"port_weight":"1","port_rate":"32/15",
      "total_stationary_weight":"47/3","total_departure_flux":"32/3",
      "M_diagonal":"1","M_adjacent":"17/30","M_nonadjacent":"0",
      "entropy_unnormalized":"(16/3)*log(5/3)",
      "entropy_rate":"(16/47)*log(5/3)",
      "entropy_per_departure":"(1/2)*log(5/3)"
    }
    (OUT/"PRIVATE_SOURCE.json").write_text(json.dumps(private,indent=2)+"\n")
    receipt={
      "version":"individual-native-producer-v1","rng":"NumPy default_rng PCG64",
      "seed":SEED,"numpy_version":np.__version__,"python_version":sys.version.split()[0],
      "individual_native_trials":N,"individual_reset_preparations":N,
      "individual_native_jumps":2*N,
      "native_port_clock_units":float(native_hold.sum()),
      "native_interior_clock_units":float(tau.sum()),
      "total_native_clock_units":float(native_hold.sum()+tau.sum()),
      "maximum_native_interior_time":float(tau.max()),
      "observed_self_returns":int(self_return.sum()),
      "source_scalar_random_variates":6*N,
      "random_draw_accounting":"N reset labels, N neighboring-edge choices, N initial holding exponentials, N hidden-star Bernoulli choices, N interior exponentials, N exit Bernoulli choices; every individual draw executed.",
      "native_record_bytes":path.stat().st_size,
      "native_record_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
      "producer_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      "software_wall_seconds":time.perf_counter()-start_time,
      "sampling_scope":"Ordinary floating exponential/uniform sampling; not a complete floating-law proof, physical assay, or independent validation of the supplied reset/clock/tail warranties."
    }
    (OUT/"PRODUCER_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,indent=2))
if __name__=="__main__":main()

