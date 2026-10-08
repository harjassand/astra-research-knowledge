#!/usr/bin/env python3
"""Fresh finite diagnostics, written without inspecting source diagnostic code.

Exact combinatorial formulas are evaluated in floating-point arithmetic. These
checks are not interval certificates or a replacement for the analytic proof.
"""
from pathlib import Path
from math import lgamma, log, log1p, exp, sqrt, gamma, pi, ceil, log2
from fractions import Fraction
import hashlib
import json
import numpy as np

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "curie_weiss" / "CRITICAL_PROOF_FROZEN.md"
EXPECTED = "55a256b8a7d90573bed614c844a3bbb3734cb4c0886a82716afe18b281467b07"
source_bytes = SOURCE.read_bytes()
assert hashlib.sha256(source_bytes).hexdigest() == EXPECTED
(ROOT / "CRITICAL_PROOF_snapshot.md").write_bytes(source_bytes)

def logsumexp(z):
    m = float(np.max(z))
    return m + log(float(np.exp(z-m).sum()))

mu2 = sqrt(12)*gamma(1.25)/gamma(.75)
I2 = 12**.75*gamma(.75)/4
C0 = 1200*exp(16/9)
I0 = (48**.25*gamma(.25)+48**.75*gamma(.75))/4
A0 = C0*exp(1/192)*(I0/2+8)

def sector_check(N):
    M = np.arange(N % 2, N+1, 2, dtype=float)
    x = M/N**.75
    u = M/N
    k = ((N-M)/2).astype(int)
    logpr = np.fromiter((lgamma(N+1)-lgamma(int(t)+1)
                         -lgamma(N-int(t)+1)-N*log(2)
                         for t in k), dtype=float, count=len(k))
    logg = log(2)+2*np.log(M+1)-np.log(N+M+2)+logpr+(M*M+2*M)/(2*N)
    logZ = logsumexp(logg)
    p = np.exp(logg-logZ)
    ex2 = float(np.dot(p, x*x))
    em = float(np.dot(p, M))
    ej2 = float(np.dot(p, M*(M+2)))/4
    c = (4*ej2-3*N)/(3*N*(N-1))
    D = 2*ej2/N-logZ
    rateI = .5*((1+u)*np.log1p(u)
                +np.where(u < 1, (1-u)*np.log(np.maximum(1-u, np.finfo(float).tiny)), 0))
    central = u <= .5
    ratio_logs = logpr[central]+N*rateI[central]+.5*log(N)
    envelope_slack = log(200)+np.log1p(x*x)-x**4/24-logg
    log_moment = logsumexp(np.log(p[p > 0])+(x[p > 0]**2)/48)
    # P(S=s) = sum_{M >= |s|} p(M)/(M+1), independently reconstructed.
    pointS = np.cumsum((p/(M+1))[::-1])[::-1]
    sign_norm = (float(pointS[0]) if N % 2 == 0 else 0) + 2*float(pointS[M > 0].sum())
    a = sqrt(N)  # r=N; actual readouts coincide with S.
    trace_threshold = sqrt(N)*a**.25
    above = M > trace_threshold
    Ptrace = 2*float(pointS[above].sum())
    Qtrace = 2*float(np.exp(logpr[above]).sum())
    KL_threshold = .5*N**.75
    aboveKL = M > KL_threshold
    PKL = 2*float(pointS[aboveKL].sum())
    logQKL = log(2)+logsumexp(logpr[aboveKL])
    QKL = exp(logQKL)
    binaryD = (PKL*log(PKL/QKL)+(1-PKL)*log((1-PKL)/(1-QKL)))
    rho2vals = np.array([(1-3*c)/4, (1+c)/4, (1+c)/4, (1+c)/4])
    chi2 = 3*c*c
    delta2 = .75*abs(c)
    D2 = float(np.dot(rho2vals, np.log(4*rho2vals)))
    assert float(envelope_slack.min()) >= -1e-7
    assert float(ratio_logs.min()) >= -log(2)-1e-7
    assert float(ratio_logs.max()) <= log(2)+1e-7
    assert logZ >= -.0 + (-16/9-log(6)+.75*log(N))-1e-7
    assert log_moment <= log(A0)+1e-7
    assert abs(sign_norm-1) <= 1e-8
    assert np.min(rho2vals) > 0
    compact = x <= 2
    compact_error = float(np.max(np.abs(np.exp(logg[compact])
                          -2*sqrt(2/pi)*x[compact]**2*np.exp(-x[compact]**4/12))))
    return {
        "N": N, "parity": N % 2, "sectors": len(M),
        "minimum_log_global_envelope_slack": float(envelope_slack.min()),
        "central_stirling_ratio_range": [exp(float(ratio_logs.min())), exp(float(ratio_logs.max()))],
        "logZ": logZ, "Z_over_N_three_quarters": exp(logZ-.75*log(N)),
        "Z_limit": sqrt(2/pi)*I2, "EX2": ex2, "mu2": mu2,
        "sqrtN_pair_c": sqrt(N)*c, "pair_c_limit": mu2/3,
        "D_global_over_sqrtN": D/sqrt(N), "D_global_limit": mu2/2,
        "compact_x_le_2_absolute_error": compact_error,
        "log_exp_square_moment": log_moment, "log_A0": log(A0),
        "S_distribution_normalization": sign_norm,
        "r2_chi_over_predicted": chi2/(mu2*mu2/(3*N)),
        "r2_delta_times_sqrtN": delta2*sqrt(N), "r2_delta_limit": mu2/4,
        "r2_KL_times_N": D2*N, "r2_KL_limit": mu2*mu2/6,
        "r_equals_N_trace_threshold_target_probability": Ptrace,
        "r_equals_N_trace_threshold_white_probability": Qtrace,
        "r_equals_N_bounded_effect_gap": Ptrace-Qtrace,
        "r_equals_N_KL_threshold_target_probability": PKL,
        "r_equals_N_KL_threshold_white_log_probability": logQKL,
        "r_equals_N_binary_KL_over_sqrtN": binaryD/sqrt(N),
    }

