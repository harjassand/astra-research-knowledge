"""Reproducible exact and binary64 diagnostics; not laboratory observations.

Exact complex matrices are pairs of numpy object arrays of Fraction, so
neither a computer algebra package nor floating-point eigenvalues are used
for the finite positive-semidefinite certificates.
"""

import json
from fractions import Fraction as F
from pathlib import Path
import numpy as np

from physical_output_bounds import (
    LocalBudget, Envelope, compile_local, compile_uniform,
    coherent_strength_necessary, invariant_return_necessary,
    ideal_pumping_comparison, json_exact,
    rational,
)

HERE = Path(__file__).resolve().parent


def mat(real, imag=None):
    real = np.array(real, dtype=object)
    real = np.array([[rational(x) for x in row] for row in real], dtype=object)
    if imag is None:
        imag = np.full(real.shape, F(0), dtype=object)
    else:
        imag = np.array([[rational(x) for x in row] for row in imag], dtype=object)
    return real, imag


def zero(n):
    return mat([[0] * n for _ in range(n)])


def identity(n):
    return mat([[int(i == j) for j in range(n)] for i in range(n)])


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def neg(a):
    return -a[0], -a[1]


def sub(a, b):
    return add(a, neg(b))


def scale(c, a):
    return F(c) * a[0], F(c) * a[1]


def times_i(a):
    return -a[1], a[0]


def adj(a):
    return a[0].T, -a[1].T


def mul(a, b):
    return a[0] @ b[0] - a[1] @ b[1], a[0] @ b[1] + a[1] @ b[0]


def chain(*args):
    result = args[0]
    for a in args[1:]:
        result = mul(result, a)
    return result


def tensor(*args):
    result = mat([[1]])
    for a in args:
        result = (np.kron(result[0], a[0]) - np.kron(result[1], a[1]),
                  np.kron(result[0], a[1]) + np.kron(result[1], a[0]))
    return result


def iszero(a):
    return all(x == 0 for x in a[0].flat) and all(x == 0 for x in a[1].flat)


def equal(a, b):
    return iszero(sub(a, b))


def trace_real(a):
    re, im = sum(np.diag(a[0])), sum(np.diag(a[1]))
    assert im == 0
    return re


def numeric(a):
    return np.asarray(a[0], dtype=float) + 1j * np.asarray(a[1], dtype=float)


def exact_psd_ldl(a):
    """Unpivoted Hermitian LDL certificate, including exact zero-pivot rule."""
    assert equal(a, adj(a))
    re, im = a[0].copy(), a[1].copy()
    n = re.shape[0]
    pivots = []
    for k in range(n):
        assert im[k, k] == 0
        p = re[k, k]
        if p < 0:
            raise AssertionError(("negative exact LDL pivot", k, p))
        pivots.append(p)
        if p == 0:
            assert all(re[j, k] == im[j, k] == 0 for j in range(k + 1, n))
            continue
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                re[i, j] -= (re[i, k] * re[j, k] + im[i, k] * im[j, k]) / p
                im[i, j] -= (im[i, k] * re[j, k] - re[i, k] * im[j, k]) / p
    return {"dimension": n, "positive_pivots": sum(p > 0 for p in pivots),
            "zero_pivots": sum(p == 0 for p in pivots), "pivots": pivots}


I = identity(2)
X = mat([[0, 1], [1, 0]])
Y = mat([[0, 0], [0, 0]], [[0, -1], [1, 0]])
Z = mat([[1, 0], [0, -1]])
P0 = mat([[1, 0], [0, 0]])
LOWER = mat([[0, 1], [0, 0]])


def local(total, replacements):
    return tensor(*(replacements.get(i, I) for i in range(total)))


def dissipator_adjoint(jump, observable):
    k = mul(adj(jump), jump)
    return sub(chain(adj(jump), observable, jump),
               scale(F(1, 2), add(mul(k, observable), mul(observable, k))))


def generator_adjoint(h, jumps, observable):
    result = times_i(sub(mul(h, observable), mul(observable, h)))
    for jump in jumps:
        result = add(result, dissipator_adjoint(jump, observable))
    return result


def generator_forward(h, jumps, state):
    result = neg(times_i(sub(mul(h, state), mul(state, h))))
    for jump in jumps:
        k = mul(adj(jump), jump)
        result = add(result, sub(chain(jump, state, adj(jump)),
                                 scale(F(1, 2), add(mul(k, state), mul(state, k)))))
    return result


