"""Principal numerical evaluations of the NEW prefix theorem.

Standard library only. No Markov trajectories or exponential-time runs.
Decimal evaluations are rounded, not formal outward interval arithmetic.
Full mathematical arguments are in PREFIX_THEOREM.md.
"""
import argparse
import hashlib
import json
import platform
import resource
import sys
import time
from decimal import Decimal, localcontext, ROUND_CEILING, ROUND_FLOOR
from pathlib import Path

D = Decimal
ZERO, ONE, TWO = D(0), D(1), D(2)


def entropy(h):
    if h == 0 or h == 1:
        return ZERO
    return -h*h.ln()-(ONE-h)*(ONE-h).ln()


def low_envelope(K, h):
    assert 0 < h < D("0.5")
    return ONE-(-(K+entropy(h))/(ONE-h)).exp()


def prefix_constants(K, alpha):
    b = ONE-(-K).exp()
    lam = -b.ln()
    gamma = (ONE-alpha)/(ONE-alpha*b)
    return b, lam, gamma


def counts(K, alpha, eps):
    b, lam, gamma = prefix_constants(K, alpha)
    x = (gamma/eps).ln()/lam
    crit = max(1, int(x.to_integral_value(rounding=ROUND_FLOOR))+1)
    safe = max(1, int(x.to_integral_value(rounding=ROUND_CEILING))+1)
    # Direct inequality checks protect this finite table from an unnoticed
    # candidate/transition off-by-one. Near arbitrary transcendental integer
    # boundaries, interval arithmetic would be required for certification.
    assert gamma*b**crit < eps
    if crit > 1:
        assert gamma*b**(crit-1) >= eps
    assert gamma*b**safe <= b*eps*(ONE+D("1e-50"))
    return crit, safe


def hybrid_bound(K, alpha, eps, N, x):
    """Evaluate Eq. (4.9) with t=ceil(exp(x)), B=R=exp(x)/x^4.

    Denominators use exp(x)<=t, so exact real evaluation would be conservative.
    eta_t <= sqrt(2/(t+1)) is the elementary binomial upper bound.
    The h=eps^2 choice is a proof parameter, not an observable algorithm input.
    """
    x = D(x)
    s = x.exp()
    B = R = s/x**4
    h = eps**2
    if R <= D(3) or ONE/B >= h or h >= D("0.5"):
        return None
    M = (TWO*K+ONE).exp()
    a = min(ONE, K/(R.ln()-ONE))
    b = low_envelope(K, ONE/B)
    bh = low_envelope(K, h)
    geom = sum((bh**j for j in range(N-1)), ZERO)
    d = min(ONE, bh**N + b*geom/(B*h))
    U = M*(D(N*N)*B+ONE)+D(N*N)+R
    delta_core = (TWO*U/(alpha*(TWO*s+ONE))).sqrt()
    eta = (TWO/(s+ONE)).sqrt()
    kappa = (ONE-alpha)/(ONE-alpha*b)
    delta_low = (alpha*(delta_core+a/R)+eta)/(ONE-alpha*b)
    bound = max(a, kappa*d)+delta_core+delta_low*d+b/B+D(N)*a/R
    return {
        "bound": bound, "high_target_tail_bound": a,
        "low_prefix_tail_bound": d, "low_effective_bound": kappa*d,
        "core_bound": delta_core, "low_range_error": delta_low*d,
        "small_tail_corrections": b/B+D(N)*a/R,
        "log_threshold_B": B.ln(),
    }


def pure_bound(K, x):
    """Earlier sharp-scale common-proposal IMH coupling bound, N~exp(x).

    This is a sufficient analytical bound, not the exact minimax risk.
    """
    x = D(x)
    s = x.exp()
    R = s/x**2
    if R <= D(3):
        return None
    a = K/(R.ln()-ONE)
    if a >= ONE:
        return None
    bound = a*(ONE+ONE/R)+(-x*x*(ONE-a)).exp()
    return {"bound": bound, "high_target_tail_bound": a}


def first_integer_log_budget(evaluate, eps):
    """Select an integer x with generous 5% error slack in a rounded bound."""
    target = D("0.95")*eps
    x = 8
    attempts = 0
    while True:
        value = evaluate(x)
        attempts += 1
        if value is not None and value["bound"] <= target:
            break
        x *= 2
        assert x <= 2**20
    lo, hi = 7, x
    # The relevant exponential branch is decreasing in all tested ranges.
    # We do not rely on global monotonicity to certify the returned x:
    # its own bound is checked below. Minimality is not claimed.
    while hi-lo > 1:
        mid = (lo+hi)//2
        value = evaluate(mid)
        attempts += 1
        if value is not None and value["bound"] <= target:
            hi = mid
        else:
            lo = mid
    value = evaluate(hi)
    attempts += 1
    assert value is not None and value["bound"] <= target
    return hi, value, attempts


