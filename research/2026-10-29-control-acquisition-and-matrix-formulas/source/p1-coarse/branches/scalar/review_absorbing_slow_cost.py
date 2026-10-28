"""Independent exact replay of seven cap-free scalar family receipts.

No source-module import, finite hidden truncation, or stochastic acquisition.
Infinite-dimensional and all-scale arguments are in the companion review.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def main():
    source_path = ROOT / 'results' / 'ABSORBING_SLOW_FAMILY.json'
    data = json.loads(source_path.read_text())
    expected_scales = [4, 8, 16, 32, 64, 128, 1024]
    assert len(data['cases']) == len(expected_scales)
    assert F(19, 48) + F(9, 512) == F(635, 1536) < F(1, 2)
    assert F(4, 7) + F(4, 55) == F(248, 385)
    assert F(1, 2) + F(248, 385) / 16 == F(208, 385)
    assert 2 * F(208, 385) * F(4, 7) == F(1664, 2695) < 1

    verified = []
    count = 0
    for denominator, saved in zip(expected_scales, data['cases']):
        g = F(1, denominator)
        assert F(saved['g']['fraction']) == g
        horizon = saved['horizon']
        h = horizon - 1
        assert F(1, 4) ** h <= g / 8
        assert h > 0 and F(1, 4) ** (h - 1) > g / 8
        assert h <= 8 / g

        # Independent closed forms, including a factored source-form bound.
        eventual_return = g*g/3 + g**3/128
        pending_upper = g*F(1, 4)**h/2 + g**3/16
        u = g*g/3 + 9*g**3/128 + g*F(1, 4)**h/2
        assert eventual_return + pending_upper == u
        absorption = g - u
        dissipation = g*(2-g)
        denominator_form = dissipation - 2*u + u*u
        assert denominator_form == (g-u)*(2-g-u) > 0
        local_form = (1-u)/denominator_form
        q_form = u*(dissipation-u)/denominator_form
        weighted = 2*q_form/dissipation
        unweighted = F(1, 4) + g**4/768
        expected_steps = 1 + 2*g/3 + g**3*h/16

        values = dict(
            g=g,
            boundary_model=1-g,
            slow_total_coupling=g**3/16,
            eventual_return_probability=eventual_return,
            pending_probability_upper=pending_upper,
            return_or_pending_probability_upper=u,
            absorption_probability_lower=absorption,
            local_inverse_dissipation_upper=local_form,
            true_residual_form_upper=q_form,
            uniform_weighted_dynamic_bound=weighted,
            weighted_bound_divided_by_g=weighted/g,
            uniform_unweighted_dynamic_bound=unweighted,
            expected_steps_per_trial_upper=expected_steps,
        )
        for key, value in values.items():
            assert F(saved[key]['fraction']) == value, (g, key)
            assert saved[key]['diagnostic'] == float(value), (g, key)
            count += 1

        # These inequalities instantiate the all-scale proof, not a new sweep.
        assert u <= F(635, 1536)*g*g < g*g/2
        assert absorption >= 7*g/8
        assert 2-g-u >= F(55, 32)
        assert local_form <= F(248, 385)/g
        assert q_form <= F(208, 385)*g*g
        assert weighted <= F(1664, 2695)*g < g
        assert unweighted >= F(1, 4)
        assert expected_steps <= 1 + 2*g/3 + g*g/2 < 2
        assert g/2-g**3/16 > 0
        assert F(3, 4)-g/2 > 0
        assert saved['all_exact_inequalities_passed'] is True
        verified.append(dict(
            g=str(g), horizon=horizon,
            weighted_bound=str(weighted), weighted_diagnostic=float(weighted),
            unweighted_bound=str(unweighted), unweighted_diagnostic=float(unweighted),
            expected_steps_upper=str(expected_steps),
            exact_fraction_fields_verified=len(values),
        ))

    paths = [
        'ABSORBING_BOUNDARY_EXTENSIONS.md',
        'core/absorbing_slow_family.py',
        'results/ABSORBING_SLOW_FAMILY.json',
        'branches/scalar/CALIBRATION_COST_THEOREM_REVIEW.md',
    ]
    reviewed_prefix = (ROOT/'ABSORBING_BOUNDARY_EXTENSIONS.md').read_text().split('## 3.', 1)[0]
    prefix_sha256 = hashlib.sha256(reviewed_prefix.encode()).hexdigest()
    assert prefix_sha256 == '413060e0c8bbc6bc3ae0136bd95e0533481afbe8a05f3ec8fea1233f8a476833'
    report = dict(
        passed=True,
        scope='Sections 1-2 only: seven saved exact family receipts and their scalar constants. No stochastic trials, matrix/domain re-audit, or sensor review.',
        exact_fraction_fields_verified=count,
        input_sha256={p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
        reviewed_sections_1_2_sha256=prefix_sha256,
        cases=verified,
        ordinary_proof_obligation='Norm one, absence of fixed live vectors, and all-scale statistical costs are established in ABSORBING_SLOW_COST_REVIEW.md, not inferred from these finite receipts.',
        limitation='The uncensored mean slow-excursion length is infinite: sum_n w_n/eta_n = sum_n 1/8. Finite censoring and its unresolved-mass bound are essential.',
    )
    output = HERE / 'ABSORBING_SLOW_COST_REVIEW_CHECKS.json'
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(passed=True, cases=len(verified), exact_fraction_fields_verified=count, output=str(output))))


if __name__ == '__main__':
    main()
