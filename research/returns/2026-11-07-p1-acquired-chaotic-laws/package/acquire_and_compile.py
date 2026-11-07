"""Data-only certificate and later-task compiler.

Reads contract.json and observations.npz. Does not import make_experiment or
read SOURCE_CHECK.json. All acceptance inequalities use integer/Fraction
arithmetic. Decimal fields are explanatory displays, never acceptance gates.
"""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import hashlib
import json
import time
import numpy as np
from exact_core import (eye,matmul,matpow,matrix_minus,determinant,
                        GridResidual,orbit_compile,cat_entropy_interval)

ROOT=Path(__file__).resolve().parent


def principal(nums, denominator):
    return (nums+denominator//2)%denominator-denominator//2


def main():
    started=time.perf_counter()
    contract=json.loads((ROOT/"contract.json").read_text())
    d=contract["dimension"]
    q=contract["grid_side"]
    steps=contract["loop_steps"]
    Q=contract["output_denominator"]
    eta=F(contract["effective_euclidean_error"])
    B,M2,M3=(F(contract[k]) for k in ("B","M2","M3"))
    assert d==4, "This executed verifier uses the exact sqrt(d)=2 shortcut."
    assert B/steps+2*eta<F(1,2)
    assert B/q+2*eta<F(1,2)
    data=np.load(ROOT/"observations.npz")
    grid=data["grid"].astype(np.int64)
    loops=data["loops"].astype(np.int64)
    assert grid.shape==(q,)*d+(d,)
    assert loops.shape==(d,steps,d)
    columns=[]
    for j in range(d):
        ys=loops[j]
        increments=principal(np.roll(ys,-1,axis=0)-ys,Q)
        winding=increments.sum(axis=0)
        assert np.all(winding%Q==0)
        columns.append(winding//Q)
        for k in range(steps):
            if k*q%steps==0:
                idx=[0]*d
                idx[j]=(k*q//steps)%q
                assert np.array_equal(ys[k],grid[tuple(idx)])
    A=np.stack(columns,axis=1).astype(np.int64)
    a=A.tolist()
    assert np.array_equal(A,A.T)
    assert abs(determinant(a))==1
    # Certificate computed from the learned integer matrix; no source import.
    assert matmul(a,a)==[[3*a[i][j]-int(i==j) for j in range(d)] for i in range(d)]
    assert sum(a[i][i] for i in range(d))==6
    C,J=F(9,4),F(21,8)
    # Polynomial identity gives eigenvalues (3+-sqrt(5))/2. Certify bounds.
    assert C*C>5
    assert (2*J-3)**2>5 and 2*J-3>0
    b=[F(int(z),Q) for z in grid[(0,)*d]]
    residual=np.zeros_like(grid,dtype=np.int64)
    # Spanning tree; error telescopes. Lexicographic predecessors are earlier.
    for idx in np.ndindex((q,)*d):
        if not any(idx):
            continue
        j=next(j for j,v in enumerate(idx) if v)
        prev=list(idx)
        prev[j]-=1
        prev=tuple(prev)
        inc=principal(grid[idx]-grid[prev],Q)-A[:,j]*(Q//q)
        residual[idx]=residual[prev]+inc
    for j in range(d):
        inc=principal(np.roll(grid,-1,axis=j)-grid,Q)-A[:,j]*(Q//q)
        assert np.array_equal(inc,np.roll(residual,-1,axis=j)-residual)
    # All noise is retained. A rigorous Frobenius upper bound is enough here.
    frob_squared=np.zeros((q,)*d,dtype=np.int64)
    max_entry=0
    for j in range(d):
        dif=np.roll(residual,-1,axis=j)-np.roll(residual,1,axis=j)
        max_entry=max(max_entry,int(np.abs(dif).max()))
        assert d*d*max_entry*max_entry < 2**63
        frob_squared+=(dif*dif).sum(axis=-1)
    max_square=int(frob_squared.max())
    root=isqrt(max_square)
    if root*root<max_square:
        root+=1
    beta=F(root*q,2*Q)
    ell=beta+2*(M3/F(6*q*q)+eta*q)+M2/F(q)
    ell_hat=ell+M2*F(d,q)+4*eta*q
    delta=eta+M2*F(d,2*q*q)
    assert C*max(ell,ell_hat)<1
    assert J*max(ell,ell_hat)<1
    D=C*delta/(1-C*ell)
    nu=F(1,8)
    assert C*(max(ell,ell_hat)+nu)<1
    assert J*(max(ell,ell_hat)+nu)<1
    D_feedback=C*delta/(1-C*(ell+nu))
    np.savez_compressed(ROOT/"surrogate.npz",residual=residual,A=A,b=np.array(grid[(0,)*d]),Q=np.array(Q))
    lo,hi=cat_entropy_interval()
    counts={}
    for m in [1,2,3,4,5,6,7,10,13,31,100]:
        counts[str(m)]=abs(determinant(matrix_minus(matpow(a,m),eye(d))))
    residual_fn=GridResidual(residual,Q)
    tasks=[(1,[0,0,0,0]),(3,[1,0,0,0]),(7,[0,1,1,0]),
           (13,[1,2,3,4]),(31,[7,11,13,17])]
    orbits=[]
    for m,label in tasks:
        orbit=orbit_compile(a,b,residual_fn,m,label,C*ell_hat,F(1,10**12),bits=60)
        orbit["source_orbit_error_bound"]=str(D+F(orbit["algorithm_error_bound"]))
        orbit["source_orbit_error_decimal"]=float(D+F(orbit["algorithm_error_bound"]))
        orbits.append(orbit)
        print(json.dumps({"period":m,"least_period":orbit["least_period"],
                          "iterations":orbit["iterations"],
                          "algorithm_error":orbit["algorithm_error_decimal"]}),flush=True)
    (ROOT/"PERIODIC_ORBITS.json").write_text(json.dumps(orbits,indent=2)+"\n")
    certificate={"A":a,"affine_offset_from_report":[str(z) for z in b],
        "query_count":contract["unique_one_step_queries"],
        "scalar_reports":contract["returned_scalar_count"],
        "integer_grid_cycle_check":True,"homology_exact":True,
        "symmetric_hyperbolicity_polynomial":"A^2-3A+I=0, A symmetric, trace A=6, det A=1",
        "constants":{key:{"rational":str(value),"decimal":float(value)}
                     for key,value in {"beta":beta,"ell":ell,"ell_hat":ell_hat,
                        "C":C,"J":J,"delta":delta,"orbit_correspondence_D":D,
                        "feedback_Lipschitz_allowance":nu,"feedback_correspondence_D":D_feedback,
                        "surrogate_contraction_factor":C*ell_hat}.items()},
        "entropy":{"exact":"2 log((3+sqrt(5))/2)","rational_lower":str(lo),
                   "rational_upper":str(hi),"decimal":float((lo+hi)/2)},
        "fixed_point_counts":counts,
        "max_executed_period":max(t[0] for t in tasks),
        "all_requested_addresses_certified":True,
        "observation_sha256":hashlib.sha256((ROOT/"observations.npz").read_bytes()).hexdigest(),
        "surrogate_sha256":hashlib.sha256((ROOT/"surrogate.npz").read_bytes()).hexdigest(),
        "wall_seconds":time.perf_counter()-started,
        "scope":"Synthetic acquisition, exact finite arithmetic certificate, and finite set of compiled addresses. General all-period guarantee is the accompanying proof."}
    (ROOT/"EXECUTED_CERTIFICATE.json").write_text(json.dumps(certificate,indent=2)+"\n")
    print(json.dumps({"A":a,"ell":float(ell),"ell_hat":float(ell_hat),
                      "D":float(D),"D_feedback":float(D_feedback),
                      "entropy":float((lo+hi)/2),"counts":counts,
                      "learner_seconds":certificate["wall_seconds"]}),flush=True)


if __name__=="__main__":
    main()
