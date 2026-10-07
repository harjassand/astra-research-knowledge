"""Small diagnostics for the exact scalar covariance-information obstruction.

No mutual-information quadrature is used to certify the theorem. The executable
checks constants and the closed-form logistic normalization/energy formulas.
"""
import json, math
from pathlib import Path

alpha = math.erfc(1 / math.sqrt(2))
s0 = 256
assert alpha * (s0 / 32 - math.log(4)) - math.log(2) >= alpha * s0 / 64
rows = []
for n in [256, 512, 1024, 4096, 16384]:
    h0 = 1 / (1 + math.exp(n)) if n < 700 else 0.0
    h1 = 1 / (1 + math.exp(-1))
    z = -math.expm1(-(n + 1))
    energy = ((1 - h0)**3 - (1 - h1)**3) / (3 * (h1 - h0))
    pa2 = (1 - math.exp(-1)) / (h1 - h0)
    poincare = 1 / (1 / 4 + math.pi**2 / (n + 1)**2)
    variance = 1 - (n + 1)**2 * math.exp(-(n + 1)) / z**2
    assert 0 < energy <= 1
    assert pa2 >= 0.5
    assert poincare <= 4 and variance <= 1
    bound = pa2 * alpha / 64 * math.log(n / s0)
    rows.append(dict(n=n,energy=energy,p_times_a_squared=pa2,
                     poincare=poincare,variance=variance,
                     integrated_information_lower=bound))
scalar_fields = []
for x in [-20, -10, -2, 0, 1, 4, 10, 20]:
    h = 1 / (1 + math.exp(-x))
    hp = h * (1 - h)
    assert abs(hp - (1 - h) * h) <= 2e-16
    scalar_fields.append(dict(relative_position=x,logistic=h,
                              sylvester_multiplier=1-h))
result = dict(status="DIAGNOSTIC_ONLY",alpha=alpha,scale_start=s0,
              worst_scale_constant_margin=alpha*(s0/32-math.log(4))-
                   math.log(2)-alpha*s0/64,
              exact_formula_fixtures=rows,scalar_sylvester_fixtures=scalar_fields,
              scope="Closed-form float checks; proof is analytic; not MI integration or KLS validation")
Path(__file__).with_name("obstruction_check.json").write_text(json.dumps(result,indent=2))
print(json.dumps({k:result[k] for k in ["status","alpha","scale_start","worst_scale_constant_margin"]}))