def write(name, value):
    (HERE / name).write_text(json.dumps(json_exact(value), indent=2) + "\n")


def finite_operator_audit():
    n, aux, total = 3, 1, 4
    p = tensor(P0, P0, P0, I)
    q = sub(identity(1 << total), p)
    terms_h = [
        (scale(F(3, 7), local(total, {0: X, 3: Z})), (0,), F(3, 7)),
        (scale(F(2, 5), local(total, {1: Y, 2: X, 3: X})), (1, 2), F(2, 5)),
        (scale(F(1, 3), local(total, {0: Z, 2: Z, 3: Y})), (0, 2), F(1, 3)),
    ]
    terms_l = [
        (scale(F(1, 2), local(total, {0: LOWER, 3: X})), (0,), F(1, 4)),
        (scale(F(1, 3), local(total, {0: scale(F(1, 2), add(I, X)), 3: X})), (0,), F(1, 9)),
        (scale(F(1, 7), add(local(total, {1: X, 3: LOWER}),
                            times_i(local(total, {1: Z, 2: X, 3: LOWER})))), (1, 2), F(4, 49)),
        (scale(F(1, 4), local(total, {2: X, 3: add(I, times_i(Y))})), (2,), F(1, 4)),
    ]
    h = zero(1 << total)
    budgets = []
    for term, support, norm in terms_h:
        h = add(h, term)
        budgets.append(LocalBudget.from_hamiltonian_and_jumps(support, norm, 0))
        exact_psd_ldl(sub(scale(norm * norm, identity(1 << total)), mul(adj(term), term)))
    for term, support, norm2 in terms_l:
        budgets.append(LocalBudget.from_hamiltonian_and_jumps(support, 0, norm2))
        exact_psd_ldl(sub(scale(norm2, identity(1 << total)), mul(adj(term), term)))
    # Huge auxiliary-only activity must have exactly zero physical-target action.
    auxiliary_h = scale(10**6, local(total, {3: X}))
    auxiliary_l = scale(10**3, local(total, {3: LOWER}))
    auxiliary_action = generator_adjoint(auxiliary_h, [auxiliary_l], p)
    assert iszero(auxiliary_action)
    c = generator_adjoint(h, [a[0] for a in terms_l], p)
    b = chain(p, c, q)
    b_formula = neg(times_i(chain(p, h, q)))
    for jump, _, _ in terms_l:
        b_formula = add(b_formula,
                        scale(F(1, 2), chain(p, adj(jump), sub(p, q), jump, q)))
    assert equal(b, b_formula)
    env, resource = compile_local(n, [1] * n, budgets)
    r = max(resource["return_incidence"])
    certificates = {
        "negative_PP": exact_psd_ldl(neg(chain(p, c, p))),
        "QQ_return_bound": exact_psd_ldl(sub(scale(r, q), chain(q, c, q))),
        "PQ_norm_bound": exact_psd_ldl(sub(scale(env.offdiag_squared, q), mul(adj(b), b))),
    }
    # Check support projectors and the global support-incidence identity.
    cover = zero(1 << total)
    for budget in budgets:
        e = sub(tensor(*(I if i in budget.support else P0 for i in range(n)), I), p)
        cover = add(cover, scale(budget.return_bound, e))
    certificates["incidence_cover"] = exact_psd_ldl(sub(scale(r, q), cover))
    action = add(c, generator_adjoint(zero(1 << total),
                                    [local(total, {i: X}) for i in range(n)], p))
    rng = np.random.default_rng(20261107)
    states = []
    for _ in range(12):
        v = mat(rng.integers(-2, 3, size=(1 << total, 1)),
                rng.integers(-2, 3, size=(1 << total, 1)))
        rho = mul(v, adj(v))
        rho = scale(1 / trace_real(rho), rho)
        f = trace_real(mul(p, rho))
        derivative = trace_real(mul(action, rho))
        base = -env.leakage * f + env.return_rate * (1 - f)
        excess = derivative - base
        assert excess <= 0 or excess * excess <= 4 * env.offdiag_squared * f * (1 - f)
        states.append({"fidelity": f, "actual_derivative": derivative,
                       "envelope_upper": env.drift_interval(f)[1]})
    write("EXACT_AUXILIARY_OPERATOR_AUDIT.json", {
        "work_qubits": n, "auxiliary_dimension": 2**aux,
        "arithmetic": "Gaussian rational via pairs of Fraction matrices",
        "all_supplied_norm_bounds_certified": True,
        "auxiliary_only_action_exactly_zero": True,
        "off_diagonal_block_identity_exact": True,
        "resource": resource, "certificates": certificates,
        "arbitrary_correlated_states": states,
    })


