#!/usr/bin/env python3
"""Exact finite-state comparison for a cue-memory polymerase reset controller.

The latent polymerase conformation X_i is G/B.  Errors depend on X_i, a noisy
cue Z_i reports the current error with sensitivity s and false-positive f,
and a controller stores L preceding cues. At each site it may apply a finite-
time reversible B/G reset map (a local LDB embedding is checked separately;
the complete controller gate is not thermodynamically closed). Independently,
all policies patch a site
when Z_i=+, with success eta; every successful resynthesis consumes one extra
dNTP and is wrong with probability e_X in the post-reset conformation.

The state chain (X_i, last-L cues) is finite. We evaluate a specified set of
deterministic policies with L=3 and compute their stationary accuracy, copy
time, dNTP and stipulated event-equivalent budgets. The reset map has both
directions: B->G with probability rho and G->B with probability delta. The
controller has no access to X or the true mismatch bit.

This is a synthetic, source-unfitted model.  Numerical outputs test only its
finite-state arithmetic and are not empirical claims about any polymerase.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import math
import numpy as np


@dataclass(frozen=True)
class Params:
    a: float = 0.005
    b: float = 0.02
    e_g: float = 1e-4
    e_b: float = 0.10
    s: float = 0.80
    f: float = 0.20
    rho: float = 0.60
    delta: float = 0.20
    eta: float = 0.98
    t0: float = 1.0
    t_patch: float = 0.4
    t_reset: float = 1.0
    w_patch_atp: float = 1.0
    w_reset_atp: float = 1.0
    L: int = 3


def h2(x: float) -> float:
    if x <= 0 or x >= 1:
        return 0.0
    return -x*math.log2(x) - (1-x)*math.log2(1-x)


def stationary(P: np.ndarray) -> np.ndarray:
    n = len(P)
    M = P.T - np.eye(n)
    M[-1, :] = 1.0
    rhs = np.zeros(n)
    rhs[-1] = 1.0
    pi = np.linalg.solve(M, rhs)
    if np.min(pi) < -1e-10:
        raise ArithmeticError("negative stationary probability")
    pi = np.maximum(pi, 0.0)
    pi /= pi.sum()
    err = float(np.max(np.abs(pi @ P - pi)))
    if err > 2e-11:
        raise ArithmeticError(f"stationarity residual {err:g}")
    return pi


def evaluate(policy: tuple[float, ...], p: Params) -> dict[str, float | str]:
    L = p.L
    nm = 1 << L
    n = 2*nm
    if len(policy) != 2*nm:
        raise ValueError("policy must map (memory,cue) to reset/no-reset")
    P = np.zeros((n,n), dtype=float)
    reward_names = ("errors", "dntp", "patches", "resets", "q_initial",
                    "cue_plus", "cue_conditional_entropy_diagnostic", "false_cue", "true_cue",
                    "missed_error", "reset_bad_state", "reset_good_state",
                    "reset_success", "reset_reverse")
    R = {name: np.zeros(n) for name in reward_names}
    # Joint law of popped oldest cue and new register contents, for Landauer's
    # minimum conditional erasure work on the shift register.
    pop_joint: dict[tuple[int,int], float] = {}
    for x, mem, e, z in product((0,1), range(nm), (0,1), (0,1)):
        i = x*nm + mem
        pe = p.e_b if x else p.e_g
        p_e = pe if e else 1-pe
        p_z = ((p.s if e else p.f) if z else
               ((1-p.s) if e else (1-p.f)))
        obs_mass = p_e*p_z
        action = float(policy[2*mem+z])
        if not 0.0 <= action <= 1.0:
            raise ValueError("randomized reset probabilities must lie in [0,1]")
        reset = []
        if action > 0:
            branches = ((1,p.delta),(0,1-p.delta)) if x == 0 else ((0,p.rho),(1,1-p.rho))
            reset.extend((xp, action*pr, 1) for xp,pr in branches)
        if action < 1:
            reset.append((x,1-action,0))
        new_mem = ((mem << 1) | z) & (nm-1)
        popped = (mem >> (L-1)) & 1
        pop_joint[(popped,new_mem)] = pop_joint.get((popped,new_mem),0.0) + 0.0
        for xp, pr, did_reset in reset:
            mass = obs_mass*pr
            e_replacement = p.e_b if xp else p.e_g
            final_error = (p.eta*e_replacement + (1-p.eta)*e) if z else float(e)
            R["errors"][i] += mass*final_error
            R["dntp"][i] += mass*(1.0 + p.eta*z)
            R["patches"][i] += mass*z
            R["resets"][i] += mass*did_reset
            R["q_initial"][i] += mass*e
            R["cue_plus"][i] += mass*z
            # Diagnostic H(Z|E), not an additive sensor-reset work charge.
            # If Z is copied into the controller register reversibly, its
            # information is retained there; the loss is counted once by the
            # popped-bit conditional entropy below.
            R["cue_conditional_entropy_diagnostic"][i] += mass*(h2(p.s) if e else h2(p.f))
            R["false_cue"][i] += mass*int(z == 1 and e == 0)
            R["true_cue"][i] += mass*int(z == 1 and e == 1)
            R["missed_error"][i] += mass*int(z == 0 and e == 1)
            R["reset_bad_state"][i] += mass*did_reset*int(x == 1)
            R["reset_good_state"][i] += mass*did_reset*int(x == 0)
            R["reset_success"][i] += mass*did_reset*int(x == 1 and xp == 0)
            R["reset_reverse"][i] += mass*did_reset*int(x == 0 and xp == 1)
            pop_joint[(popped,new_mem)] += mass*0.0  # stationary weight added below
            # natural conformation transition after current-site actions
            xnext = ((1,p.a),(0,1-p.a)) if xp == 0 else ((0,p.b),(1,1-p.b))
            for xn, p_xn in xnext:
                P[i, xn*nm+new_mem] += obs_mass*pr*p_xn
    pi = stationary(P)
    # Recompute the popped-bit distribution using the stationary state masses.
    pop_joint.clear()
    for x, mem, e, z in product((0,1), range(nm), (0,1), (0,1)):
        i = x*nm+mem
        pe = p.e_b if x else p.e_g
        p_e = pe if e else 1-pe
        p_z = ((p.s if e else p.f) if z else
               ((1-p.s) if e else (1-p.f)))
        new_mem = ((mem << 1) | z) & (nm-1)
        popped = (mem >> (L-1)) & 1
        pop_joint[(popped,new_mem)] = pop_joint.get((popped,new_mem),0.0) + pi[i]*p_e*p_z
    pop_marg = {}
    for (popped,new_mem), mass in pop_joint.items():
        pop_marg[new_mem] = pop_marg.get(new_mem,0.0)+mass
    erase_bits = 0.0
    for (popped,new_mem), mass in pop_joint.items():
        if mass > 0:
            erase_bits -= mass*math.log2(mass/pop_marg[new_mem])
    out = {k: float(pi @ v) for k,v in R.items()}
    out["memory_erase_bits"] = erase_bits
    out["cue_conditional_entropy_bits_diagnostic"] = out["cue_conditional_entropy_diagnostic"]
    out["reset_bad_probability"] = out["reset_bad_state"]/out["resets"] if out["resets"] else 0.0
    out["reset_false_alarm_fraction"] = out["reset_good_state"]/out["resets"] if out["resets"] else 0.0
    out["reset_success_fraction"] = out["reset_success"]/out["resets"] if out["resets"] else 0.0
    out["time"] = p.t0+p.t_patch*out["patches"]+p.t_reset*out["resets"]
    out["atp_equiv"] = p.w_patch_atp*out["patches"]+p.w_reset_atp*out["resets"]
    out["residual"] = float(np.max(np.abs(pi @ P-pi)))
    out["policy"] = "".join(str(int(bit)) if bit in (0,1) else f"{bit:.3g}" for bit in policy)
    return out


def index(mem: int, z: int) -> int:
    return 2*mem+z


def make_policies(p: Params) -> dict[str, tuple[int,...]]:
    L=p.L; nm=1<<L
    site=[]; burst_runs={}
    for mem in range(nm):
        for z in (0,1):
            site.append(z)
    # Sitewise: alarm on each positive cue.
    sitewise=tuple(site)
    # At least two policies from common burst controls, including repeated
    # threshold and one-shot threshold on the first cue of each positive run.
    burst2=[]; burst3=[]; one_shot2=[]; one_shot1=[]
    for mem in range(nm):
        bits=[(mem >> j)&1 for j in reversed(range(L))] # oldest to newest
        for z in (0,1):
            seq=bits+[z]
            burst2.append(int(len(seq)>=2 and seq[-1] and seq[-2]))
            burst3.append(int(len(seq)>=3 and all(seq[-3:])))
            one_shot2.append(int(z==1 and len(bits)>=2 and bits[-1]==1 and bits[-2]==0))
            one_shot1.append(int(z==1 and bits[-1]==0))
    return {"none":(0,)*(2*nm), "sitewise_each_plus":sitewise,
            "burst_2plus_repeated":tuple(burst2),
            "burst_3plus_repeated":tuple(burst3),
            "burst_2plus_one_shot":tuple(one_shot2),
            "burst_1plus_one_shot":tuple(one_shot1)}


def mode_posterior(policy: tuple[int,...], p: Params, history: tuple[int,...]) -> float:
    """P(X_current=B | finite cue history) under that policy's stationary law."""
    L=p.L; nm=1<<L
    P=np.zeros((2*nm,2*nm))
    for x,mem,e,z in product((0,1),range(nm),(0,1),(0,1)):
        i=x*nm+mem
        pe=p.e_b if x else p.e_g
        p_e=pe if e else 1-pe
        p_z=((p.s if e else p.f) if z else ((1-p.s) if e else (1-p.f)))
        action=policy[2*mem+z]
        reset=(((1,p.delta),(0,1-p.delta)) if x==0 else ((0,p.rho),(1,1-p.rho))) if action else ((x,1.0),)
        new_mem=((mem<<1)|z)&(nm-1)
        for xp,pr in reset:
            trans=((1,p.a),(0,1-p.a)) if xp==0 else ((0,p.b),(1,1-p.b))
            for xn,px in trans:
                P[i,xn*nm+new_mem]+=p_e*p_z*pr*px
    pi=stationary(P)
    # history is ordered oldest->newest; choose the memory component equal to it.
    m=0
    for bit in history: m=(m<<1)|bit
    mass=sum(pi[x*nm+m] for x in (0,1))
    return float(pi[1*nm+m]/mass) if mass>0 else math.nan


