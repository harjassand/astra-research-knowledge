#!/usr/bin/env python3
"""Independent finite checks for the reconstruction and stronger coherent bound.

No imported source scripts are run. Results are finite algebra/numerical checks,
not an asymptotic theorem, device qualification, or external validation.
"""
import itertools
import json
import math
from pathlib import Path

import numpy as np
import sympy as s

I = s.eye(2)
X = s.Matrix([[0, 1], [1, 0]])
Y = s.Matrix([[0, -s.I], [s.I, 0]])
Z = s.diag(1, -1)
P0 = s.diag(1, 0)
P1 = s.diag(0, 1)
kron = s.kronecker_product


def equal(a, b):
    if isinstance(a, s.MatrixBase):
        assert a.shape == b.shape
        assert all(s.simplify(v) == 0 for v in a - b), (a, b)
    else:
        assert s.simplify(a - b) == 0, (a, b)


def vec(a):
    return s.Matrix(list(a))


def choi(a):
    return vec(a) * vec(a).conjugate().T


def partial_out(j, di=2, do=2):
    return s.Matrix(di, di, lambda i, k: sum(j[o * di + i, o * di + k] for o in range(do)))


results = {}

# Weighted CP-majorant frontier for an exactly solvable local coherent channel.
c, sn = s.Rational(4, 5), s.Rational(3, 5)
u = c * I - s.I * sn * X
ji, ju, jx = choi(I), choi(u), choi(X)
support = (ji + jx) / 2
equal(support * support, support)
weighted = []
for a in (s.Rational(0), s.Rational(1, 10), s.Rational(14, 25), s.Rational(1), s.Rational(9, 4), s.Rational(100)):
    delta = ju - a * ji
    d = s.sqrt((1 - a) ** 2 + 4 * a * sn ** 2)
    lp, lm = 1 - a + d, 1 - a - d
    zplus = s.simplify(lp / (2 * d)) * (delta - lm * support)
    equal(zplus * zplus, lp * zplus)
    equal((zplus - delta) * (zplus - delta), (-lm) * (zplus - delta))
    b = (1 - a + d) / 2
    equal(partial_out(zplus), b * I)
    equal(partial_out(zplus - delta), (b - 1 + a) * I)
    assert float(lp) >= 0 and float(-lm) >= 0
    weighted.append({"a": str(a), "b": str(b)})
results["weighted_unitary_cp_majorants"] = weighted

# Exact minimizer and a matching two-dimensional acceptance witness.
f = s.Rational(9, 25)
rf, tf = s.Rational(3, 5), s.Rational(4, 5)
aopt = c ** 2 - sn ** 2 + c * sn * (1 - 2 * f) / (rf * tf)
bopt = (1 - aopt + s.sqrt((1 - aopt) ** 2 + 4 * aopt * sn ** 2)) / 2
beta = (c * rf + sn * tf) ** 2
equal(aopt, s.Rational(14, 25))
equal(aopt * f + bopt, beta)
equal(beta, s.Rational(576, 625))
psi = s.Matrix([tf, rf])
rotation = s.Matrix([[c, -sn], [sn, c]])
equal((rotation * psi)[1] ** 2, beta)
results["exact_angle_frontier_example"] = {"f": str(f), "cos_theta": str(c), "sin_theta": str(sn),
    "a_opt": str(aopt), "b_opt": str(bopt), "coherent_bound": str(beta), "diamond_bound": str(f + sn)}

# A small coherent example and exact angle composition over two slots.
cc, ss = s.Rational(9999, 10001), s.Rational(200, 10001)
rr, tt = s.Rational(200, 10001), s.Rational(9999, 10001)
equal(cc ** 2 + ss ** 2, 1)
equal(rr ** 2 + tt ** 2, 1)
first_r, first_t = cc * rr + ss * tt, cc * tt - ss * rr
assert first_t > 0
second_r = cc * first_r + ss * first_t
cos_two, sin_two = cc ** 2 - ss ** 2, 2 * cc * ss
equal(second_r ** 2, (cos_two * rr + sin_two * tt) ** 2)
results["small_coherent_example"] = {
    "f_exact": str(rr ** 2), "one_slot_angle_bound_exact": str(first_r ** 2),
    "one_slot_angle_bound_float": float(first_r ** 2), "generic_half_diamond_bound_float": float(rr ** 2 + ss),
    "two_slot_composition_exact": str(second_r ** 2), "two_slot_angle_addition": "PASS"}

# The coherent bound cannot be inferred from a diamond number or a mean angle.
eps = s.Rational(1, 100)
results["stochastic_floor_counterexample"] = {"actual_bad": str(eps),
    "invalid_using_epsilon_as_coherent_angle": float(s.sin(eps) ** 2)}