def instantaneous_sharpness():
    n, j, kappa = 4, F(2), F(9)
    p = tensor(*([P0] * n))
    h = zero(1 << n)
    jumps = []
    budgets = []
    for i in range(n):
        h = add(h, scale(j, local(n, {i: X})))
        jumps.extend([local(n, {i: X}), scale(3, local(n, {i: LOWER}))])
        # Actual off-diagonal action of an absorbing lowering pump is zero.
        budgets.append(LocalBudget((i,), kappa, j))
    env, _ = compile_local(n, [1] * n, budgets)
    a = generator_adjoint(h, jumps, p)
    rows = []
    for aa, bb, cc in [(3, 4, 5), (20, 21, 29), (99, 20, 101)]:
        real = [[F(0)] for _ in range(1 << n)]
        imag = [[F(0)] for _ in range(1 << n)]
        real[0][0] = F(aa, cc)
        for i in range(n):
            imag[1 << i][0] = F(bb, 2 * cc)
        v = mat(real, imag)
        rho = mul(v, adj(v))
        assert trace_real(rho) == 1
        f = F(aa * aa, cc * cc)
        actual = trace_real(mul(a, rho))
        expected = -n * f + (1 + kappa) * (1 - f) + 2 * j * 2 * F(aa * bb, cc * cc)
        assert actual == expected
        rows.append({"fidelity": f, "actual_derivative": actual,
                     "theorem_derivative": expected, "exact_equality": True})
    write("EXACT_INSTANTANEOUS_SHARPNESS.json", {
        "N": n, "Hamiltonian_per_site": j, "absorbing_pump_rate": kappa,
        "scope": "Pointwise fidelity drift; not stationary attainability of the envelope",
        "rows": rows,
    })


def graph_audit():
    n = 4
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    h_unscaled = mat([[1, 1], [1, -1]])
    h_all = scale(F(1, 4), tensor(*([h_unscaled] * n)))
    signs = []
    for x in range(1 << n):
        parity = sum(((x >> (n - 1 - i)) & 1) * ((x >> (n - 1 - j)) & 1)
                     for i, j in edges) % 2
        signs.append((-1)**parity)
    cz = mat([[signs[i] if i == j else 0 for j in range(1 << n)] for i in range(1 << n)])
    u = mul(cz, h_all)
    assert equal(mul(adj(u), u), identity(1 << n))
    p = tensor(*([P0] * n))
    pg = chain(u, p, adj(u))
    physical_noise = [local(n, {i: Z}) for i in range(n)]
    pumps = []
    for i in range(n):
        assert equal(chain(adj(u), physical_noise[i], u), local(n, {i: X}))
        neighbors = {j if i == k else k for k, j in edges if i in (k, j)}
        stabilizer = local(n, {i: X, **{j: Z for j in neighbors}})
        pump = chain(physical_noise[i], scale(F(1, 2), sub(identity(1 << n), stabilizer)))
        assert equal(pump, chain(u, local(n, {i: LOWER}), adj(u)))
        assert iszero(mul(pump, pg))
        pumps.append(scale(3, pump))
    sigma = chain(u, tensor(*([mat([[F(10, 11), 0], [0, F(1, 11)]])] * n)), adj(u))
    assert iszero(generator_forward(zero(1 << n), physical_noise + pumps, sigma))
    fidelity = trace_real(mul(pg, sigma))
    assert fidelity == F(10, 11)**n
    action = generator_adjoint(zero(1 << n), pumps, pg)
    qg = sub(identity(1 << n), pg)
    assert iszero(chain(pg, action, pg)) and iszero(chain(pg, action, qg))
    # A physical one-site control has target-frame support in its closed neighborhood.
    transformed = chain(adj(u), local(n, {0: X}), u)
    assert iszero(sub(mul(transformed, local(n, {2: X})), mul(local(n, {2: X}), transformed)))
    assert iszero(sub(mul(transformed, local(n, {2: Z})), mul(local(n, {2: Z}), transformed)))
    env, resources = compile_local(n, [1] * n,
                                  [LocalBudget((i,), 1, 1) for i in range(n)], edges)
    assert resources["total_offdiag"] == n
    assert max(resources["offdiag_incidence"]) == 3
    assert env.offdiag_squared == 3 * n
    write("EXACT_GRAPH_AND_PUMPING_AUDIT.json", {
        "N": n, "edges": edges,
        "physical_Z_to_virtual_X_exact": True,
        "native_graph_pump_formula_exact": True,
        "stationarity_exact": True,
        "whole_state_fidelity": fidelity,
        "absorbing_upper": F(10, n + 10),
        "target_invariance_PP_and_PQ_exact": True,
        "support_map": resources,
        "scope": "Finite rational diagnostic; ideal native pumps are a comparator assumption",
    })


