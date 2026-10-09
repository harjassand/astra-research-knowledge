#!/usr/bin/env python3
"""Finite hidden-conformation copying/repair controller diagnostics.

This is an explicit finite-state model, not a fit to a named polymerase.
The latent polymerase conformation X is good (0) or bad (1), with Markov
transition probabilities a=P(B|G), b=P(G|B).  Conditional error rates are
eG,eB.  A mismatch cue has sensitivity s and false-positive probability f.

The physical controller stores only the preceding cue m.  Each deterministic
reset policy is a four-bit truth table A(m,z).  A=1 attempts one ATP-driven
finite-efficacy conformational reset.  All policies patch a current site on
z=+ using an excision/resynthesis reaction; a successful patch consumes one
additional dNTP and the replacement error probability is that of the
post-reset conformation.  Reset transitions B->G and G->B have probabilities
rho and delta, respectively, so the reset is not an oracle or a one-way map.

The script enumerates all 16 one-bit reset controllers, solves their exact
finite-state Markov chains numerically, and reports errors, dNTP, time, ATP,
cue frequencies, and Landauer lower bounds for cue/register erasure.  All
reported numerical outputs are internal model diagnostics only.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import math
import numpy as np


def h2(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


@dataclass(frozen=True)
class Params:
    a: float = 0.004       # G -> B per incorporation
    b: float = 0.05        # B -> G per incorporation
    e_g: float = 1e-4      # initial wrong-incorporation probability in G
    e_b: float = 0.02      # initial wrong-incorporation probability in B
    s: float = 0.90        # P(Z=+ | E=1)
    f: float = 0.01        # P(Z=+ | E=0)
    rho: float = 0.80      # reset probability B -> G on an alarm
    delta: float = 0.002   # reset side-effect probability G -> B on an alarm
    eta: float = 0.98      # excision/resynthesis completion probability on Z=+
    t0: float = 1.0        # base-copy time
    t_patch: float = 0.4   # time per attempted patch (also false alarms)
    t_reset: float = 1.0   # time per reset attempt
    w_patch_atp: float = 1.0  # ATP equivalents per cue-triggered patch attempt
    w_reset_atp: float = 1.0  # ATP equivalents per reset attempt


def stationary(P: np.ndarray) -> np.ndarray:
    """Solve pi P=pi, sum(pi)=1, and verify the residual."""
    n = P.shape[0]
    A = P.T - np.eye(n)
    A[-1, :] = 1.0
    rhs = np.zeros(n)
    rhs[-1] = 1.0
    pi = np.linalg.solve(A, rhs)
    if np.min(pi) < -1e-10:
        raise ArithmeticError("negative stationary mass")
    pi = np.maximum(pi, 0.0)
    pi /= pi.sum()
    residual = np.max(np.abs(pi @ P - pi))
    if residual > 2e-11:
        raise ArithmeticError(f"stationarity residual {residual}")
    return pi


def run(policy: tuple[int, int, int, int], p: Params = Params()) -> dict[str, float | str]:
    """Exact-state enumeration for one policy; index bits by 2*m+z."""
    # State is (X,m), with X in {G=0,B=1} and previous cue m in {-,+}.
    nstate = 4
    P = np.zeros((nstate, nstate), dtype=float)
    rewards = {name: np.zeros(nstate, dtype=float) for name in (
        "errors", "dntp", "patches", "resets", "cue_plus", "bad_after_reset",
        "sensor_conditional_entropy_bits")}
    for x, m, e, z in product((0, 1), repeat=4):
        i = 2 * x + m
        pe = p.e_b if x else p.e_g
        p_e = pe if e else 1.0 - pe
        p_z = (p.s if e else p.f) if z else ((1.0-p.s) if e else (1.0-p.f))
        mass = p_e * p_z
        alarm = policy[2*m+z]
        # Finite reset channel. Its reverse branch is nonzero in both states.
        if alarm:
            reset_branches = ((1, p.delta), (0, 1-p.delta)) if x == 0 else ((0, p.rho), (1, 1-p.rho))
        else:
            reset_branches = ((x, 1.0),)
        for xp, p_xp in reset_branches:
            # Expected final error: no patch leaves E; successful patch replaces
            # it with a fresh incorporation at the post-reset conformation.
            e_new = p.e_b if xp else p.e_g
            err = (p.eta * e_new + (1-p.eta) * e) if z else float(e)
            rewards["errors"][i] += mass * p_xp * err
            rewards["dntp"][i] += mass * p_xp * (1.0 + p.eta * z)
            rewards["patches"][i] += mass * p_xp * z
            rewards["resets"][i] += mass * p_xp * alarm
            rewards["cue_plus"][i] += mass * p_xp * z
            rewards["bad_after_reset"][i] += mass * p_xp * xp
            rewards["sensor_conditional_entropy_bits"][i] += mass * p_xp * (
                h2(p.s) if e else h2(p.f))
            # Advance the polymerase mode one incorporation step; remember z.
            for xn, p_xn in ((1, p.a), (0, 1-p.a)) if xp == 0 else ((0, p.b), (1, 1-p.b)):
                j = 2 * xn + z
                P[i, j] += mass * p_xp * p_xn
    pi = stationary(P)
    avg = {k: float(pi @ v) for k, v in rewards.items()}
    # Joint law of (previous cue,current cue) is obtained from stationary state
    # mass and cue emission. The cost is the minimum work to overwrite the old
    # one-bit shift register while retaining the new cue.
    joint = np.zeros((2, 2), dtype=float)
    q_error = 0.0
    for x, m in product((0, 1), repeat=2):
        i = 2*x+m
        pe = p.e_b if x else p.e_g
        q_error += pi[i] * pe
        for e in (0, 1):
            p_e = pe if e else 1-pe
            for z in (0, 1):
                p_z = (p.s if e else p.f) if z else ((1-p.s) if e else (1-p.f))
                joint[m,z] += pi[i] * p_e * p_z
    pz = joint.sum(axis=0)
    memory_erase_bits = 0.0
    for m in (0,1):
        for z in (0,1):
            if joint[m,z] > 0 and pz[z] > 0:
                memory_erase_bits -= joint[m,z] * math.log2(joint[m,z]/pz[z])
    avg["q_initial"] = q_error
    avg["memory_erase_bits"] = memory_erase_bits
    avg["sensor_erase_bits"] = avg["sensor_conditional_entropy_bits"]
    avg["speed_time"] = p.t0 + p.t_patch*avg["patches"] + p.t_reset*avg["resets"]
    avg["atp_equiv"] = p.w_patch_atp*avg["patches"] + p.w_reset_atp*avg["resets"]
    avg["total_dntp"] = avg["dntp"]
    avg["policy"] = "".join(map(str, policy))
    avg["stationary_residual"] = float(np.max(np.abs(pi @ P - pi)))
    return avg


def named_policies() -> dict[str, tuple[int,int,int,int]]:
    # A(m,z), table index 2*m+z. Sitewise alarm reacts to current +.
    sitewise = (0, 1, 0, 1)
    burst2 = (0, 0, 0, 1)  # reset only after a two-cue ++ burst
    delayed = (0, 0, 1, 1) # reset on any cue following a preceding +
    return {"none": (0,0,0,0), "sitewise_current_plus": sitewise,
            "two_plus_burst": burst2, "delayed_after_plus": delayed}


def main() -> None:
    p = Params()
    print("params", p)
    print("policy,initial_error,final_error,reset_rate,patch_rate,dNTP/site,time/site,ATP/site,sensor_bits,memory_bits,residual")
    rows = []
    for bits in product((0,1), repeat=4):
        row = run(bits, p)
        rows.append(row)
    for name, policy in named_policies().items():
        row = run(policy, p)
        print(f"{name},{row['q_initial']:.9g},{row['errors']:.9g},{row['resets']:.9g},"
              f"{row['patches']:.9g},{row['dntp']:.9g},{row['speed_time']:.9g},"
              f"{row['atp_equiv']:.9g},{row['sensor_erase_bits']:.9g},"
              f"{row['memory_erase_bits']:.9g},{row['stationary_residual']:.2e}")
    # Find deterministic controllers that improve the named baselines at equal
    # or lower reset rate and no larger total work/time.
    targets = [run(x,p) for x in named_policies().values() if x != (0,0,0,0)]
    print("\ncontrollers that weakly use no more resets/time than sitewise and have fewer errors:")
    site = run(named_policies()["sitewise_current_plus"], p)
    for row in rows:
        if row["errors"] < site["errors"]-1e-12 and row["resets"] <= site["resets"]+1e-12 and row["speed_time"] <= site["speed_time"]+1e-12:
            print(f"policy={row['policy']} err={row['errors']:.9g} resets={row['resets']:.9g} "
                  f"dNTP={row['dntp']:.9g} time={row['speed_time']:.9g} ATP={row['atp_equiv']:.9g}")
    # Exact scope of the controller class: 16 truth tables, one stored cue bit.
    print(f"\nfinite policies enumerated={len(rows)}; max stationarity residual="
          f"{max(float(r['stationary_residual']) for r in rows):.3e}")


if __name__ == "__main__":
    main()
