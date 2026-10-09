#!/usr/bin/env python3
"""Finite exact orientation controls for the frozen analytic classification.

One modular channel/noncommuting state, one complex Choi control, and the
already frozen counterexample with a tuned ancilla. Not a theorem prover.
"""
import json
import sympy as s

Q = s.Rational
checks = []


def adj(a):
    return a.conjugate().T


def equal(a, b, label):
    delta = a - b
    ok = (all(s.simplify(x) == 0 for x in delta) if isinstance(delta, s.MatrixBase)
          else s.simplify(delta) == 0)
    assert ok, (label, delta)
    checks.append(label)


def vec(a):
    return s.Matrix([a[0, 0], a[1, 0], a[0, 1], a[1, 1]])


def absolute_square(a):
    return s.simplify(s.conjugate(a) * a)


ident = s.eye(2)
swap = s.Matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
E01 = s.Matrix([[0, 1], [0, 0]])
E10 = E01.T
complex_hermitian = s.Matrix([[1, s.I], [-s.I, 2]])
equal(adjoint_control := swap * vec(complex_hermitian).conjugate(),
      vec(adj(complex_hermitian)), "Choi antiunitary implements Kraus adjoint")
equal(adjoint_control, vec(complex_hermitian), "complex Hermitian zero-frequency Choi vector fixed")
choi_complex = vec(complex_hermitian) * adj(vec(complex_hermitian))
equal(swap * choi_complex.conjugate() * swap, choi_complex,
      "complex CP HS-self-adjoint Choi invariant under swap plus conjugation")
assert swap * choi_complex * swap != choi_complex
checks.append("swap without conjugation rejected by complex Choi control")

sigma = s.diag(Q(1, 5), Q(4, 5))
sqrt_sigma = s.diag(1, 2) / s.sqrt(5)
S = s.diag(1, s.sqrt(2)) / 5 ** Q(1, 4)
V = [s.I * E01 / 2, -s.I * E10 / 2,
     s.diag(1 / s.sqrt(2), s.sqrt(14) / 4)]
weights = [Q(1, 2), Q(2), Q(1)]  # exp(omega/2)
K = [s.sqrt(w) * v for w, v in zip(weights, V)]
for index, (v, k, weight) in enumerate(zip(V, K, weights)):
    equal(S * v * S.inv(), k, f"physical Kraus frequency sign {index}")
    equal(sigma * v * sigma.inv(), weight ** 2 * v,
          f"modular eigenvalue {index}")
equal(V[1], adj(V[0]), "nonzero frequency Kraus adjoint pair")
equal(V[2], adj(V[2]), "zero frequency Kraus Hermitian")
equal(sum((adj(k) * k for k in K), s.zeros(2)), ident, "physical Kraus TP completeness")


def phi(a):
    return s.simplify(sum((k * a * adj(k) for k in K), s.zeros(2)))


def T(a):
    return s.simplify(sum((v * a * adj(v) for v in V), s.zeros(2)))


def H(a):
    return s.simplify(sum((adj(k) * a * k for k in K), s.zeros(2)))


equal(phi(sigma), sigma, "modular control stationary")
for i in range(2):
    for j in range(2):
        unit = s.zeros(2)
        unit[i, j] = 1
        equal(S.inv() * phi(S * unit * S) * S.inv(), T(unit),
              f"weighted transform orientation {i}{j}")
        equal(sqrt_sigma * H(unit) * sqrt_sigma,
              phi(sqrt_sigma * unit * sqrt_sigma), f"KMS symmetry {i}{j}")
choi_T = sum((vec(v) * adj(vec(v)) for v in V), s.zeros(4))
equal(swap * choi_T.conjugate() * swap, choi_T, "paired Choi invariant")
log_sigma = s.diag(s.log(Q(1, 5)), s.log(Q(4, 5)))
frequencies = [s.log(Q(1, 4)), s.log(Q(4)), 0]
expected_log_image = log_sigma + sum((omega * weight * adj(v) * v
                                     for omega, weight, v in zip(frequencies, weights, V)),
                                    s.zeros(2))
equal(H(log_sigma), expected_log_image, "H log sigma frequency sign")

unitary = s.Matrix([[3, 4 * s.I], [4 * s.I, 3]]) / 5
equal(adj(unitary) * unitary, ident, "complex state eigenbasis unitary")
eigenvalues = [Q(1, 3), Q(2, 3)]
rho = unitary * s.diag(*eigenvalues) * adj(unitary)
log_rho = unitary * s.diag(*(s.log(x) for x in eigenvalues)) * adj(unitary)
root_rho = unitary * s.diag(*(s.sqrt(x) for x in eigenvalues)) * adj(unitary)
equal(root_rho * root_rho, rho, "physical state square root")
assert rho * sigma != sigma * rho
checks.append("actual scalar control state noncommutes with reference")
J = s.simplify(s.trace((rho - phi(rho)) * (log_rho - log_sigma)))
E = s.simplify(s.trace(root_rho * (root_rho - T(root_rho))))
J_sum = E_sum = s.Integer(0)
for v, weight in zip(V, weights):
    in_rho_basis = adj(unitary) * v * unitary
    for i in range(2):
        for j in range(2):
            x = weight * eigenvalues[j]
            y = eigenvalues[i] / weight
            coefficient = absolute_square(in_rho_basis[i, j]) / 2
            J_sum += coefficient * (x - y) * s.log(x / y)
            E_sum += coefficient * (s.sqrt(x) - s.sqrt(y)) ** 2
equal(J, J_sum, "full noncommuting scalar entropy paired-sum identity")
equal(E, E_sum, "full noncommuting root-energy paired-sum identity")

# The frozen nonmodular witness, amplified by root's supplied tuned ratio.
old_sigma = s.diag(Q(4, 5), Q(1, 5))
tau = s.diag(Q(1, 5), Q(4, 5))
reference = s.kronecker_product(old_sigma, tau)
old_S = s.diag(s.sqrt(2), 1) / 5 ** Q(1, 4)
vectors = [s.Matrix([1, 0]), s.Matrix([Q(3, 5), Q(4, 5)]),
           s.Matrix([Q(4, 5), -Q(3, 5)])]
probabilities = [Q(3, 5), Q(1, 5), Q(1, 5)]
old_V = [s.sqrt(p) * old_S.inv() * v * adj(v) * old_S.inv()
         for p, v in zip(probabilities, vectors)]
U = s.kronecker_product(E01, E01)
commuting_input = U + adj(U)
equal(commuting_input * reference, reference * commuting_input,
      "tuned two-level reference cancels input modular frequency")
amplified_output = sum((s.kronecker_product(v, ident) * commuting_input
                        * adj(s.kronecker_product(v, ident)) for v in old_V), s.zeros(4))
commutator = s.simplify(amplified_output * reference - reference * amplified_output)
assert commutator != s.zeros(4)
checks.append("tuned reference detects nonmodular output frequency")
equal(s.trace(commuting_input * s.kronecker_product(s.diag(2, 1), s.diag(1, 2))),
      0, "ancilla real direction lies in physical weighted trace tangent")

print(json.dumps({
    'status': 'PASS_EXACT_ORIENTATION_CONTROLS',
    'checks': len(checks),
    'assertions': checks,
    'scalar_control_J': str(s.simplify(J)),
    'scalar_control_E': str(s.simplify(E)),
    'scope': 'One analytic modular control, one complex Choi control, and one tuned amplification; not a proof of the universal classification',
    'floating_point_used': False
}, indent=2))