def stringify(value):
    if isinstance(value, D):
        return str(value)
    if isinstance(value, dict):
        return {k:stringify(v) for k,v in value.items()}
    if isinstance(value, list):
        return [stringify(v) for v in value]
    return value


def run(precision):
    start_wall, start_cpu = time.perf_counter(), time.process_time()
    with localcontext() as ctx:
        ctx.prec = precision
        K, alpha = D(1), D("0.5")
        b, lam, gamma = prefix_constants(K, alpha)
        floor_table = [{"N_candidates":N, "prefix_transitions":N-1,
                        "uniform_error_floor":gamma*b**N}
                       for N in [1,2,3,5,10,15,20]]
        accuracy_table = []
        certificate_rows = []
        evaluations = 0
        for eps in map(D, ["0.1","0.03","0.01","0.003","0.001"]):
            crit, safe = counts(K, alpha, eps)
            accuracy_table.append({
                "epsilon":eps,"N_critical":crit,"N_safe":safe,
                "safe_prefix_transitions":safe-1,
                "critical_floor":gamma*b**crit,
                "safe_floor":gamma*b**safe,
                "safe_floor_over_epsilon":gamma*b**safe/eps,
            })
            x, value, calls = first_integer_log_budget(
                lambda x:hybrid_bound(K,alpha,eps,safe,x),eps)
            xp, pv, pcalls = first_integer_log_budget(
                lambda x:pure_bound(K,x),eps)
            evaluations += calls+pcalls
            certificate_rows.append({
                "epsilon":eps,"N_safe":safe,
                "hybrid_log_time_integer_x":x,
                "hybrid_log10_steps":D(x)/D(10).ln(),
                "hybrid_epsilon_log_time":eps*D(x),
                "hybrid_bound_parts":value,
                "hybrid_log10_expected_global_candidates_approx":
                    (D(x)+(alpha/TWO).ln())/D(10).ln(),
                "pure_IMH_log_budget_integer_x":xp,
                "pure_IMH_log10_transitions":D(xp)/D(10).ln(),
                "pure_IMH_epsilon_log_time":eps*D(xp),
                "pure_IMH_bound_parts":pv,
                "interpretation":"Rounded evaluations of sufficient bounds; no trajectory run, no measured speed ratio.",
            })
        scales=[]
        for k in map(D,["0.1","1","4","8"]):
            bk,lk,gk=prefix_constants(k,alpha)
            ncrit,nsafe=counts(k,alpha,D("0.01"))
            scales.append({
                "K":k,"alpha":alpha,
                "prefix_log_accuracy_coefficient":ONE/lk,
                "N_critical_at_epsilon_0.01":ncrit,
                "N_safe_at_epsilon_0.01":nsafe,
                "unprefixed_uniform_floor":gk*bk,
            })
        result={
            "contract":{"K":K,"alpha":alpha,"natural_log":True,
                        "precision_digits":precision,
                        "arithmetic":"Decimal, nearest rounding, not outward intervals",
                        "theorem":"PREFIX_THEOREM.md",
                        "counts_include_initialization":True},
            "constants":{"b_K":b,"lambda_K":lam,"gamma_K_alpha":gamma,
                         "prefix_log_accuracy_coefficient":ONE/lam},
            "floor_table":floor_table,"accuracy_table":accuracy_table,
            "sufficient_bound_evaluations":certificate_rows,
            "K_dependence":scales,
            "comparison":{"pure_IMH_coefficient":1,
                          "unprefixed_joint_K1_J4_alpha_half":2,
                          "one_step_prefixed_joint_K1_J4_alpha_half":1,
                          "forward_only_safe_prefix_coefficient":1,
                          "claim":"No finite-time dominance or application speedup."},
            "resources":{"wall_seconds":time.perf_counter()-start_wall,
                         "cpu_seconds":time.process_time()-start_cpu,
                         "peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                         "scalar_bound_evaluations":evaluations,
                         "markov_trajectory_steps":0,
                         "hardware":"Local CPU; no accelerator or paid compute"},
            "python":sys.version,"platform":platform.platform(),
            "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        }
    return stringify(result)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--precision",type=int,default=80)
    parser.add_argument("--output",type=Path,default=Path("results/prefix_calculations.json"))
    args=parser.parse_args()
    out=run(args.precision)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({
        "output":str(args.output),"resources":out["resources"],
        "constants":out["constants"],"accuracy_table":out["accuracy_table"],
        "sufficient_log_budgets":[
            {k:r[k] for k in ["epsilon","hybrid_log_time_integer_x",
                             "pure_IMH_log_budget_integer_x"]}
            for r in out["sufficient_bound_evaluations"]],
    },indent=2))
