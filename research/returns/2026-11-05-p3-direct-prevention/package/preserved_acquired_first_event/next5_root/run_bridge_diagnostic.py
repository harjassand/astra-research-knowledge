"""Certificate execution and analytic three-state comparison only.

No general rare-event engine or physical experiment is executed here.
The three-state chain has a simpler exact solver; this diagnoses only
the new confidence calculation and the CDF/mark distinction.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import mpmath as mp
from certificate import schedule, rare_certificate, decimal_summary, sqrt_up

mp.mp.dps = 110


def marked_exp_tv(rate_ratio, weights, altered):
    """Analytic density integral; floating reference, not certificate."""
    c = mp.mpf(str(rate_ratio))
    ans = mp.mpf(0)
    for v, w in zip(weights, altered):
        v, w = mp.mpf(str(v)), mp.mpf(str(w))
        if c == 1:
            ans += abs(v - w)
            continue
        crossing = mp.log(w * c / v) / (c - 1)
        if crossing <= 0:
            ans += abs(v - w)
        else:
            A = v * (1 - mp.exp(-crossing)) - w * (1 - mp.exp(-c * crossing))
            ans += abs(A) + abs(v - w - A)
    return ans / 2


rows = []
h = F(1, 10**12)
for power in [12, 30, 100]:
    lam = F(1, 10**power)
    pars = schedule(F(1, 5), F(1, 4), lam / 8, H=1)
    cert = rare_certificate(g=F(1, 4), zeta=lam / 8, p_upper=2*lam,
                            H=1, b=pars["b"], L=pars["L"], E=2*h, a=2*h)
    exact_tv = marked_exp_tv(1 + mp.mpf(1)/10**12,
                            [mp.mpf('0.4'), mp.mpf('0.6')],
                            [mp.mpf('0.4')*(1+mp.mpf(1)/10**12),
                             1-mp.mpf('0.4')*(1+mp.mpf(1)/10**12)])
    rows.append(dict(lambda_power=-power, mean_time=f"1e{power}",
                     **pars, **decimal_summary(cert),
                     exact_rational_certificate={k:str(v) for k,v in cert.items()},
                     exact_time_and_mark_TV=str(exact_tv)))

cdf_counterexample = dict(equal_CDF=True, terminal_mark_TV="0.98",
                          true_marks=["0.99", "0.01"],
                          alternative_marks=["0.01", "0.99"])
assert abs(marked_exp_tv(1, ['0.99', '0.01'], ['0.01', '0.99']) - mp.mpf('0.98')) < mp.mpf('1e-100')

for x in [F(0), F(1, 3), F(2), F(1, 10**100), F(10**50, 7)]:
    y = sqrt_up(x)
    assert y*y >= x
    if y:
        assert max(F(0), y-F(1,10**32))**2 <= x

report = {
    "status": "Exact-rational upper certificates; analytic floating reference only",
    "executed": ["certificate arithmetic", "three-state exact-density formula", "CDF/mark counterexample"],
    "not_executed": ["general Gibbs counting", "general first-event sampler", "physical acquisition"],
    "rows": rows,
    "CDF_does_not_control_marks": cdf_counterexample,
}
out = Path(__file__).with_name('bridge_execution.json')
out.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))

