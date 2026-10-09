#!/usr/bin/env python3
"""Exact-rational finite-chain check for the N27 controller example.

No simulation or floating-point stationary solve is used here.  It verifies
the rational stationary distributions and the stated strict inequalities for
the evidence-crossing controller against sitewise and positive-run controls.
The model remains synthetic; exact arithmetic validates only these equations.
"""

from fractions import Fraction as F
from itertools import product


P = {
    "a": F(1,200), "b": F(1,50),
    "eg": F(1,10000), "eb": F(1,10),
    "s": F(4,5), "f": F(1,5),
    "rho": F(3,5), "delta": F(1,5), "eta": F(49,50),
    "t0": F(1), "tpatch": F(2,5), "treset": F(1),
}
L=3
NM=1<<L
N=2*NM


def stationary_exact(T):
    """Exact pi solving pi*T=pi, sum(pi)=1 by rational Gauss-Jordan."""
    A=[[T[j][i]-(F(1) if i==j else F(0)) for j in range(N)] for i in range(N)]
    A[-1]=[F(1) for _ in range(N)]
    rhs=[F(0) for _ in range(N)]
    rhs[-1]=F(1)
    for col in range(N):
        pivot=next((r for r in range(col,N) if A[r][col]),None)
        if pivot is None:
            raise ArithmeticError("stationary system singular")
        A[col],A[pivot]=A[pivot],A[col]
        rhs[col],rhs[pivot]=rhs[pivot],rhs[col]
        scale=A[col][col]
        A[col]=[v/scale for v in A[col]]
        rhs[col]/=scale
        for r in range(N):
            if r==col: continue
            c=A[r][col]
            if c:
                A[r]=[A[r][j]-c*A[col][j] for j in range(N)]
                rhs[r]-=c*rhs[col]
    pi=rhs
    assert sum(pi)==1
    assert all(v>=0 for v in pi)
    assert all(sum(pi[i]*T[i][j] for i in range(N))==pi[j] for j in range(N))
    return pi


def evaluate(policy):
    if len(policy)!=2*NM or any(a not in (0,1) for a in policy):
        raise ValueError("expected a deterministic three-cue controller")
    T=[[F(0) for _ in range(N)] for _ in range(N)]
    rewards={k:[F(0) for _ in range(N)] for k in
             ("errors","dntp","patches","resets","q_initial","false_cue",
              "true_cue","missed_error","reset_bad","reset_good","reset_success",
              "reset_reverse")}
    for x,mem,e,z in product((0,1),range(NM),(0,1),(0,1)):
        i=x*NM+mem
        eprob=P["eb"] if x else P["eg"]
        pe=eprob if e else 1-eprob
        pplus=(P["s"] if e else P["f"])
        pz=pplus if z else 1-pplus
        obs=pe*pz
        alarm=policy[2*mem+z]
        if alarm:
            reset=((1,P["delta"]),(0,1-P["delta"])) if x==0 else ((0,P["rho"]),(1,1-P["rho"]))
        else:
            reset=((x,F(1)),)
        next_mem=((mem<<1)|z)&(NM-1)
        for xp,pr in reset:
            mass=obs*pr
            repl=P["eb"] if xp else P["eg"]
            final=(P["eta"]*repl+(1-P["eta"])*e) if z else F(e)
            rewards["errors"][i]+=mass*final
            rewards["dntp"][i]+=mass*(1+P["eta"]*z)
            rewards["patches"][i]+=mass*z
            rewards["resets"][i]+=mass*alarm
            rewards["q_initial"][i]+=mass*e
            rewards["false_cue"][i]+=mass*int(z==1 and e==0)
            rewards["true_cue"][i]+=mass*int(z==1 and e==1)
            rewards["missed_error"][i]+=mass*int(z==0 and e==1)
            rewards["reset_bad"][i]+=mass*int(alarm and x==1)
            rewards["reset_good"][i]+=mass*int(alarm and x==0)
            rewards["reset_success"][i]+=mass*int(alarm and x==1 and xp==0)
            rewards["reset_reverse"][i]+=mass*int(alarm and x==0 and xp==1)
            trans=((1,P["a"]),(0,1-P["a"])) if xp==0 else ((0,P["b"]),(1,1-P["b"]))
            for xn,pt in trans:
                T[i][xn*NM+next_mem]+=obs*pr*pt
    assert all(sum(row)==1 for row in T)
    pi=stationary_exact(T)
    out={name:sum(pi[i]*v[i] for i in range(N)) for name,v in rewards.items()}
    out["time"]=P["t0"]+P["tpatch"]*out["patches"]+P["treset"]*out["resets"]
    out["atp"]=out["patches"]+out["resets"]
    return out


def sitewise():
    return tuple(z for mem in range(NM) for z in (0,1))


def burst_repeated(k):
    out=[]
    for mem in range(NM):
        bits=[(mem>>j)&1 for j in reversed(range(L))]
        for z in (0,1):
            out.append(int(z==1 and all((bits+[z])[-k:])))
    return tuple(out)


def burst_one_shot(k):
    out=[]
    for mem in range(NM):
        bits=[(mem>>j)&1 for j in reversed(range(L))]
        for z in (0,1):
            seq=bits+[z]
            reached=z==1 and all(seq[-k:])
            was_reached=len(bits)>=k and all(bits[-k:])
            out.append(int(reached and not was_reached))
    return tuple(out)


def main():
    # Posterior-crossing truth table: trigger when the four-cue pattern has
    # three positives and the previous three-cue window was below threshold.
    # State/index order is (oldest-to-newest 3-bit memory,current cue).
    candidate=tuple(int(2*mem+z in (7,11,13)) for mem in range(NM) for z in (0,1))
    cases={
        "candidate_3of4_crossing":candidate,
        "sitewise_each_plus":sitewise(),
        "burst_1plus_one_shot":burst_one_shot(1),
        "burst_2plus_repeated":burst_repeated(2),
        "burst_2plus_one_shot":burst_one_shot(2),
        "burst_3plus_repeated":burst_repeated(3),
        "burst_3plus_one_shot":burst_one_shot(3),
    }
    results={name:evaluate(pol) for name,pol in cases.items()}
    c=results["candidate_3of4_crossing"]
    print("name,errors,initial_errors,reset_rate,reset_on_G,reset_on_B,successful_B_reset,reverse_G_to_B,dNTP,time,ATP")
    for name,r in results.items():
        print(name,*[f"{float(r[k]):.12g}" for k in
              ("errors","q_initial","resets","reset_good","reset_bad","reset_success","reset_reverse","dntp","time","atp")],sep=",")
    strict=[]
    for name in ("sitewise_each_plus","burst_1plus_one_shot","burst_2plus_repeated","burst_2plus_one_shot"):
        r=results[name]
        assert c["errors"]<r["errors"]
        assert c["resets"]<r["resets"]
        assert c["dntp"]<r["dntp"]
        assert c["time"]<r["time"]
        assert c["atp"]<r["atp"]
        strict.append(name)
    print("EXACT strict componentwise improvements:",", ".join(strict))
    print("exact stationary equations, nonnegative masses, and row stochasticity all verified")


if __name__=="__main__":
    main()
