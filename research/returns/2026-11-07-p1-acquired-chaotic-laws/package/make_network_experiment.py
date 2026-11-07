"""SOURCE-AWARE generation of 32 independent two-coordinate acquisitions.

Distinct source offsets, amplitudes and phases; each module pays its own
queries. The learner does not read this file or its source checks.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import time
import numpy as np
from make_experiment import sine_integer_table
from exact_core import floor

ROOT=Path(__file__).resolve().parent
N=32
q=16
steps=32
Q=1<<30
A=np.array([[2,1],[1,1]],dtype=np.int64)


def main():
    start=time.perf_counter()
    tables=[sine_integer_table(F(j,32768))[0] for j in range(1,6)]
    grid=np.indices((q,q),dtype=np.int64).reshape(2,-1).T*2
    obs=[]
    loopobs=[]
    sources=[]
    native_evaluations=0
    for module in range(N):
        b=[F(1,7+2*module),F(1,101+2*module)]
        table=tables[module%5]
        def read(z):
            nonlocal native_evaluations
            native_evaluations+=len(z)
            affine=(z@A.T)*(Q//32)+np.array([floor(t*Q+F(1,2)) for t in b],dtype=np.int64)
            phase=np.column_stack([(z[:,0]+z[:,1]+module)%32,
                                    (z[:,0]-z[:,1]+2*module)%32])
            code=z@np.array([47,1031],dtype=np.int64)+module*1009
            errors=np.column_stack([((code*(71+2*j)+(j+1)*331)%2049)-1024 for j in range(2)])
            return ((affine+table[phase]+errors)%Q).astype(np.uint32)
        component_grid=read(grid).reshape(q,q,2)
        obs.append(component_grid)
        loops=[]
        for j in range(2):
            ys=np.empty((steps,2),dtype=np.uint32)
            ys[::2]=component_grid[tuple(slice(None) if axis==j else 0 for axis in range(2))]
            z=np.zeros((steps//2,2),dtype=np.int64)
            z[:,j]=2*np.arange(steps//2)+1
            ys[1::2]=read(z)
            loops.append(ys)
        loopobs.append(np.stack(loops))
        sources.append({"module":module,"offset":[str(z) for z in b],
                        "sine_amplitude":str(F(module%5+1,32768)),"phase_index":module})
    np.savez_compressed(ROOT/"network_observations.npz",grids=np.stack(obs),loops=np.stack(loopobs))
    count=N*(q*q+2*(steps//2))
    assert native_evaluations==count
    contract={"modules":N,"component_dimension":2,"grid_side":q,"loop_steps":steps,
        "output_denominator":Q,"B":"3","M2":"1/10","M3":"3/4",
        "effective_euclidean_error":"1/262144","unique_one_step_queries":count,
        "returned_scalar_count":2*count,
        "channel":"independent exact software preparation and finite noisy full state readout for each module",
        "joint_state_queries":0,"known_later_coupling":"v_i=(triangle(x_(i-1,0)),triangle(x_(i+1,1)))/16 on a ring; triangle(t)=dist(t,Z)-1/4",
        "known_coupling_block_row_Lipschitz":"1/8"}
    (ROOT/"network_contract.json").write_text(json.dumps(contract,indent=2)+"\n")
    gamma=F(5,32768)
    two_pi=F(44,7)
    assert F(21,8)+2*gamma*two_pi*F(10,7)<3
    assert 2*gamma*two_pi**2*2<F(1,10)
    assert 2*gamma*two_pi**3*2*F(10,7)<F(3,4)
    assert F(3,2)*F(1025,Q)<F(1,262144)
    checks={"true_A":A.tolist(),"modules":sources,
        "sine_rounding":"The same rational Machin/Taylor enclosure routine is used for each of the five amplitudes.",
        "derivative_guards_checked":True,"noise_guard_checked":True,
        "all_components_acquired_separately":True,"unique_queries":count,
        "executed_native_forward_evaluations":native_evaluations,
        "joint_state_queries":0,"wall_seconds":time.perf_counter()-start,
        "observation_sha256":hashlib.sha256((ROOT/"network_observations.npz").read_bytes()).hexdigest()}
    (ROOT/"NETWORK_SOURCE_CHECK.json").write_text(json.dumps(checks,indent=2)+"\n")
    print(json.dumps({"modules":N,"state_dimension":2*N,"queries":count,
                      "joint_state_queries":0,"seconds":checks["wall_seconds"]}))


if __name__=="__main__":
    main()