assert float(s.sin(eps) ** 2) < float(eps)
results["rare_large_seed_angle_counterexample"] = {"large_rotation_probability": str(eps),
    "actual_bad": str(eps), "invalid_mean_angle_bound": float(s.sin(eps * s.pi / 2) ** 2),
    "weighted_cp_frontier_at_f_zero": str(eps)}
assert float(s.sin(eps * s.pi / 2) ** 2) < float(eps)

# The unitary angle uses the numerical range, not normalized Choi overlap.
u3 = s.diag(1, 1, -1)
psi3 = s.Matrix([1, 0, 1]) / s.sqrt(2)
accept3 = s.Matrix([1, 0, -1]) / s.sqrt(2)
equal((accept3.conjugate().T * psi3)[0], 0)
equal(abs((accept3.conjugate().T * u3 * psi3)[0]) ** 2, 1)
results["choi_overlap_is_not_uniform_unitary_angle"] = {
    "unitary": "diag(1,1,-1)", "normalized_choi_overlap": "1/3",
    "false_f_zero_bound_from_choi_overlap": "8/9", "actual_f_zero_acceptance": "1",
    "correct_numerical_range_distance": "0", "correct_angle": "pi/2"}

# A code of distance two: each elementary one-qubit footprint passes, their union fails.
paulis = [I, X, Y, Z]
xxxx, zzzz = kron(X, X, X, X), kron(Z, Z, Z, Z)
id16 = s.eye(16)
code_p = (id16 + xxxx) * (id16 + zzzz) / 4
equal(code_p * code_p, code_p)
single_counts = []
for site in (0, 1):
    commuting = []
    for name, p in zip(("I", "X", "Y", "Z"), paulis):
        factors = [I] * 4
        factors[site] = p
        op = kron(*factors)
        if op * xxxx == xxxx * op and op * zzzz == zzzz * op:
            commuting.append(name)
    assert commuting == ["I"]
    single_counts.append(commuting)
x1, x2 = kron(X, I, I, I), kron(I, X, I, I)
logical = x1 * x2
equal(logical * xxxx, xxxx * logical)
equal(logical * zzzz, zzzz * logical)
assert all(logical != stabilizer and logical != -stabilizer for stabilizer in (id16, xxxx, zzzz, xxxx * zzzz))
ghz = s.zeros(16, 1)
ghz[0] = ghz[15] = 1 / s.sqrt(2)
equal(code_p * ghz, ghz)
equal((ghz.conjugate().T * logical * ghz)[0], 0)
actual = (c * id16 - s.I * sn * x2) * (c * id16 - s.I * sn * x1)
good_k = code_p * actual * code_p
equal(good_k, c ** 2 * code_p - sn ** 2 * logical * code_p)
good_output = good_k * ghz
good_probability = (good_output.conjugate().T * good_output)[0]
equal(good_probability, s.Rational(337, 625))
results["propagated_union_counterexample"] = {
    "code": "<XXXX,ZZZZ>, [[4,2,2]]", "individual_single_site_centralizers": single_counts,
    "union_undetected_logical": "X1 X2", "endpoint_good_probability": str(good_probability),
    "endpoint_good_kraus_on_code": "(16/25) I_logical - (9/25) X1X2_logical",
    "orthogonal_logical_component_unconditional_weight": str(sn ** 4)}

# Trusted endpoint projections need an immutable comparator, not a mutable working copy.
input_sr = kron(P0, P0)
flip_both = kron(X, X)
output_sr = flip_both * input_sr * flip_both
equal(output_sr, kron(P1, P1))
results["mutable_comparator_counterexample"] = {"true_entry_r": 0, "reported_entry_copy_after_fault": 1,
    "exact_final_t": 1, "reported_bad_flag": 0, "true_syndrome_change": 1}

# Logical coherent error has no nonzero ideal CP minorant.
a = s.symbols("a", positive=True)
basis = s.Matrix.hstack(vec(I) / s.sqrt(2), vec(X) / s.sqrt(2))
minor = s.factor((basis.conjugate().T * (ju - a * ji) * basis).det())
equal(minor, -4 * a * sn ** 2)
results["coherent_no_ideal_minorant_determinant"] = str(minor)

# Exact finite pulse and the cheap Schur-resolution bracket.
omega = s.symbols("Omega", positive=True)
j = s.sqrt(5) * omega
frequency = s.sqrt(omega ** 2 + j ** 2 / 4)
finite_bad = s.simplify(omega ** 2 / frequency ** 2 * s.sin(s.pi / omega * frequency) ** 2)
equal(finite_bad, s.Rational(4, 9))
results["finite_pulse"] = {"selected_branch_bad": str(finite_bad), "fair_seed_bad": str(finite_bad / 2),
    "baseline_old_coarse_odd_action": "0"}
