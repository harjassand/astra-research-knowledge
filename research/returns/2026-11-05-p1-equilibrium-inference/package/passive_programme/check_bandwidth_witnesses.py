"""Numerical checks of explicit positive moment witnesses and upper certificates.

These deterministic numerical checks support the formulas; the analytic proof is
in bandwidth_accuracy_theorem.md. No physical measurements are represented.
"""
import json
from pathlib import Path
import mpmath as mp

mp.mp.dps = 250


def minimax_dual_nodes_weights(K, degree):
    K = mp.mpf(K)
    q = (mp.sqrt(K) - 1) / (mp.sqrt(K) + 1)
    angles = []
    for ell in range(degree + 2):
        if ell == 0:
            angles.append(mp.mpf(0))
            continue
        if ell == degree + 1:
            angles.append(mp.pi)
            continue
        lo, hi = mp.mpf(0), mp.pi
        target = ell * mp.pi
        for _ in range(900):
            theta = (lo + hi) / 2
            phase = (degree - 1) * theta + 2 * mp.atan2(mp.sin(theta), mp.cos(theta) + q)
            if phase < target:
                lo = theta
            else:
                hi = theta
        angles.append((lo + hi) / 2)
    xs = list(reversed([(K + 1) / 2 + (K - 1) * mp.cos(t) / 2 for t in angles]))
    cs = [1 / mp.fprod([x - y for j, y in enumerate(xs) if j != i]) for i, x in enumerate(xs)]
    total = mp.fsum(abs(c) for c in cs)
    signed = [2 * c / total for c in cs]
    if mp.fsum(c / x for c, x in zip(signed, xs)) < 0:
        signed = [-c for c in signed]
    return xs, signed


def logcosh(x):
    x = abs(x)
    return x + mp.log1p(mp.exp(-2*x)) - mp.log(2)


def upper_certificate(kappa, tau, epsilon):
    kap, tau, eps = map(mp.mpf, (kappa, tau, epsilon))
    L1 = mp.log(4 / eps)
    m = int(mp.ceil(min(mp.sqrt(kap) * L1 / 2, L1**2 / (2*tau))))
    h = tau / (m+1)
    a, b = mp.exp(-kap*h), mp.exp(-h)
    d = b-a
    v = (2-a-b)/d
    vnoise = (2+a+b)/d
    log_bias_bound = -logcosh(m*mp.acosh(v))
    log_amplification = logcosh(m*mp.acosh(vnoise))-logcosh(m*mp.acosh(v))
    return {
        "degree": m,
        "bins": m+1,
        "normalized_bin_width": mp.nstr(h, 25),
        "bias_bound": mp.nstr(mp.exp(log_bias_bound), 25),
        "target_half_error": mp.nstr(eps/2, 25),
        "log10_exact_l1_noise_amplification": mp.nstr(log_amplification/mp.log(10), 25),
        "log10_sufficient_bin_error": mp.nstr((mp.log(eps/2)-log_amplification)/mp.log(10), 25),
        "bias_pass": bool(mp.exp(log_bias_bound) <= eps/2),
    }


