#!/usr/bin/env python3
"""Exact, solver-free replay of the independent KMS FOUR counterexample.

No floating-point arithmetic is used to establish any assertion. SymPy is
needed only for finite algebra. Integral/Taylor bounds are proved in the
frozen text; this replay verifies their constants and the final strict sign.
"""
import json
import sympy as sp


Q = sp.Rational
I2 = sp.eye(2)
checks = []


def equal(actual, expected, label):
    delta = actual - expected
    if isinstance(delta, sp.MatrixBase):
        ok = all(sp.simplify(x) == 0 for x in delta)
    else:
        ok = sp.simplify(delta) == 0
    if not ok:
        raise AssertionError(f"{label}: {delta}")
    checks.append(label)


def positive_rational(value, label):
    value = sp.factor(value)
    if not value.is_Rational or not value > 0:
        raise AssertionError(f"{label}: {value}")
    checks.append(label)


def adjoint(a):
    return a.conjugate().T


def hs(a, b):
    return sp.simplify(sp.trace(adjoint(a) * b))


def partial_trace(a, dims, traced):
    """Exact matrix partial trace, retaining tensor factors in given order."""
    from itertools import product
    kept = [k for k in range(len(dims)) if k not in traced]
    retained = list(product(*(range(dims[k]) for k in kept)))
    deleted = list(product(*(range(dims[k]) for k in traced)))

    def index(coords):
        index_value = 0
        for dim, coordinate in zip(dims, coords):
            index_value = dim * index_value + coordinate
        return index_value

    out = sp.zeros(len(retained))
    for row, rcoords in enumerate(retained):
        for col, ccoords in enumerate(retained):
            value = 0
            for tcoords in deleted:
                rr, cc = [0] * len(dims), [0] * len(dims)
                for k, r, c in zip(kept, rcoords, ccoords):
                    rr[k], cc[k] = r, c
                for k, t in zip(traced, tcoords):
                    rr[k] = cc[k] = t
                value += a[index(rr), index(cc)]
            out[row, col] = sp.simplify(value)
    return out


sigma = sp.diag(Q(4, 5), Q(1, 5))
sqrt_sigma = sp.diag(2, 1) / sp.sqrt(5)
inv_sqrt_sigma = sp.diag(Q(1, 2), 1) * sp.sqrt(5)
S = sp.diag(sp.sqrt(2), 1) / 5 ** Q(1, 4)
Sinv = S.inv()
vectors = [sp.Matrix([1, 0]), sp.Matrix([Q(3, 5), Q(4, 5)]),
           sp.Matrix([Q(4, 5), -Q(3, 5)])]
probabilities = [Q(3, 5), Q(1, 5), Q(1, 5)]
projectors = [v * adjoint(v) for v in vectors]
effects = [p * inv_sqrt_sigma * pi * inv_sqrt_sigma
           for p, pi in zip(probabilities, projectors)]
expected_effects = [sp.diag(Q(3, 4), 0),
                    sp.Matrix([[Q(9, 100), Q(6, 25)], [Q(6, 25), Q(16, 25)]]),
                    sp.Matrix([[Q(4, 25), -Q(6, 25)], [-Q(6, 25), Q(9, 25)]])]
for z, (v, pi, effect, expected) in enumerate(zip(vectors, projectors, effects,
                                                 expected_effects)):
    equal(hs(v, v), 1, f"pure vector {z} normalized")
    equal(pi * pi, pi, f"projector {z} rank-one identity")
    equal(effect, expected, f"effect {z} rational identity")
    equal(effect.det(), 0, f"effect {z} determinant zero")
    positive_rational(sp.trace(effect), f"effect {z} positive nonzero eigenvalue")
equal(sum(effects, sp.zeros(2)), I2, "POVM normalization")
equal(sum((p * pi for p, pi in zip(probabilities, projectors)), sp.zeros(2)),
      sigma, "ensemble barycenter")


def phi(a):
    return sp.simplify(sum((pi * sp.trace(m * a)
                           for pi, m in zip(projectors, effects)), sp.zeros(2)))


def H(a):
    return sp.simplify(sum((m * sp.trace(pi * a)
                           for pi, m in zip(projectors, effects)), sp.zeros(2)))


def broadcaster(a):
    return sum((sp.kronecker_product(pi, pi) * sp.trace(m * a)
                for pi, m in zip(projectors, effects)), sp.zeros(4))


def T(a):
    return sp.simplify(Sinv * phi(S * a * S) * Sinv)