p = q = s.Rational(1, 10000)
mu = s.Rational(1, 4)
h = s.sqrt(p * q * (1 - p) * (1 - q))
qq = p + q - p * q
upper = qq + 2 * h * mu
lower = qq + max(s.Rational(0), 2 * h * mu - p * q)
equal(upper - lower, p * q)
results["schur_resolution"] = {"L": str(lower), "U": str(upper), "width": str(upper - lower)}

# Same terminal joint channel need not mean the same two-port strategy.
swap = s.Matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
equal(swap * swap, s.eye(4))
intervene = kron(X, I)
reference_output = intervene * input_sr * intervene
actual_output = swap * intervene * swap * input_sr * swap * intervene * swap
equal(reference_output, kron(P1, P0))
equal(actual_output, kron(P0, P1))
results["terminal_channel_vs_strategy"] = {"terminal_joint_channel_without_intervention": "Id exactly in both cases",
    "intervening_X_on_system_reference_output": "|10>", "intervening_X_on_system_actual_output": "|01>",
    "process_distinguishability": "1"}

# Full-input effect checks with interleaved parents and a shared, noncommuting bath.
ni, nx, ny, nz = [np.array(m, dtype=complex) for m in (I, X, Y, Z)]
np0, np1 = np.array(P0, dtype=complex), np.array(P1, dtype=complex)


def nk(*factors):
    out = np.array([[1]], dtype=complex)
    for factor in factors:
        out = np.kron(out, factor)
    return out


def unitary(hermitian, angle):
    vals, vectors = np.linalg.eigh(hermitian)
    return (vectors * np.exp(-1j * angle * vals)) @ vectors.conj().T


hy1, hy2 = nk(ny, ni, ni), nk(ni, ny, ni)
error11, error12 = nk(nx, ni, nz), nk(ny, ni, nx)
error21, error22 = nk(ni, nx, ny), nk(ni, ny, nz)
free1, free2, free3 = nk(nz, nz, nz), nk(ni, nz, nx), nk(nz, ni, ny)
assert np.linalg.norm(error11 @ error21 - error21 @ error11, ord=2) > 1.9
rng = np.random.default_rng(20261016)
fixture_results = []
for fixture in range(30):
    a1, a2 = rng.uniform(0.01, 0.16, size=2)
    d11, d12, d21, d22 = rng.uniform(0.001, 0.03, size=4)
    free_angles = rng.uniform(-2.0, 2.0, size=3)
    chronological = [(free1, free_angles[0]), (hy1, 0.4 * a1), (hy2, 0.5 * a2),
        (error11, d11), (free2, free_angles[1]), (error21, d21), (hy2, 0.5 * a2),
        (free3, free_angles[2]), (error12, d12), (hy1, 0.6 * a1), (error22, d22)]
    joint_u = np.eye(8, dtype=complex)
    for generator, angle in chronological:
        joint_u = unitary(generator, angle) @ joint_u
    effect = np.zeros((8, 8), dtype=complex)
    for r0, r1 in itertools.product(range(2), repeat=2):
        projectors = [np0, np1]
        pin = nk(projectors[r0], projectors[r1], ni)
        pout = nk(projectors[1 - r0], projectors[1 - r1], ni)
        effect += pin @ joint_u.conj().T @ pout @ joint_u @ pin
    bound = math.sin(a1 + d11 + d12) ** 2 * math.sin(a2 + d21 + d22) ** 2
    eig = np.linalg.eigvalsh(effect)
    slack = bound - float(eig[-1])
    assert slack >= -1e-12, (fixture, eig[-1], bound)
    fixture_results.append({"fixture": fixture, "max_full_input_effect_eigenvalue": float(eig[-1]),
        "coherent_product_bound": bound, "minimum_domination_slack": slack})
results["shared_bath_full_input_effect_tests"] = {"fixtures": len(fixture_results),
    "noncommuting_cross_parent_bath_error_commutator_norm": float(np.linalg.norm(error11 @ error21 - error21 @ error11, ord=2)),
    "minimum_slack": min(item["minimum_domination_slack"] for item in fixture_results),
    "largest_effect": max(item["max_full_input_effect_eigenvalue"] for item in fixture_results),
    "details": fixture_results}
results["status"] = "PASS"
results["scope"] = "Finite exact algebra and deterministic floating-point full-input checks only. General claims rely on DERIVATION.md."
destination = Path(__file__).with_name("results.json")
destination.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps({key: value for key, value in results.items() if key != "shared_bath_full_input_effect_tests"}, indent=2))
print(json.dumps({"shared_bath_summary": {key: value for key, value in results["shared_bath_full_input_effect_tests"].items() if key != "details"}}, indent=2))
