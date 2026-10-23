#!/usr/bin/env python3
"""Exact bounded diagnostic of the ABSTRACT rare-sector construction.

This does not simulate or claim a counterexample for the physical bath map.
The all-length proof is MOMENT_COMPARISON_AND_RARE_SECTOR.tex. Large parameters
below use only rational formulas for graph degree; no large graph is allocated.
"""
from __future__ import annotations
from fractions import Fraction as F
from math import comb
from pathlib import Path
import hashlib
import itertools
import json
import time


def ratio(x: F) -> str:
    return f"{x.numerator}/{x.denominator}"


def symbolic_witness(N: int) -> dict:
    # r=1/256, k=N^4 makes h=floor(k^(3/4)/(4 sqrt(r))) exactly 4N^3.
    r=F(1,256)
    k=N**4
    h=4*N**3
    L=2*h
    n=k-L
    assert N >= 16 and k % 2 == 0 and L <= k//2 and n % 2 == 0
    b=r/k
    a=1-b
    w=12*(a*b)**2
    degree=comb(h,2)**2
    lam=w*degree
    row_square=w*lam
    assert F(3*k,65536) <= lam <= F(3*k,256)
    assert row_square <= F(9,64)*r*r/k <= r*r
    assert lam < F(k,2)  # Exact compressed-output-charge spectral interval.
    # Log pressure >= ln(2)*(lambda/(2a)-L)-ln(n+1).
    # If z>=0, ln(2)>1/2 and ln(n+1)<bit_length(k) imply the following
    # fully rational certified lower bound without transcendental numerics.
    z=lam/(2*a)-L
    lower=z/2-k.bit_length() if z>=0 else None
    return {
        "N":N,"k":k,"r":ratio(r),"b":ratio(b),"active_length":L,
        "active_weight":h,"spectator_length":n,"adjacency_degree":degree,
        "block_norm":ratio(w),"negative_perron_magnitude":ratio(lam),
        "lambda_over_k":float(lam/k),"conditional_row_square":ratio(row_square),
        "conditional_row_square_over_r_squared":float(row_square/(r*r)),
        "log_pressure_certified_lower":ratio(lower) if lower is not None else None,
        "certified_divergence_witness":bool(lower is not None and lower>0),
        "large_matrix_allocated":False,
    }


def small_trace_identity() -> dict:
    # A small exact graph check of degeneracy, color-fiber cancellation, and
    # closed-walk traces. This is not an extrapolation establishing the theorem.
    k,L=8,4
    h=L//2
    n=k-L
    active=[u for u in itertools.product((0,1),repeat=L) if sum(u)==h]
    spectators=[v for v in itertools.product((0,1),repeat=n) if sum(v)==n//2]
    A=[[int(sum(x!=y for x,y in zip(u,v))==4) for v in active] for u in active]
    degree=comb(h,2)**2
    assert all(sum(row)==degree for row in A)
    size=len(active)
    Ap=[[int(i==j) for j in range(size)] for i in range(size)]
    traces=[]
    for p in range(1,9):
        Ap=[[sum(Ap[i][t]*A[t][j] for t in range(size))
             for j in range(size)] for i in range(size)]
        tr=sum(Ap[i][i] for i in range(size))
        # Here A is a disjoint union of three edges.
        assert tr==(size if p%2==0 else 0)
        scalar_weight=F(len(spectators)*tr,2**k)
        physical_weight=F(len(spectators)*2**(k//2)*tr,2**(k+k//2))
        assert scalar_weight==physical_weight
        traces.append({"power":p,"trace_A_power":tr,
                       "physical_weighted_trace_without_w":ratio(physical_weight)})
    return {"k":k,"L":L,"active_vertices":size,"spectator_words":len(spectators),
            "color_fiber_dimension":2**(k//2),"degree":degree,"moments":traces}


def main() -> None:
    started=time.perf_counter()
    cases=[symbolic_witness(N) for N in (16,64,512,2048,4096)]
    assert cases[-2]["certified_divergence_witness"]
    assert cases[-1]["certified_divergence_witness"]
    out={
        "status":"PASS",
        "scope":"Abstract block-data counterexample only; not a physical K_zeta",
        "proof":"MOMENT_COMPARISON_AND_RARE_SECTOR.tex",
        "inputs":{"r":"1/256","N":[16,64,512,2048,4096]},
        "small_exact_trace_check":small_trace_identity(),
        "symbolic_large_parameter_checks":cases,
        "observed_script_body_seconds":time.perf_counter()-started,
        "discovery_inference_review_costs":"unknown",
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    target=Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({"status":out["status"],"output":str(target),
        "observed_script_body_seconds":out["observed_script_body_seconds"],
        "positive_exact_pressure_witnesses":[c["N"] for c in cases if c["certified_divergence_witness"]]},indent=2))


if __name__=='__main__':
    main()