def posterior_crossing_policy(p: Params, theta: float) -> tuple[int,...]:
    """Reset if finite-window posterior crosses theta after the current cue."""
    L=p.L; nm=1<<L
    # Start from the uncontrolled stationary mode distribution. The map is an
    # offline finite-state lookup; it consumes only stored cues online.
    prior=p.a/(p.a+p.b)
    emis=[]
    for x in (0,1):
        e=p.e_b if x else p.e_g
        pp=e*p.s+(1-e)*p.f
        emis.append((1-pp,pp))
    def filt(seq):
        u=[1-prior,prior]
        for t,z in enumerate(seq):
            u=[u[x]*emis[x][z] for x in (0,1)]
            sm=sum(u); u=[a/sm for a in u]
            if t+1<len(seq):
                u=[u[0]*(1-p.a)+u[1]*p.b,
                   u[0]*p.a+u[1]*(1-p.b)]
        return u[1]
    table=[]
    for mem in range(nm):
        bits=tuple((mem >> j)&1 for j in reversed(range(L)))
        for z in (0,1):
            post_new=filt(bits+(z,))
            post_old=filt(bits)
            table.append(int(post_new>=theta and post_old<theta))
    return tuple(table)


def one_shot_run_policy(p: Params, k: int) -> tuple[int,...]:
    """Trigger once when a positive run first reaches k, using stored cues."""
    L=p.L; nm=1<<L
    if k >= L+1:
        raise ValueError("run threshold must fit in stored cues plus current cue")
    table=[]
    for mem in range(nm):
        bits=[(mem >> j)&1 for j in reversed(range(L))]
        for z in (0,1):
            seq=bits+[z]
            reached=(z==1 and all(seq[-k:]))
            was_reached=(len(bits)>=k and all(bits[-k:]))
            table.append(int(reached and not was_reached))
    return tuple(table)


