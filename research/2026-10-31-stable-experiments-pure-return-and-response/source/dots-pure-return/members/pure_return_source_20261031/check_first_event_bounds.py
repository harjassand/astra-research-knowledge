"""Scalar diagnostic only; not a simulator or a replacement for the proof."""
import json
import math
from pathlib import Path

rows = []
worst_accept = 0.0
worst_mass_ratio = 0.0
for m in (1, 2, 8, 64):
    a = -math.expm1(-math.log(2) / m) / 2
    for B in (1e-6, 0.1, 1.0, 100.0):
        for ratio in (1.0, 16.0, 1e6):
            mu = 4096 * B * m*m * ratio
            c = math.sqrt(mu*B)
            r = a*mu
            delta = r-2*c
            nu = math.hypot(delta, math.sqrt(8)*c)
            down = (nu+delta)/2
            slow = 2*c*c/down
            tau = 2.0**(-math.ceil(math.log2(max(1.0, 512*m*B))))
            amp = 256 * 2**math.ceil(math.log(m, 4))
            no_sq = 64*math.exp(2*slow*tau)
            integral = 1024*math.exp(2*slow*tau)*(
                mu*(-math.expm1(-2*delta*tau))/(2*delta)
                + B*tau/(a*a))
            mass_ratio = (no_sq+integral)/(amp*amp)
            worst_mass_ratio = max(worst_mass_ratio, mass_ratio)
            assert r >= 8*c*(1-1e-12)
            assert slow*tau <= 1/24+1e-12
            assert no_sq+integral < 4096/a
            assert mass_ratio < 1
            for fraction in (0., 1e-8, .01, .2, .7, 1.):
                u = tau*fraction
                es = math.exp(slow*u)
                ed = math.exp(-down*u)
                e00 = down/nu*es + slow/nu*ed
                e01 = 2*c/nu*(es-ed)
                e11 = 2*(slow/nu*es+down/nu*ed)
                assert max(e00, e01, e11) <= 2*math.exp(slow*tau)*(1+1e-12)
                jump_alpha = 32*math.exp(slow*tau)*math.sqrt(
                    mu*math.exp(-2*delta*u)+B/(a*a))
                accept = max(4*math.sqrt(mu)*e01/jump_alpha,
                             4*math.sqrt(mu)*e11/jump_alpha)
                worst_accept = max(worst_accept, accept)
                assert accept <= 1+1e-12
            rows.append(dict(m=m, B=B, mu=mu, tau=tau,
                             slow_times_tau=slow*tau,
                             complete_mass=no_sq+integral,
                             padded_normalizer=amp,
                             complete_mass_ratio=mass_ratio))

result = dict(status="scalar diagnostic passed", cases=len(rows),
              maximum_jump_acceptance_amplitude=worst_accept,
              maximum_mass_over_padded_normalizer_squared=worst_mass_ratio,
              exclusions="Not an implemented quantum compiler, source certificate, or proof.",
              cases_data=rows)
out = Path(__file__).with_name("first_event_scalar_bounds.json")
out.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k != "cases_data"}, indent=2))