def finite_certificates():
    rows = []
    for degree in (0, 4):
        for n in (100, 10000, 1000000):
            env = compile_uniform(n, 1, 10, 15, degree)
            c, gamma, linear_floor = env.linear_parameters()
            rows.append({
                "N": n, "maximum_graph_degree": degree,
                "noise_rate": F(1), "return_incidence_bound": F(10),
                "offdiag_incidence_bound": F(15),
                "ceiling_interval": env.root_interval(),
                "exclusion_99_percent": env.exclusion_certificate(F(99, 100)),
                "high_fidelity_interval_length_upper": env.dwell_upper(F(99, 100)),
                "linear_comparison": {"C": c, "gamma": gamma, "floor": linear_floor},
                "delay": F(1, 10000),
                "delivery_fidelity_upper": env.delivery_upper(F(1, 10000)),
                "accepted_probability_upper_at_99_percent": env.accepted_probability_upper(F(1, 10000), F(99, 100)),
            })
    write("FINITE_RESOURCE_CERTIFICATES.json", {
        "status": "Declared mathematical rates; no device calibration or physical trials",
        "arithmetic": "Exact rationals; root brackets by exact sign; exponential upper from positive Taylor sum",
        "rows": rows,
        "necessary_common_generator_bound_N1e6_error_1percent": coherent_strength_necessary(1000000, 1, F(1, 100)),
        "necessary_absorbing_return_N1e6_error_1percent": invariant_return_necessary(1000000, 1, F(1, 100)),
        "ideal_native_pump_comparator": ideal_pumping_comparison(1000000, 1, F(1, 100), 1, 4),
    })
    # Every nonempty error set has cover weight at most the largest singleton incidence.
    n = 8
    supports = [(0, 1), (1, 2, 3), (3, 4), (0, 5, 7), (5, 6), (6, 7)]
    weights = [F(i + 1, 7) for i in range(len(supports))]
    incidence = [sum(w for s, w in zip(supports, weights) if i in s) for i in range(n)]
    error_cover = []
    for mask in range(1, 1 << n):
        error = {i for i in range(n) if mask & (1 << i)}
        value = sum(w for s, w in zip(supports, weights) if error <= set(s))
        assert value <= max(incidence)
        error_cover.append(value)
    assert max(error_cover) == max(incidence)
    write("EXACT_SUPPORT_COVER_AUDIT.json", {
        "N": n, "supports": supports, "weights": weights,
        "incidence": incidence, "nonempty_error_sets_checked": len(error_cover),
        "maximum_cover_weight": max(error_cover), "exact_incidence_norm_identity": True,
    })
    # An application to the previously DECLARED native interval model, not
    # a new acquisition or a claim that synthetic calibration measured it.
    native_n = 1000000
    native = Envelope(F(9, 10) * native_n, F(67, 10), 0)
    native_root = F(67, 9 * native_n + 67)
    assert native.drift_sign(native_root) == 0
    write("ACCEPTED_NATIVE_REGIME_BOUND.json", {
        "status": "Conditional on the already declared, stable matched native law",
        "N": native_n, "lambda_lower": F(9, 10), "lambda_upper": F(11, 10),
        "actuator_rate_cap": F(5), "actuator_flip_fraction_upper": F(3, 25),
        "maximum_return_rate_per_site": F(28, 5),
        "offdiagonal_target_coupling": F(0),
        "ceiling_exact": native_root,
        "dwell_99_percent_upper": native.dwell_upper(F(99, 100)),
        "delivery_delay": F(1, 10000),
        "delivery_upper": native.delivery_upper(F(1, 10000)),
        "scope": "Arbitrary time-dependent/adaptive choices within this additive native menu; unconditional output. Additional physical controllers require their own budgets.",
    })


