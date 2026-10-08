#!/usr/bin/env python3
"""Exact small-instance replay of the finite EB comparator compiler.

All channel, effect, completion, and final-certificate arithmetic is exact
SymPy rational/complex-rational arithmetic.  The 16-outcome tree is fully
enumerated only as a small-instance diagnostic oracle.  The separate
recursive sampler implements the polynomial-message correlated sampler and
is checked against that oracle pointwise in law and by seeded draws.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from decimal import Decimal, localcontext
from functools import reduce
from math import gcd
from pathlib import Path

import sympy as sp
from sympy import I, Matrix, Rational, eye, zeros
from sympy.matrices import kronecker_product


ROOT = Path(__file__).resolve().parent
D = 2
I2 = eye(2)
I4 = eye(4)
P_X = Matrix([[0, 1], [1, 0]])
P_Y = Matrix([[0, -I], [I, 0]])
P_Z = Matrix([[1, 0], [0, -1]])
PAULI = [P_X, P_Y, P_Z]
BASIS = [I2, P_X, P_Y, P_Z]


def clean(x):
    return sp.cancel(sp.expand_complex(x))


def clean_matrix(a):
    return a.applyfunc(clean)


def is_zero(x):
    return clean(x) == 0


def exact_nonnegative(x):
    x = clean(sp.re(x))
    truth = x.is_nonnegative
    if truth is None:
        truth = sp.ask(sp.Q.nonnegative(x))
    if truth is not True:
        raise AssertionError(f"not certified nonnegative: {x}")
    return True


def psd2(a):
    a = clean_matrix(a)
    assert a == a.H
    exact_nonnegative(a[0, 0])
    exact_nonnegative(a[1, 1])
    exact_nonnegative(a.det())
    return True


def principal_minor_psd(a):
    """Exact Hermitian PSD check by all principal minors (small matrices)."""
    a = clean_matrix(a)
    assert a == a.H
    n = a.rows
    for mask in range(1, 1 << n):
        inds = [i for i in range(n) if (mask >> i) & 1]
        exact_nonnegative(a.extract(inds, inds).det())
    return True


def ptrace_right(y):
    # Y is on C^2 (left) tensor C^2 (right).
    return clean_matrix(Matrix(2, 2, lambda i, k: sum(y[2*i+j, 2*k+j] for j in range(2))))


def ptrace_left(y):
    return clean_matrix(Matrix(2, 2, lambda j, l: sum(y[2*i+j, 2*i+l] for i in range(2))))


def conditional_right(y, e_left):
    return ptrace_left(kronecker_product(e_left, I2) * y)


def make_broadcaster():
    # Dephasing copier Kraus operators |00><0| and |11><1|.
    k0 = zeros(4, 2)
    k1 = zeros(4, 2)
    k0[0, 0] = 1
    k1[3, 1] = 1

    # Universal 1->2 qubit cloner Kraus numerators.  The physical Kraus
    # operators are A_j/sqrt(6), while the exact map uses A_j X A_j*/6.
    a0 = zeros(4, 2)
    a1 = zeros(4, 2)
    a0[0, 0] = 2
    a0[1, 1] = 1
    a0[2, 1] = 1
    a1[1, 0] = 1
    a1[2, 0] = 1
    a1[3, 1] = 2

    t = Rational(9, 10)

    def b(x):
        return clean_matrix(
            t * (k0*x*k0.H + k1*x*k1.H)
            + (1-t) * (a0*x*a0.H + a1*x*a1.H) / 6
        )

    def badj(e):
        return clean_matrix(
            t * (k0.H*e*k0 + k1.H*e*k1)
            + (1-t) * (a0.H*e*a0 + a1.H*e*a1) / 6
        )

    data = {"t": t, "K_dephase": [k0, k1], "A_cloner": [a0, a1]}
    return b, badj, data


def make_leaf_effects(axis, gamma):
    p = {"X": P_X, "Y": P_Y, "Z": P_Z}[axis]
    return [clean_matrix((1-gamma)*(I2+s*p)/2 + gamma*I2/2) for s in (1, -1)]


def tree_effects(depth, start, leaf_axes, leaf_fx, badj):
    if depth == 0:
        return {(s,): leaf_fx[start][s] for s in range(2)}
    half = 2**(depth-1)
    left = tree_effects(depth-1, start, leaf_axes, leaf_fx, badj)
    right = tree_effects(depth-1, start+half, leaf_axes, leaf_fx, badj)
    out = {}
    for zl, el in left.items():
        for zr, er in right.items():
            z = zl + zr
            out[z] = clean_matrix(badj(kronecker_product(el, er)))
    return out


def choose_exact(weights, rng):
    vals = [sp.Rational(clean(w)) for w in weights]
    assert all(w >= 0 for w in vals)
    den = sp.ilcm(*[int(w.q) for w in vals])
    ints = [int(w.p * (den // int(w.q))) for w in vals]
    total = sum(ints)
    assert total > 0
    r = rng.randrange(total)
    acc = 0
    for i, mass in enumerate(ints):
        acc += mass
        if r < acc:
            return i
    raise AssertionError("categorical draw escaped support")


def recursive_sample(x, depth, start, leaf_fx, b, badj, rng):
    """Correlated conditional sampler returning labels and their root effect."""
    if depth == 0:
        masses = [clean(sp.trace(f*x)) for f in leaf_fx[start]]
        y = choose_exact(masses, rng)
        return (y,), leaf_fx[start][y]
    y_joint = b(x)
    x_left = ptrace_right(y_joint)
    labels_left, e_left = recursive_sample(
        x_left, depth-1, start, leaf_fx, b, badj, rng
    )
    x_right = conditional_right(y_joint, e_left)
    labels_right, e_right = recursive_sample(
        x_right, depth-1, start + 2**(depth-1), leaf_fx, b, badj, rng
    )
    e = clean_matrix(badj(kronecker_product(e_left, e_right)))
    return labels_left + labels_right, e


def canonical_channel(ensemble, x):
    y = zeros(x.rows, x.cols)
    for effect, state in ensemble:
        y += sp.trace(effect*x) * state
    return clean_matrix(y)


def transfer_matrix(ensemble):
    return clean_matrix(Matrix(4, 4, lambda i, j: sp.trace(BASIS[i]*canonical_channel(ensemble, BASIS[j]))/2))


def choi_from_ensemble(ensemble):
    # For X -> Tr(M X) sigma, J = M^T tensor sigma.
    j = zeros(4, 4)
    for effect, state in ensemble:
        j += kronecker_product(effect.T, state)
    return clean_matrix(j)


def checked_channel(ensemble):
    total_effect = clean_matrix(sum((e for e, _ in ensemble), zeros(2, 2)))
    assert total_effect == I2
    total_prepared = clean_matrix(sum((sp.trace(e)*s for e, s in ensemble), zeros(2, 2)))
    assert total_prepared == I2
    for e, s in ensemble:
        assert psd2(e) and psd2(s)
        assert sp.trace(s) == 1
    r = transfer_matrix(ensemble)
    assert r == r.T
    assert canonical_channel(ensemble, I2) == I2
    for h in BASIS:
        assert sp.trace(canonical_channel(ensemble, h)) == sp.trace(h)
    j = choi_from_ensemble(ensemble)
    assert principal_minor_psd(j)
    return r, j


def sample_histogram(probabilities, n, rng):
    vals = [sp.Rational(clean(p)) for p in probabilities]
    den = sp.ilcm(*[int(p.q) for p in vals])
    masses = [int(p.p * (den // int(p.q))) for p in vals]
    assert sum(masses) == den
    cumulative = []
    acc = 0
    for mass in masses:
        acc += mass
        cumulative.append(acc)
    counts = [0] * len(masses)
    for _ in range(n):
        r = rng.randrange(den)
        lo, hi = 0, len(cumulative)
        while lo < hi:
            mid = (lo+hi)//2
            if r < cumulative[mid]:
                hi = mid
            else:
                lo = mid+1
        counts[lo] += 1
    return counts


def completed_ensemble(effects, probabilities, counts, n, alpha):
    c = Rational(1, 1) / (1 + alpha)
    states = []
    barycenter = zeros(2, 2)
    for e, p, count in zip(effects, probabilities, counts):
        if count == 0:
            continue
        tr_e = sp.trace(e)
        rho = clean_matrix(e / tr_e)
        states.append((rho, count))
        barycenter += Rational(count, n) * rho
    barycenter = clean_matrix(barycenter)
    m0 = clean_matrix(I2 - c*D*barycenter)
    psd2(m0)
    assert sp.trace(m0) == D*(1-c)
    ens = []
    for rho, count in states:
        mi = clean_matrix(c*D*Rational(count, n)*rho)
        ens.append((mi, rho))
    sigma0 = clean_matrix(m0 / sp.trace(m0))
    ens.append((m0, sigma0))
    return ens, barycenter, m0, c


def pauli_twirl(ensemble):
    unitaries = [I2, P_X, P_Y, P_Z]
    twirled = []
    for u in unitaries:
        for e, s in ensemble:
            twirled.append((clean_matrix(u.H*e*u/4), clean_matrix(u.H*s*u)))
    return twirled


def as_fraction_text(x):
    x = clean(x)
    if x.is_Rational:
        return str(x)
    return str(x)


def decimal_weights(q_acc, eta, precision=60):
    with localcontext() as ctx:
        ctx.prec = precision
        eta_d = Decimal(eta.numerator) / Decimal(eta.denominator)
        exps = []
        for value in q_acc:
            v = Decimal(int(value.p)) / Decimal(int(value.q))
            exps.append((eta_d*v).exp())
        total = sum(exps)
        return [x/total for x in exps]


def decimal_score(q, values):
    with localcontext() as ctx:
        ctx.prec = 60
        return sum(qi * (Decimal(int(v.p))/Decimal(int(v.q))) for qi, v in zip(q, values))


def exact_complex_bit_size(z):
    z = clean(z)
    total = 0
    for x in [sp.re(z), sp.im(z)]:
        x = sp.Rational(clean(x))
        total += abs(int(x.p)).bit_length() + int(x.q).bit_length()
    return total


def matrix_payload(a):
    return [[[str(sp.Rational(clean(sp.re(a[i,j])))),
              str(sp.Rational(clean(sp.im(a[i,j]))))]
             for j in range(a.cols)] for i in range(a.rows)]


def matrix_from_payload(payload):
    return Matrix([[sp.Rational(x[0]) + I*sp.Rational(x[1]) for x in row]
                   for row in payload])


def dense_liouville(b):
    matrix_units = [Matrix([[1, 0], [0, 0]]), Matrix([[0, 1], [0, 0]]),
                    Matrix([[0, 0], [1, 0]]), Matrix([[0, 0], [0, 1]])]
    cols = []
    for x in matrix_units:
        y = b(x)
        cols.append(Matrix([y[i, j] for i in range(4) for j in range(4)]))
    return Matrix.hstack(*cols)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=16)
    ap.add_argument("--samples", type=int, default=1024)
    ap.add_argument("--sampler-draws", type=int, default=256)
    ap.add_argument("--seed", type=int, default=20261008)
    ap.add_argument("--delta", default="1/4")
    args = ap.parse_args()
    start_time = time.perf_counter()
    delta = sp.Rational(args.delta)
    assert 0 < delta <= 1
    T, N = args.rounds, args.samples
    assert T > 0 and N > 0
    alpha = Rational(1, 10)
    gamma = Rational(1, 100)
    eta_mw = delta / (4 * 8**2)

    b, badj, bdata = make_broadcaster()
    # Exact CPTP and swap-symmetry certificates for the supplied extension.
    k0, k1 = bdata["K_dephase"]
    a0, a1 = bdata["A_cloner"]
    tp_b = clean_matrix(Rational(9, 10)*(k0.H*k0+k1.H*k1)
                        + Rational(1, 60)*(a0.H*a0+a1.H*a1))
    assert tp_b == I2
    swap = Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
    assert all(swap*k == k for k in [k0, k1, a0, a1])
    # J_B is an exact positive Gram sum with positive rational weights.
    # Flattened unscaled Kraus numerators are the Gram vectors.
    gram_terms = [(Rational(9, 10), k) for k in [k0, k1]]
    gram_terms += [(Rational(1, 60), a) for a in [a0, a1]]
    jb = zeros(8, 8)
    for weight, k in gram_terms:
        v = Matrix([k[i, j] for i in range(4) for j in range(2)])
        jb += weight * v * v.H
    assert jb == jb.H
    assert principal_minor_psd(jb)

    def phi(x):
        return ptrace_right(b(x))

    def phi_other(x):
        return ptrace_left(b(x))

    # Actual dense channel checks: unital, TP, and HS-self-adjoint.
    assert phi(I2) == I2
    for h in BASIS:
        assert sp.trace(phi(h)) == sp.trace(h)
        assert phi(h) == phi_other(h)
    phi_ptm = clean_matrix(Matrix(4, 4, lambda i, j: sp.trace(BASIS[i]*phi(BASIS[j]))/2))
    assert phi_ptm == phi_ptm.T
    assert phi_ptm == Matrix.diag(1, Rational(1, 15), Rational(1, 15), Rational(29, 30))
    lambdas = [Rational(1,15), Rational(1,15), Rational(29,30)]
    gaps = [1-l for l in lambdas]
    m = 2
    j_target = [1-2*m*g for g in gaps]
    assert j_target == [Rational(-41,15), Rational(-41,15), Rational(13,15)]

    # Four leaves realize the d=2, n=3 equal-depth support tree.
    leaf_axes = ["X", "Y", "Z", "Z"]
    leaf_fx = [make_leaf_effects(axis, gamma) for axis in leaf_axes]
    tree = tree_effects(2, 0, leaf_axes, leaf_fx, badj)
    assert len(tree) == 16
    assert clean_matrix(sum(tree.values(), zeros(2,2))) == I2
    for e in tree.values():
        psd2(e)
    labels = sorted(tree)
    probs = [clean(sp.trace(tree[z])/D) for z in labels]
    assert sum(probs) == 1
    assert all(p > 0 for p in probs)
    rare_floor = (gamma/D)**4
    assert all(p >= rare_floor for p in probs)

    # Pointwise sampler factorization for each correlated leaf tuple.
    root_input = I2 / D
    root_y = b(root_input)
    root_left_state = ptrace_right(root_y)
    path_probability_checks = 0
    for z in labels:
        left_effect = tree_effects(1, 0, leaf_axes, leaf_fx, badj)[z[:2]]
        right_effect = tree_effects(1, 2, leaf_axes, leaf_fx, badj)[z[2:]]
        p_left = clean(sp.trace(left_effect*root_left_state))
        right_state = conditional_right(root_y, left_effect)
        p_right_cond = clean(sp.trace(right_effect*right_state) / sp.trace(right_state))
        assert clean(p_left*p_right_cond) == probs[labels.index(z)]
        assert clean(sp.trace(badj(kronecker_product(left_effect,right_effect))*root_input)) == probs[labels.index(z)]
        path_probability_checks += 1

    # Exact negative control: independent leaf marginals do not reproduce the
    # joint correlated tree law.
    marginals = []
    for leaf in range(4):
        marginals.append([sum(p for z,p in zip(labels,probs) if z[leaf] == y) for y in range(2)])
    prod_probs = [sp.prod(marginals[k][z[k]] for k in range(4)) for z in labels]
    independent_tv = clean(sum(abs(p-q) for p,q in zip(probs,prod_probs))/2)
    assert independent_tv > 0

    # Seeded draws exercise the recursive polynomial-message sampler; every
    # returned effect must be precisely the enumerated effect for its label.
    sampler_rng = random.Random(args.seed ^ 0x5A17)
    sampler_counts = [0]*len(labels)
    enum_index = {z:i for i,z in enumerate(labels)}
    for _ in range(args.sampler_draws):
        z, e = recursive_sample(root_input, 2, 0, leaf_fx, b, badj, sampler_rng)
        assert clean_matrix(e) == tree[z]
        sampler_counts[enum_index[z]] += 1

    # Exact full-outcome canonical channel is kept as a control, not compiler
    # output.  Its Pauli twirl must remain a valid canonical EB map.
    exact_tree_ensemble = []
    for z, e, p in zip(labels, [tree[z] for z in labels], probs):
        exact_tree_ensemble.append((e, clean_matrix(e/sp.trace(e))))
    exact_tree_twirl = pauli_twirl(exact_tree_ensemble)
    exact_tree_ptm, _ = checked_channel(exact_tree_twirl)
    assert all(exact_tree_ptm[i,j] == 0 for i in range(1,4) for j in range(1,4) if i != j)

    # A finite adaptive MW trajectory.  The diagonal query's Gram columns are
    # positive multiples of X,Y,Z, so the exact spectral PVM frame is fixed;
    # query weights still update from the realized response losses each round.
    rng = random.Random(args.seed)
    accumulated = [Rational(0)]*3
    response_rows = []
    all_output_ensembles = []
    min_residual_eig_lower = None
    for round_id in range(T):
        q_dec = decimal_weights(accumulated, eta_mw)
        counts = sample_histogram(probs, N, rng)
        ensemble, bary, m0, c = completed_ensemble(
            [tree[z] for z in labels], probs, counts, N, alpha
        )
        # Test/check the pre-twirl rational residual-completed channel, then
        # twirl to keep every MW loss diagonal in the Pauli basis.
        pre_ptm, pre_choi = checked_channel(ensemble)
        empirical = zeros(3, 3)
        for e, count in zip([tree[z] for z in labels], counts):
            if count == 0:
                continue
            rho = clean_matrix(e/sp.trace(e))
            score_vector = [clean(sp.trace(rho*p)) for p in PAULI]
            empirical += Rational(count, N) * Matrix(score_vector) * Matrix(score_vector).T
        empirical = clean_matrix(empirical)
        residual_cov = clean_matrix(Matrix(3, 3, lambda i, j:
            D/sp.trace(m0) * (sp.trace(PAULI[i]*m0)/D) * (sp.trace(PAULI[j]*m0)/D)))
        pre_traceless = pre_ptm.extract([1,2,3],[1,2,3])
        assert pre_traceless == clean_matrix(c*empirical + residual_cov)
        assert principal_minor_psd(residual_cov)
        twirled = pauli_twirl(ensemble)
        ptm, _ = checked_channel(twirled)
        assert all(ptm[i,j] == 0 for i in range(1,4) for j in range(1,4) if i != j)
        psi_diag = [clean(ptm[i,i]) for i in range(1,4)]
        losses = [clean(j_target[i]-psi_diag[i]) for i in range(3)]
        support = decimal_score(q_dec, [clean(psi_diag[i]-j_target[i]) for i in range(3)])
        residual_det = clean(m0.det())
        if min_residual_eig_lower is None or residual_det < min_residual_eig_lower:
            min_residual_eig_lower = residual_det
        response_rows.append({
            "round": round_id+1,
            "query_diagonal_decimal": [str(x) for x in q_dec],
            "response_diagonal": [as_fraction_text(x) for x in psi_diag],
            "response_loss_diagonal": [as_fraction_text(x) for x in losses],
            "support_score_decimal": str(support),
            "barycenter_diagonal": [as_fraction_text(clean(bary[i,i])) for i in range(2)],
            "residual_effect_det": as_fraction_text(residual_det),
            "sample_outcome_support_size": sum(k>0 for k in counts),
        })
        all_output_ensembles.extend([(clean(e/T),s) for e,s in twirled])
        accumulated = [clean(accumulated[i]+losses[i]) for i in range(3)]

    final_ptm, final_choi = checked_channel(all_output_ensembles)
    avg_diag = [clean(final_ptm[i,i]) for i in range(1,4)]
    assert all(final_ptm[i,j] == 0 for i in range(1,4) for j in range(1,4) if i != j)
    slack_diag = [clean(delta-(j_target[i]-avg_diag[i])) for i in range(3)]
    slack = clean_matrix(delta*eye(3)-Matrix.diag(*j_target)+Matrix.diag(*avg_diag))
    assert slack == Matrix.diag(*slack_diag)
    assert all(v >= 0 for v in slack_diag)
    assert principal_minor_psd(slack)

    channel_record = {
        "description": "Exact finite measure-and-prepare representation of the compiled common EB map. Each record is (effect M_z, prepared density sigma_z) and Psi(X)=sum_z Tr(M_z X) sigma_z.",
        "dimension": 2,
        "outcome_count": len(all_output_ensembles),
        "effects_and_preparations_real_imag_rational": [
            {"effect": matrix_payload(e), "prepared_state": matrix_payload(s)}
            for e, s in all_output_ensembles
        ],
        "pauli_transfer_matrix": [[as_fraction_text(final_ptm[i,j]) for j in range(4)] for i in range(4)],
        "operator_order_slack_on_XYZ": [as_fraction_text(x) for x in slack_diag],
    }
    channel_file = ROOT / "FINAL_CHANNEL.json"
    channel_text = json.dumps(channel_record, indent=2) + "\n"
    channel_file.write_text(channel_text)
    # Round-trip the serialized output and redo the exact channel checks.
    loaded_channel = json.loads(channel_file.read_text())
    loaded_ensemble = [
        (matrix_from_payload(item["effect"]), matrix_from_payload(item["prepared_state"]))
        for item in loaded_channel["effects_and_preparations_real_imag_rational"]
    ]
    loaded_ptm, loaded_choi = checked_channel(loaded_ensemble)
    assert loaded_ptm == final_ptm and loaded_choi == final_choi

    # Input representation size in rational Liouville form for B.
    liouville = dense_liouville(b)
    input_bit_size = sum(exact_complex_bit_size(x) for x in liouville)
    input_record = {
        "description": "Exact dense Liouville matrix of B:M_2 -> M_4; columns correspond to E00,E01,E10,E11 and rows to output matrix entries (00,01,10,11) in row-major order.",
        "rows": liouville.rows,
        "columns": liouville.cols,
        "complex_rational_entries_real_imag": matrix_payload(liouville),
        "sum_numerator_denominator_bit_lengths": input_bit_size,
    }
    input_file = ROOT / "INPUT_BROADCASTER_LIOUVILLE.json"
    input_text = json.dumps(input_record, indent=2) + "\n"
    input_file.write_text(input_text)
    # Conservative generic proof horizons/samples for comparison.  The actual
    # replay is accepted because it has an exact final certificate, not because
    # it meets these sufficient concentration/MW horizons.
    generic_T = math.ceil(16 * (8**2) * math.log(3) / float(delta**2))
    generic_N_coefficient = 2 * float(delta**-2) * math.log(8*2*generic_T*3/0.05)
    elapsed = time.perf_counter() - start_time

    result = {
        "status": "PASS_EXACT_INSTANCE_CERTIFICATE",
        "claim_scope": "one rational d=2 dense self-compatible channel; not a theorem proof or dimension-free/sharp-2 result",
        "channel": {
            "dimension": 2,
            "marginal": "(9/10)*Z_dephasing + (1/10)*universal_1_to_2_qubit_cloner_marginal",
            "bloch_eigenvalues_XYZ": ["1/15", "1/15", "29/30"],
            "dirichlet_gaps_XYZ": [as_fraction_text(x) for x in gaps],
            "tree_depth_m": m,
            "leaves": 4,
            "logarithmic_target_J_diagonal_XYZ": [as_fraction_text(x) for x in j_target],
            "broadcaster_symmetric_kraus_weighted_sum": "9/10 * sum(K_i X K_i*) + 1/60 * sum(A_j X A_j*)",
            "input_liouville_entries": 64,
            "input_rational_liouville_bits_sum_numerators_denominators": input_bit_size,
            "broadcaster_cptp_exact": True,
            "broadcaster_swap_symmetric_exact": True,
            "both_broadcast_marginals_equal_phi_exact": True,
            "marginal_unital_tp_hs_selfadjoint_exact": True,
        },
        "tree_sampler": {
            "leaf_axes": leaf_axes,
            "gamma": as_fraction_text(gamma),
            "enumerated_outcomes_diagnostic_only": len(tree),
            "all_effects_psd_and_sum_identity_exact": True,
            "all_outcome_probabilities_at_least_full_support_bound": as_fraction_text(rare_floor),
            "all_16_recursive_conditional_path_probabilities_match_exactly": path_probability_checks == 16,
            "recursive_sampler_seeded_draws": args.sampler_draws,
            "recursive_sampler_returned_exact_enum_effect_every_draw": True,
            "independent_product_marginal_wrong_tv_exact": as_fraction_text(independent_tv),
            "independent_product_marginal_wrong_tv_decimal": str(sp.N(independent_tv, 15)),
        },
        "compiler_replay": {
            "delta": as_fraction_text(delta),
            "failure_probability_target_for_generic_theorem": "1/20",
            "rounds_T_actual": T,
            "samples_N_actual": N,
            "seed": args.seed,
            "alpha_barycenter": as_fraction_text(alpha),
            "completion_scale_c": as_fraction_text(1/(1+alpha)),
            "rational_completion_used": True,
            "completion_transfer_equals_c_times_empirical_covariance_plus_psd_residual_exact": True,
            "pre_and_post_twirled_each_channel_cp_tp_unital_hs_selfadjoint_exact": True,
            "adaptive_query_update": "Q_t proportional to exp(eta * cumulative (J - Psi_t)) in the Pauli diagonal basis",
            "eta_mw": as_fraction_text(eta_mw),
            "finite_adaptive_rounds_recorded": len(response_rows),
            "min_residual_effect_determinant": as_fraction_text(min_residual_eig_lower),
            "final_finite_channel_outcomes_before_equal-state_compression": len(all_output_ensembles),
            "final_channel_cp_tp_unital_hs_selfadjoint_exact": True,
            "final_channel_choi_psd_exact_principal_minor_check": True,
            "serialized_final_channel_roundtrip_exact_check": True,
            "final_channel_file": channel_file.name,
            "final_channel_sha256": hashlib.sha256(channel_text.encode()).hexdigest(),
            "input_channel_file": input_file.name,
            "input_channel_sha256": hashlib.sha256(input_text.encode()).hexdigest(),
            "final_comparator_pauli_diagonal_XYZ": [as_fraction_text(x) for x in avg_diag],
            "final_operator_order_slack_diagonal_XYZ": [as_fraction_text(x) for x in slack_diag],
            "final_operator_order_psd_exact": True,
            "generic_sufficient_MW_rounds_for_same_delta_eta_1_20": generic_T,
            "generic_sample_count_formula_coefficient_before_unspecified_absolute_C": generic_N_coefficient,
            "actual_run_is_short_diagnostic_not_generic_high_probability_horizon": T < generic_T,
            "full_tree_enumeration_used_only_for_small_instance_sampling_diagnostic": True,
            "runtime_seconds": elapsed,
        },
        "adaptive_rounds": response_rows,
    }
    out = ROOT / "REPLAY.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "independent_tv": result["tree_sampler"]["independent_product_marginal_wrong_tv_exact"],
        "generic_T": generic_T,
        "actual_T": T,
        "actual_N": N,
        "comparator": result["compiler_replay"]["final_comparator_pauli_diagonal_XYZ"],
        "slack": result["compiler_replay"]["final_operator_order_slack_diagonal_XYZ"],
        "runtime_seconds": elapsed,
        "report": str(out),
    }, indent=2))


if __name__ == "__main__":
    main()