def check_case(kappa, tau, epsilon):
    kap, tau, eps = map(mp.mpf, (kappa, tau, epsilon))
    L0 = mp.log(1/(4*eps))
    K = min(kap, (L0/(8*mp.e*tau))**2)
    m = int(mp.floor(mp.sqrt(K)*L0/4))
    xs, signed = minimax_dual_nodes_weights(K, m)
    pplus = mp.fsum(c for c in signed if c > 0)
    pminus = -mp.fsum(c for c in signed if c < 0)
    moment_error = max(abs(mp.fsum(c*(x/K)**j for c,x in zip(signed,xs))) for j in range(m+1))
    gain_gap = mp.fsum(c/x for c,x in zip(signed,xs))
    q = (mp.sqrt(K)-1)/(mp.sqrt(K)+1)
    exact_gap = (K-1)/K*q**m
    bound = 2*(mp.e*tau*(K-1)/(m+1))**(m+1)
    sampled_kernel_gap = max(abs(mp.fsum(c*mp.exp(-x*tau*j/256) for c,x in zip(signed,xs))) for j in range(257))
    sampled_step_gap = max(abs(mp.fsum(c*(-mp.expm1(-x*tau*j/256))/x for c,x in zip(signed,xs))) for j in range(257))
    L = mp.log(1/eps)
    F = mp.sqrt(kap)*L*mp.log1p(L/(tau*mp.sqrt(kap)))
    checks = {
        "positive_part_normalized": abs(pplus-1)<mp.mpf('1e-200'),
        "negative_part_normalized": abs(pminus-1)<mp.mpf('1e-200'),
        "moments_match": moment_error<mp.mpf('1e-200'),
        "minimax_gap_formula": abs(gain_gap-exact_gap)<mp.mpf('1e-190'),
        "target_separation": gain_gap>4*eps,
        "sampled_kernel_within_proved_bound": sampled_kernel_gap<=bound,
        "sampled_step_within_proved_bound": sampled_step_gap<=tau*bound,
    }
    return {
        "kappa": mp.nstr(kap, 20),
        "tau": mp.nstr(tau, 20),
        "epsilon": mp.nstr(eps, 20),
        "effective_bandwidth": mp.nstr(K, 25),
        "matched_moment_degree": m,
        "total_support_points": len(xs),
        "gain_gap": mp.nstr(gain_gap, 30),
        "four_epsilon": mp.nstr(4*eps, 20),
        "normalized_moment_residual": mp.nstr(moment_error, 10),
        "proved_kernel_gap_bound": mp.nstr(bound, 20),
        "sampled_kernel_gap": mp.nstr(sampled_kernel_gap, 20),
        "sampled_step_gap": mp.nstr(sampled_step_gap, 20),
        "F": mp.nstr(F, 25),
        "checks": {k:bool(v) for k,v in checks.items()},
        "upper_certificate": upper_certificate(kap,tau,eps),
        "spectral_witness": [{"rate_ratio":mp.nstr(x,270), "signed_mass":mp.nstr(c,270)} for x,c in zip(xs,signed)],
    }


if __name__ == '__main__':
    cases = [
        (16, mp.mpf(1)/128, mp.mpf(1)/16),
        (256, mp.mpf(1)/512, mp.mpf(1)/64),
        (4096, mp.mpf(1)/2048, mp.mpf(1)/256),
        (10**8, mp.mpf(1)/256, mp.mpf(1)/64),
    ]
    results = [check_case(*case) for case in cases]
    output = {"kind":"deterministic high-precision numerical checks, not physical data", "decimal_precision":mp.mp.dps, "results":results}
    path=Path(__file__).with_name('moment_witness_checks.json')
    path.write_text(json.dumps(output,indent=2)+'\n')
    # Validate the serialized spectra, not only the original working objects.
    saved_checks = []
    for r in json.loads(path.read_text())['results']:
        xs = [mp.mpf(z['rate_ratio']) for z in r['spectral_witness']]
        ws = [mp.mpf(z['signed_mass']) for z in r['spectral_witness']]
        K, m, tau = max(xs), r['matched_moment_degree'], mp.mpf(r['tau'])
        residual = max(abs(mp.fsum(w*(x/K)**j for w,x in zip(ws,xs))) for j in range(m+1))
        gain = mp.fsum(w/x for w,x in zip(ws,xs))
        kernel = max(abs(mp.fsum(w*mp.exp(-x*tau*j/256) for w,x in zip(ws,xs))) for j in range(257))
        checks = {
            'moments_pass': bool(residual < mp.mpf('1e-200')),
            'gap_pass': bool(abs(gain-mp.mpf(r['gain_gap'])) < mp.mpf('1e-28')),
            'kernel_pass': bool(abs(kernel/mp.mpf(r['sampled_kernel_gap'])-1) < mp.mpf('1e-18')),
        }
        assert all(checks.values())
        saved_checks.append({'kappa':r['kappa'],
            'moment_residual_after_reload':mp.nstr(residual,12),
            'sampled_kernel_after_reload':mp.nstr(kernel,25), **checks})
    path.with_name('saved_witness_checks.json').write_text(json.dumps({
        'working_decimal_precision':250, 'serialized_significant_digits':270,
        'checks':saved_checks, 'all_pass':True}, indent=2)+'\n')
    for r in results:
        print(json.dumps({k:r[k] for k in ['kappa','tau','epsilon','matched_moment_degree','gain_gap','proved_kernel_gap_bound','sampled_kernel_gap','checks','upper_certificate']}))
    assert all(all(r['checks'].values()) and r['upper_certificate']['bias_pass'] for r in results)