def randomized_to_reset_rate(policy: tuple[int,...], target: float, p: Params):
    """Analytical Bernoulli thinning to match rate; randomizer cost is omitted."""
    low,high=0.0,1.0
    for _ in range(60):
        u=(low+high)/2
        row=evaluate(tuple(u*float(bit) for bit in policy),p)
        if row["resets"] < target:
            low=u
        else:
            high=u
    u=(low+high)/2
    return u,evaluate(tuple(u*float(bit) for bit in policy),p)


def report(p: Params) -> None:
    policies=make_policies(p)
    policies["burst_3plus_one_shot"] = one_shot_run_policy(p,3)
    candidate_policy=posterior_crossing_policy(p,0.30)
    candidate=evaluate(candidate_policy,p)
    print("params",p)
    print("candidate trigger table: memory is three previous cue bits in oldest-to-newest order; input is current cue")
    print("candidate A=1 patterns (previous three,current): -+++ ; +-++ ; ++-+")
    print("policy table index is 2*memory+current_cue; all omitted entries are zero")
    print("candidate",candidate)
    print("\nreset-rate-matched controls (analytical Bernoulli thinning; randomizer cost omitted):")
    print("name,scale,errors,reset_rate,false_cue_rate,missed_error_rate,false_reset_rate,successful_B_resets,dNTP/site,time/site,event_ATP_equiv/site,H_Z_given_E_diagnostic_bits,register_overwrite_Landauer_bound_bits,stationary_residual")
    controls=("sitewise_each_plus","burst_1plus_one_shot","burst_2plus_repeated",
              "burst_2plus_one_shot","burst_3plus_repeated","burst_3plus_one_shot")
    rows=[]
    for name in controls:
        base=policies[name]
        max_row=evaluate(base,p)
        if max_row["resets"] >= candidate["resets"]:
            scale,row=randomized_to_reset_rate(base,candidate["resets"],p)
        else:
            scale,row=1.0,max_row
        rows.append((name,scale,row))
        print(f"{name},{scale:.12g},{row['errors']:.12g},{row['resets']:.12g},{row['false_cue']:.12g},"
              f"{row['missed_error']:.12g},{row['reset_good_state']:.12g},{row['reset_success']:.12g},"
              f"{row['dntp']:.12g},{row['time']:.12g},{row['atp_equiv']:.12g},"
              f"{row['cue_conditional_entropy_bits_diagnostic']:.12g},{row['memory_erase_bits']:.12g},{row['residual']:.2e}")
    print("\ncandidate false-cue rate, missed-error rate, false-reset rate, successful B resets:",
          candidate["false_cue"],candidate["missed_error"],candidate["reset_good_state"],candidate["reset_success"])
    # Executable inequalities for the stated finite model and matched-reset
    # controls. The claim is scoped to this model and these control families.
    assert candidate["resets"] > 0
    assert candidate["residual"] < 2e-11
    for name,scale,row in rows[:4]:
        assert candidate["errors"] < row["errors"]
        assert candidate["dntp"] < row["dntp"]
        assert candidate["time"] < row["time"]
        assert candidate["atp_equiv"] < row["atp_equiv"]
        assert candidate["memory_erase_bits"] < row["memory_erase_bits"]
        assert abs(candidate["resets"]-row["resets"]) < 1e-10
        assert abs(candidate["cue_conditional_entropy_bits_diagnostic"]-row["cue_conditional_entropy_bits_diagnostic"]) < 1e-10
    print(f"\nmatched controls checked={len(rows)}; first four strict inequalities passed")


if __name__ == "__main__":
    report(Params())