heat = []
for r in [2, 3, 4, 8, 16, 64, 256, 1024, 4096]:
    k = np.arange(r+1)
    logp = np.fromiter((lgamma(r+1)-lgamma(int(t)+1)-lgamma(r-int(t)+1)-r*log(2)
                       for t in k), dtype=float, count=r+1)
    p = np.exp(logp)
    y = (2*k-r)**2/(4*r)
    T = float(np.dot(p, np.exp(-y)))
    q = float(np.dot(p, y*np.exp(-y)))
    kap = T-4*q
    coeff_direct = float(np.dot(p, np.exp(-y)*((2*k-r)**2-r)/(r*(r-1))))
    assert kap >= exp(-12)/8-1e-12
    assert abs(coeff_direct+kap/(r-1)) < 1e-12
    heat.append({"r": r, "kappa": kap, "pair_coefficient_direct": coeff_direct,
                 "EY": float(np.dot(p,y)), "EY2": float(np.dot(p,y*y)),
                 "EY3": float(np.dot(p,y*y*y)),
                 "variance_Y": float(np.dot(p,y*y)-np.dot(p,y)**2)})

# Exact rational check of the deletion estimate actually used in the heat proof.
deletion_upper = 2*Fraction(15,64)*(Fraction(1,12)+Fraction(1,2*12**2)
                                  +Fraction(3,16*12**3))
assert deletion_upper < Fraction(1,16)

counterexamples = []
for N in [256, 4096, 65536, 1048576]:
    eps = mu2/sqrt(N)
    r = ceil(2*log2(N))
    d = 2**r
    sym_mass = eps+(1-eps)*(r+1)/d
    chi = eps*eps*(d/(r+1)-1)
    delta = eps*(1-(r+1)/d)
    Deta = sym_mass*log(1-eps+eps*d/(r+1))+(1-sym_mass)*log1p(-eps)
    Dconvex = eps*(r*log(2)-log(r+1))
    assert 0 <= Deta <= Dconvex+1e-12
    assert 0 < delta <= eps < 1
    counterexamples.append({"N":N, "r":r, "epsilon":eps,
                            "chi":chi, "half_trace":delta, "KL":Deta,
                            "KL_convexity_upper":Dconvex,
                            "global_half_trace_upper":eps,
                            "sqrtN_pair_c":mu2/3,
                            "legal_scope":"PI SU2 separable rare-maxspin mixture; not the exact Gibbs model"})

results = {
    "source": str(SOURCE), "source_sha256": EXPECTED,
    "method": "Fresh analytic-formula diagnostic; floating point, not formal or interval validation",
    "constants": {"mu2": mu2, "A0": A0, "kappa_floor": exp(-12)/8,
                  "heat_tail_deletion_exact": str(deletion_upper),
                  "heat_tail_deletion_decimal": float(deletion_upper)},
    "sectors": [sector_check(N) for N in [256,257,512,513,4096,4097,16384,16385,
                                           65536,65537,1048576,1048577]],
    "white_heat": heat,
    "false_extension_counterexamples": counterexamples,
    "scope": "Both parity grids; exact finite sector formulas; fixed-r=2 full marginal; global-r=N bounded effects. No general marginal eigensolver or external review."
}
(ROOT / "verification_results.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps({"cases":len(results["sectors"]),"heat_cases":len(heat),
                  "all_assertions_passed":True,
                  "largest_even":results["sectors"][-2],
                  "largest_odd":results["sectors"][-1]}, indent=2))