def dynamics_audit():
    from scipy.integrate import solve_ivp
    n, total = 3, 4
    d = 1 << total
    p = numeric(tensor(P0, P0, P0, I))
    h_terms = [(.3, {0: X, 3: Z}, (0,)), (.2, {1: Y, 2: X, 3: X}, (1, 2))]
    h = sum(c * numeric(local(total, op)) for c, op, _ in h_terms)
    h += .7 * numeric(local(total, {3: X}))
    jumps = [numeric(local(total, {i: X})) for i in range(n)]
    jumps += [np.sqrt(.8) * numeric(local(total, {i: LOWER})) for i in range(n)]
    jumps += [np.sqrt(.4) * numeric(local(total, {3: LOWER}))]
    budgets = [LocalBudget(s, 0, F(str(c))) for c, _, s in h_terms]
    budgets += [LocalBudget((i,), F(4, 5), 0) for i in range(n)]
    env, _ = compile_local(n, [1] * n, budgets)
    js = [(l, l.conj().T, l.conj().T @ l) for l in jumps]

    def rhs(_, flat):
        rho = flat.reshape(d, d)
        out = -1j * (h @ rho - rho @ h)
        for l, ld, k in js:
            out += l @ rho @ ld - (k @ rho + rho @ k) / 2
        return out.reshape(-1)

    rng = np.random.default_rng(1072026)
    inputs = []
    v = np.zeros(d, dtype=complex)
    v[0], v[1] = 1 / np.sqrt(2), 1j / np.sqrt(2)
    inputs.append(("perfect_work_arbitrary_auxiliary", np.outer(v, v.conj())))
    v = rng.normal(size=d) + 1j * rng.normal(size=d)
    v /= np.linalg.norm(v)
    inputs.append(("correlated_work_auxiliary", np.outer(v, v.conj())))
    times = np.linspace(0, 5, 201)
    records = []
    _, gamma, floor = env.linear_parameters()
    b = np.sqrt(float(env.offdiag_squared))
    for label, rho0 in inputs:
        sol = solve_ivp(rhs, (0, 5), rho0.reshape(-1), method="DOP853",
                        t_eval=times, atol=1e-11, rtol=1e-10)
        assert sol.success
        fidelities, drifts, ceilings = [], [], []
        min_eig, max_trace_error, max_drift_excess = 1., 0., -1e300
        for t, flat in zip(sol.t, sol.y.T):
            rho = flat.reshape(d, d)
            f = float(np.trace(p @ rho).real)
            df = float(np.trace(p @ rhs(t, flat).reshape(d, d)).real)
            drift = -float(env.leakage) * f + float(env.return_rate) * (1 - f) + 2 * b * np.sqrt(max(0., f * (1 - f)))
            bound = float(floor) + (1 - float(floor)) * np.exp(-float(gamma) * t)
            assert df <= drift + 1e-8 and f <= bound + 1e-8
            min_eig = min(min_eig, float(np.linalg.eigvalsh((rho + rho.conj().T) / 2).min()))
            max_trace_error = max(max_trace_error, abs(np.trace(rho) - 1))
            max_drift_excess = max(max_drift_excess, df - drift)
            fidelities.append(f); drifts.append(df); ceilings.append(bound)
        records.append({"input": label, "times": sol.t.tolist(),
                        "fidelities": fidelities, "actual_drifts": drifts,
                        "linear_upper": ceilings, "minimum_state_eigenvalue": min_eig,
                        "maximum_trace_error": max_trace_error,
                        "maximum_drift_excess": max_drift_excess,
                        "solver_function_evaluations": sol.nfev})
    write("FINITE_DYNAMICS_DIAGNOSTIC.json", {
        "arithmetic": "binary64; tolerance diagnostics, not the all-size proof or a diamond-norm certification",
        "seed": 1072026, "work_qubits": n, "auxiliary_qubits": 1,
        "records": records,
    })


def main():
    finite_operator_audit()
    instantaneous_sharpness()
    graph_audit()
    finite_certificates()
    dynamics_audit()
    outputs = sorted(p.name for p in HERE.glob("*.json") if p.name != "RUN_SUMMARY.json")
    write("RUN_SUMMARY.json", {
        "all_assertions_passed": True,
        "exact_operator_and_incidence_certificates": True,
        "instantaneous_envelope_saturation": True,
        "graph_noise_and_pump_identities": True,
        "finite_dynamics_diagnostic": True,
        "physical_experiment": False,
        "formal_kernel_verification": False,
        "outputs": outputs,
    })
    print(json.dumps({"status": "all audits passed", "outputs": outputs}, indent=2))


if __name__ == "__main__":
    main()
