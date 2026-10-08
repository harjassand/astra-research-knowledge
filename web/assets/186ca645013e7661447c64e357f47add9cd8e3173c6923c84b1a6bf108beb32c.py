"""Independent exact diagnostics; the all-state proof is in INDEPENDENT_PROOF.md.

No candidate verification script was read or imported. No Monte Carlo inference.
Run from the workspace root with python3 work/agents/chemistry_audit/independent_checks.py.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

OUT = Path(__file__).parent


def H(b):
    return Q(3, 2) * ((b + 1) // 2) + (Q(1, 2) if b == 1 else 0)


def F(b):
    return 0 if b == 0 else (5 if b == 1 else 2 ** b)


def ff(a, k):
    if a < k:
        return 0
    z = 1
    for i in range(k):
        z *= a - i
    return z


def check_state(a, b, coeff):
    c0, c2, c3, c4, c5 = coeff
    d = c4 + c5
    s = c3 * b + c2 / (a - 2)
    death = d * b * (b - 1)
    qb = s + death
    hraw = s * (H(b + 1) - H(b))
    hraw += death * (H(max(b - 2, 0)) - H(b) + 1)
    assert hraw <= 0, (a, b, coeff, hraw)

    d0_f = F(max(b - 2, 0))
    d1_f = 0 if a == 3 else d0_f  # killed on the first A=2 state
    stopped = (s * F(b + 1) + b * (b - 1) * (c4 * d0_f + c5 * d1_f)) / qb
    assert stopped <= Q(4, 5) * F(b)

    qfull = c0 + ff(a, 3) * qb
    full_f = (c0 * F(b) + ff(a, 3) * qb * stopped) / qfull
    z = c0 / (c0 + 6 * c3)
    gamma = z + (1 - z) * Q(4, 5)
    assert full_f <= gamma * F(b)
    assert c0 / qfull <= z < 1

    # Exact reset distribution conditional on a B-changing event at this state.
    # An ignored input run is an a.s.-finite mixture of these statewise cases.
    if a == 3 and b > 2:
        d1_macro_f = (c0 * F(b - 2) + 2 * c2 * F(b - 1)) / (c0 + 2 * c2)
    else:
        d1_macro_f = d0_f  # in particular, stop immediately when b=2
    macro = (s * F(b + 1) + b * (b - 1) * (c4 * d0_f + c5 * d1_macro_f)) / qb
    assert macro <= Q(4, 5) * F(b)
    return stopped / F(b), macro / F(b), full_f / F(b)


fixture = tuple(map(Q, (1, 1, 1, 4, 1)))
parameters = [fixture]
for c0, c2, c3, c4, c5 in product(
    [Q(1, 1000), Q(1), Q(10**6)],
    [Q(19, 20), Q(21, 20)],
    [Q(19, 20), Q(21, 20)],
    [Q(79, 20), Q(81, 20)],
    [Q(19, 20), Q(21, 20)],
):
    d = c4 + c5
    assert 3 * (2 * c3 + c2) < 2 * d
    assert 8 * (3 * c3 + c2) < 7 * d
    assert 2 * c5 < d
    parameters.append((c0, c2, c3, c4, c5))

nchecks = 0
max_stopped = Q(0)
max_macro = Q(0)
max_full = Q(0)
for coeff in parameters:
    avals = range(3, 51) if coeff == fixture else [3, 4, 10, 100]
    bvals = range(1, 257) if coeff == fixture else range(1, 129)
    for a, b in product(avals, bvals):
        r1, r2, r3 = check_state(a, b, coeff)
        max_stopped = max(max_stopped, r1)
        max_macro = max(max_macro, r2)
        max_full = max(max_full, r3)
        nchecks += 1

# Exhaust the small boundary, including every enabled jump's destination.
jumps = [(2, 0), (1, 1), (0, 1), (0, -2), (-1, -2)]
boundary_checks = 0
for a, b in product(range(8), range(8)):
    rates = [1, ff(a, 2), ff(a, 3) * b, 4 * ff(a, 3) * ff(b, 2), ff(a, 3) * ff(b, 2)]
    for rate, (da, db) in zip(rates, jumps):
        if rate:
            assert a + da >= 0 and b + db >= 0
            if a >= 2:
                assert a + da >= 2
    if a < 2:
        assert [i for i, z in enumerate(rates) if z] == [0]
    if a == 2:
        assert [i for i, z in enumerate(rates) if z] == [0, 1]
    boundary_checks += 1

# Independent exact source-face certificate, including every tied outgoing arrow.
sources = [(0, 0), (2, 0), (3, 1), (3, 2)]
arrows = [[(2, 0)], [(1, 1)], [(0, 1)], [(0, -2), (-1, -2)]]
normals = [(0, -1), (1, -1), (1, 0), (-2, 3)]
dot = lambda x, y: x[0] * y[0] + x[1] * y[1]
faces = []
for normal in normals:
    top = max(dot(normal, s) for s in sources)
    rows = []
    for s, out in zip(sources, arrows):
        if dot(normal, s) == top:
            rows.extend({'source': s, 'arrow': v, 'projection': dot(normal, v)} for v in out)
    assert all(z['projection'] <= 0 for z in rows)
    assert any(z['projection'] < 0 for z in rows)
    faces.append({'normal': normal, 'rows': rows})
for i, out in enumerate(arrows):
    for v in out:
        p = [dot(normals[(i - 1) % 4], v), dot(normals[i], v)]
        assert max(p) <= 0 and min(p) < 0

# Counterexample to conditioning death marks as though their count were independent.
# From (3,3), D=1 cannot reach B=0; it must stop at A=2 and its only death is D1.
counterexamples = {
    'death_mark_dependence': {
        'initial_state': [3, 3],
        'first_D1_probability': str(Q(36, 205)),
        'conditional_D1_count_given_D_equals_1': 1,
        'false_binomial_mark_probability': str(Q(1, 5)),
        'reason': 'With only one pair death, B remains positive. Termination must be A=2; hence its sole death is D1.',
    },
    'zero_c0': {'initial_state': [0, 0], 'all_rates': [0, 0, 0, 0, 0], 'explosion_probability': 0},
    'zero_c2_axis': {'initial_B': 0, 'only_enabled_reaction': 'constant-rate +2A input', 'explosion_probability': 0},
    'untruncated_ordinary_powers': {'state': [1, 1], 'D0_rate': 4, 'D0_destination': [1, -1], 'valid_CTMC_on_N0_squared': False},
    'products_need_not_belong_to_source_hull': {'product': [3, 0], 'violated_source_hull_edge_inequality': 'b >= a-2'},
    'no_deterministic_explosion_deadline': {'initial_state': [0, 0], 'bound': 'P(T_infinity>t) >= exp(-t) > 0 for every finite t>0'},
    'irreducibility_does_not_amplify_to_one': {
        'state_space': 'Z',
        'outward_jump_probability_off_zero': str(Q(3, 4)),
        'rate_positive_states': 'n+1',
        'rate_negative_states': '(|n|+1)^2',
        'rate_zero': 1,
        'first_direction_probability': str(Q(1, 2)),
        'never_return_probability_after_first_step': str(Q(2, 3)),
        'explosion_probability_lower_bound': str(Q(1, 3)),
        'nonexplosion_probability_lower_bound': str(Q(1, 3)),
        'proof_location': 'COUNTEREXAMPLES.md',
    },
}
result = {
    'status': 'PASS finite exact arithmetic only; not a theorem proof',
    'candidate_verification_code_read': False,
    'local_state_parameter_cases': nchecks,
    'parameter_tuples': len(parameters),
    'boundary_states': boundary_checks,
    'maximum_stopped_B_event_ratio': str(max_stopped),
    'maximum_reset_macro_ratio': str(max_macro),
    'maximum_full_reaction_ratio_over_grid': str(max_full),
    'geometry_faces': faces,
    'counterexamples': counterexamples,
}
(OUT / 'independent_checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k not in ['geometry_faces', 'counterexamples']}, indent=2))