def D(a):
    return sp.simplify(a - T(a))


kraus = [sp.sqrt(p) * v * adjoint(inv_sqrt_sigma * v)
         for p, v in zip(probabilities, vectors)]
broadcast_kraus = [sp.sqrt(p) * sp.kronecker_product(v, v)
                   * adjoint(inv_sqrt_sigma * v)
                   for p, v in zip(probabilities, vectors)]
equal(sum((adjoint(k) * k for k in kraus), sp.zeros(2)), I2,
      "channel Kraus completeness")
equal(sum((adjoint(k) * k for k in broadcast_kraus), sp.zeros(2)), I2,
      "broadcaster Kraus completeness")
equal(phi(sigma), sigma, "stationarity")
equal(H(I2), I2, "adjoint unitality")
units = []
for i in range(2):
    for j in range(2):
        e = sp.zeros(2)
        e[i, j] = 1
        units.append(e)
for k, e in enumerate(units):
    equal(phi(e), sum((a * e * adjoint(a) for a in kraus), sp.zeros(2)),
          f"full-domain channel Kraus identity {k}")
    equal(broadcaster(e), sum((a * e * adjoint(a) for a in broadcast_kraus),
                             sp.zeros(4)), f"full-domain broadcast Kraus identity {k}")
    equal(partial_trace(broadcaster(e), [2, 2], [1]), phi(e),
          f"first full channel marginal {k}")
    equal(partial_trace(broadcaster(e), [2, 2], [0]), phi(e),
          f"second full channel marginal {k}")
    equal(sqrt_sigma * H(e) * sqrt_sigma,
          phi(sqrt_sigma * e * sqrt_sigma), f"KMS adjoint intertwining {k}")
choi = sum((sp.kronecker_product(m.T, pi)
            for m, pi in zip(effects, projectors)), sp.zeros(4))
choi_broadcast = sum((sp.kronecker_product(m.T, pi, pi)
                      for m, pi in zip(effects, projectors)), sp.zeros(8))
# Both Choi matrices are sums of positive tensor factors; no numerical PSD test.
equal(partial_trace(choi, [2, 2], [1]), I2, "Choi trace preservation")
equal(partial_trace(choi_broadcast, [2, 2, 2], [1, 2]), I2,
      "broadcast Choi trace preservation")
equal(partial_trace(choi_broadcast, [2, 2, 2], [2]), choi,
      "first broadcast Choi marginal")
equal(partial_trace(choi_broadcast, [2, 2, 2], [1]), choi,
      "second broadcast Choi marginal")

X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.diag(1, -1)
basis = [sqrt_sigma, X / sp.sqrt(2), Y / sp.sqrt(2),
         sp.diag(1, -2) / sp.sqrt(5)]
equal(sp.Matrix([[hs(a, b) for b in basis] for a in basis]), sp.eye(4),
      "weighted transformed basis HS-orthonormal")
T_matrix = sp.Matrix([[hs(a, T(b)) for b in basis] for a in basis])
expected_T = sp.Matrix([[1, 0, 0, 0],
                        [0, Q(288, 625), 0, -42 * sp.sqrt(5) / 625],
                        [0, 0, 0, 0],
                        [0, -42 * sp.sqrt(5) / 625, 0, Q(53, 125)]])
equal(T_matrix, expected_T, "exact HS-transformed channel matrix")
equal(T_matrix, T_matrix.T, "HS self-adjointness")
block = T_matrix.extract([1, 3], [1, 3])
equal(block.det(), Q(108, 625), "centered block determinant")
equal(sp.trace(block), Q(553, 625), "centered block trace")
positive_rational(block[0, 0], "centered block positive diagonal")
positive_rational(block.det(), "centered block positive determinant")
positive_rational(1 - sp.trace(block), "centered positive eigenvalues below one")
equal(D(sqrt_sigma), sp.zeros(2), "reference fixed by transformed channel")
if T_matrix[1, 3] == 0:
    raise AssertionError("commutant/coherence coupling absent")
checks.append("commutant/coherence coupling strictly nonzero")

A = Q(2, 5) * Z - Q(1, 15) * X
C = Sinv * A * Sinv
equal(sp.trace(A), 0, "state direction trace zero")
equal(A * A, Q(37, 225) * I2, "state direction norm squared")
positive_rational(Q(1, 4) - Q(37, 225), "state direction norm below one half")
equal(sp.Matrix([hs(u, C) for u in basis]),
      sp.Matrix([0, -sp.sqrt(5) / 15, 0, 1]), "state direction HS coordinates")
