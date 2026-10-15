#!/usr/bin/env python3
"""Arithmetic diagnostics for REPORT.md. No simulation or laboratory evidence."""
from decimal import Decimal, localcontext
from pathlib import Path
import json
import sys


def main():
    with localcontext() as ctx:
        ctx.prec = 70
        D = Decimal
        mu = beta = gamma = D(1)
        budget = D(100)
        delta = D('0.05')
        demand = (1 - 2 * delta) * ((1 - delta) / delta).ln()
        rows = []
        checks = 0
        for exponent in range(0, 17, 2):
            b = D(10) ** exponent
            s = (gamma + (gamma * gamma + 4 * b / beta).sqrt()) / (2 * b)
            residual = b * s * s - gamma * s - 1 / beta
            assert abs(residual) < D('1e-60')
            checks += 1
            kl = mu * beta * gamma * gamma * budget * s
            bayes_floor = max(D(0), (1 - (kl / 2).sqrt()) / 2)
            rows.append({
                'b': str(b),
                'second_moment_upper': str(s),
                'path_KL_upper_at_total_time_100': str(kl),
                'equal_prior_error_lower_Pinsker': str(bayes_floor),
                'necessary_total_time_for_each_error_0_05': str(demand / (mu * beta * gamma * gamma * s)),
                'unstable_minimum_displacement': str((gamma / b).sqrt()),
                'unstable_release_energy': str(gamma * gamma / (4 * b)),
            })

        # General adaptive bounded-control moment bound, normalized units.
        G, F, eta, b = D(2), D(3), D(1), D(10) ** 12
        C, H = G + gamma + eta / 2, 1 / beta + F * F / (2 * eta)
        s = (C + (C * C + 4 * b * H).sqrt()) / (2 * b)
        assert abs(b * s * s - C * s - H) < D('1e-59')
        checks += 1
        controlled = {
            'G': str(G), 'F': str(F), 'eta': str(eta), 'b': str(b),
            'C': str(C), 'H': str(H), 'second_moment_upper': str(s),
            'KL_upper_at_total_time_100': str(mu * beta * gamma * gamma * budget * s),
        }

        # Rigorous formulas; Decimal arithmetic here is not an interval enclosure.
        pi = D('3.1415926535897932384626433832795028841971693993751058209749445923078164')
        linear = []
        for d in [1, 10, 1000, 1000000]:
            dd, a, diffusion = D(d), D(1), D(1)
            h = dd * diffusion / (a * delta)
            t = (1 + 2 * dd / (pi * delta ** 3)).ln() / (2 * a)
            q = diffusion * ((2 * a * t).exp() - 1) / a
            fp = dd * diffusion / (a * h)
            fn = (2 * h / (pi * q)).sqrt()
            assert abs(fp - delta) < D('1e-65')
            assert abs(fn - delta) < D('1e-65')
            checks += 2
            linear.append({
                'd': d, 'a': str(a), 'diffusion_D': str(diffusion),
                'threshold_h': str(h), 'sufficient_time_T': str(t),
                'stable_error_upper': str(fp), 'unstable_error_upper': str(fn),
                'noise_injection_into_half_norm_squared_per_time': str(dd * diffusion),
            })

        # exp(A) acting on e2 for A=[[-1,100],[0,-1]].
        nonnormal_norm_squared = D(10001) * D(-2).exp()
        assert nonnormal_norm_squared > 1000
        checks += 1
        result = {
            'status': 'MODEL_ARITHMETIC_ONLY',
            'precision_decimal_digits': ctx.prec,
            'interval_certified': False,
            'simulation': False,
            'laboratory_evidence': False,
            'units': 'dimensionless model normalization; no mapping to a physical specimen',
            'checks_passed': checks,
            'quartic_mu_beta_gamma': ['1', '1', '1'],
            'quartic_total_interrogation_time': str(budget),
            'quartic_rows': rows,
            'bounded_adaptive_control_example': controlled,
            'linear_OU_planning': linear,
            'nonnormal_stable_eigenvalues': ['-1', '-1'],
            'nonnormal_K_100_time_1_seed_e2_norm_squared': str(nonnormal_norm_squared),
            'limitations': [
                'Finite arithmetic checks are not a universal proof.',
                'No specimen, gain actuator, noise metric, reset, or detector was acquired.',
                'Necessary quartic times apply only to the stated bounded-force/gain thermal-trajectory interface.',
            ],
        }
        out = Path(__file__).resolve().with_name('RESULTS.json')
        out.write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps({'status': result['status'], 'checks_passed': checks, 'output': str(out), 'python': sys.version.split()[0]}))


if __name__ == '__main__':
    main()
