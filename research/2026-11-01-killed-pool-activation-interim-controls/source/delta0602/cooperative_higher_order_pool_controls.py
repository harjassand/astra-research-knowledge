"""All-input killed Green controls for 6A <-> 5A+X <-> 4A+2X <-> 3A+3X.

The two equilibrium edge ratios are incompatible (2 and 7/3), so this is
not a complex-balanced/product-form example. Every fast complex carries 7B.
These are physical-clock finite CME solves, not an asymptotic theorem.
"""
import json, math, hashlib
from pathlib import Path
import numpy as np
from scipy.linalg import solve_banded

ROOT=Path(__file__).resolve().parents[2]


def ff(x,k):
    if x<k:return 0
    return math.prod(range(x-k+1,x+1))


def solve(N, minimum_A=2, m=4):
    # Directed rate pairs for all neighboring complexes A^j X^(m-j).
    a=np.arange(minimum_A,N+1,dtype=float)
    count=len(a); x=N-a; B=m+1; catalyst=ff(B,B)
    up=np.zeros(count);down=np.zeros(count)
    for j in range(minimum_A,m):
        k_up=(2.,7.,11.,17.,23.)[j-minimum_A]
        k_down=(1.,3.,5.,13.,19.)[j-minimum_A]
        up += k_up*np.array([ff(int(t),j)*ff(int(N-t),m-j) for t in a],float)
        down += k_down*np.array([ff(int(t),j+1)*ff(int(N-t),m-j-1) for t in a],float)
    up*=catalyst;down*=catalyst
    clear=catalyst*np.array([ff(int(t),m) for t in a],float)
    act=B*a;imm=np.ones(count)
    scale=catalyst*N**m
    band=np.zeros((3,count))
    band[0,1:]=-up[:-1]/scale
    band[2,:-1]=-down[1:]/scale
    band[1,:]=(up+down+clear+act+imm)/scale
    reward=np.array([math.prod(1/(1+b*(t-m+b)) for b in range(1,m+1)) if t>=m else 0 for t in a])
    rhs=np.column_stack([np.ones(count)/scale,a/scale,clear/scale,act/scale,imm/scale,
                         clear*reward/scale] +
                         [clear*np.where(a>=m,(1+np.maximum(a-m,0))**(-j),0)/scale for j in range(1,m+1)])
    val=solve_banded((1,1),band,rhs)
    applied=band[1,:,None]*val
    applied[:-1]+=band[0,1:,None]*val[1:]
    applied[1:]+=band[2,:-1,None]*val[:-1]
    residual=float(np.max(abs(applied-rhs)))
    probability_error=float(np.max(abs(val[:,2:5].sum(axis=1)-1)))
    assert residual<1e-10 and probability_error<2e-8 and val.min()>-1e-12
    ratio=val[:,0]/val[:,1]
    incoming=val[:,5]/val[:,3]
    carry=[float(np.max(val[:,6+j]*(1+a)**(j+1))) for j in range(m)]
    return {"N":N,"minimum_A":minimum_A,"m":m,"states":count,
            "max_time_to_occupation_ratio":float(ratio.max()),
            "ratio_times_logN":float(ratio.max()*math.log(N)),
            "max_terminal_reward_to_activation_ratio":float(incoming.max()),
            "reward_ratio_times_logN":float(incoming.max()*math.log(N)),
            "max_carried_inverse_moment_amplification":carry,
            "all_input_probability_sum_error":probability_error,"linear_residual":residual,
            "lowest_active_input":{"T":float(val[0,0]),"U":float(val[0,1]),
                                  "P_clear":float(val[0,2]),"P_activation":float(val[0,3]),
                                  "incoming_up_reward":float(val[0,5])}}


def main():
    rows=[]
    for minimum_A,m,pops in ((3,6,(32,64,128,256,512,1024,2048,4096)),):
        for n in pops:
            row=solve(n,minimum_A,m);rows.append(row)
            print(json.dumps({k:row[k] for k in ("N","minimum_A","max_time_to_occupation_ratio",
                 "max_terminal_reward_to_activation_ratio","max_carried_inverse_moment_amplification")}),flush=True)
    result={"status":"PASS finite all-input killed controls", "rows":rows,
            "scope":"No global recurrence proof or asymptotic constant inferred from finite solves.",
            "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/"outputs/mechanism_selection_20261101/cooperative_higher_order_pool_controls.json").write_text(json.dumps(result,indent=2)+"\n")


if __name__=="__main__":main()