delta = A - phi(A)
equal(delta, sp.Matrix([[Q(692, 3125), Q(293, 9375)],
                       [Q(293, 9375), -Q(692, 3125)]]), "exact channel defect")
log_derivative = sp.Matrix([[Q(1, 2), -2 * sp.log(2) / 9],
                            [-2 * sp.log(2) / 9, -2]])
root_derivative = sp.Matrix([[sp.sqrt(5) / 10, -sp.sqrt(5) / 45],
                             [-sp.sqrt(5) / 45, -sp.sqrt(5) / 5]])
for i in range(2):
    for j in range(2):
        si, sj = sigma[i, i], sigma[j, j]
        log_factor = (1 / si if i == j else (sp.log(si) - sp.log(sj)) / (si - sj))
        root_factor = 1 / (sp.sqrt(si) + sp.sqrt(sj))
        equal(log_derivative[i, j], A[i, j] * log_factor,
              f"log derivative divided difference {i}{j}")
        equal(root_derivative[i, j], A[i, j] * root_factor,
              f"sqrt derivative divided difference {i}{j}")
J2 = sp.simplify(sp.trace(delta * log_derivative))
E2 = hs(root_derivative, D(root_derivative))
equal(J2, Q(346, 625) - Q(1172, 84375) * sp.log(2), "exact J Hessian")
equal(E2, Q(37124, 253125) - Q(14, 1875) * sp.sqrt(2), "exact E Hessian")
q = sp.simplify(J2 - 4 * E2)
equal(q, -Q(8366, 253125) - Q(1172, 84375) * sp.log(2)
      + Q(56, 1875) * sp.sqrt(2), "exact FOUR Hessian gap")
log_lower = Q(34657, 50000)
root_upper = Q(70711, 50000)
five_terms = sum((Q(2, (2 * k + 1) * 3 ** (2 * k + 1)) for k in range(5)), Q(0))
positive_rational(five_terms - log_lower, "five log series terms exceed rational lower bound")
positive_rational(root_upper ** 2 - 2, "rational sqrt upper bound")
q_upper = -Q(8366, 253125) - Q(1172, 84375) * log_lower + Q(56, 1875) * root_upper
equal(q_upper, -Q(1394713, 3164062500), "strict rational Hessian bound")
positive_rational(-Q(1, 2500) - q_upper, "strict Hessian bound below minus one over 2500")

epsilon = Q(1, 10 ** 6)
rho = sigma + epsilon * A
equal(rho, sp.Matrix([[Q(2000001, 2500000), -Q(1, 15000000)],
                     [-Q(1, 15000000), Q(499999, 2500000)]]), "actual rational state")
equal(sp.trace(rho), 1, "actual state trace one")
positive_rational(rho[0, 0], "actual state positive diagonal")
positive_rational(rho.det(), "actual state positive determinant")
m, t_max = Q(1, 10), Q(1, 5)
equal(sigma[1, 1] - t_max * Q(1, 2), m, "uniform path eigenvalue lower bound")
equal(Q(1, 4) / (2 * m ** 2), Q(25, 2), "log Taylor remainder coefficient")
positive_rational(1 - Q(250, 256), "sqrt Taylor coefficient 5sqrt10 over16 below one")
positive_rational(1 - hs(root_derivative, root_derivative), "sqrt derivative HS norm below one")
positive_rational(5 - (4 + 4 * t_max), "energy Taylor bound at path endpoint")
positive_rational(t_max - epsilon, "certified state within path")
equal(25 + 4 * 5, 45, "combined analytic remainder coefficient")
gap_upper = epsilon ** 2 * (-Q(1, 2500) + 45 * epsilon)
equal(gap_upper, -Q(71, 200000) * epsilon ** 2, "actual scalar gap strictly negative")
positive_rational(-gap_upper, "strict rational FOUR exclusion")

print(json.dumps({
    "status": "PASS_EXACT",
    "checks": len(checks),
    "all_assertions": checks,
    "dimension": 2,
    "ensemble_atoms": 3,
    "broadcaster_choi_dimension": 8,
    "rho_epsilon": str(epsilon),
    "certified_J_minus_4E_upper_bound": str(gap_upper),
    "universal_two_status": "UNKNOWN",
    "external_formal_validation": "UNKNOWN",
    "floating_point_used_for_certificate": False,
    "scope": "Finite algebra and analytic bound constants replay; integral derivations are in the frozen proof"
}, indent=2))
