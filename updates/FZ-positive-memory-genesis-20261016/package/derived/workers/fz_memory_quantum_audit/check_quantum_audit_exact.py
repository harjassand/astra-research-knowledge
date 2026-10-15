#!/usr/bin/env python3
"""Independent finite exact diagnostics. These are not an asymptotic proof.

Writes only CHECKS.json adjacent to this script. All matrix calculations use
SymPy exact rational/Gaussian-rational arithmetic. No producer script is run.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction
import hashlib
import json
import platform
import time

import sympy as s

HERE = Path(__file__).resolve().parent
started = time.time()
counts = {}
details = {}


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    counts[name] = counts.get(name, 0) + 1


def eq(name, lhs, rhs):
    if lhs == rhs:
        check(name, True)
        return
    difference = lhs-rhs
    if isinstance(difference, s.MatrixBase):
        check(name, all(s.simplify(v) == 0 for v in difference.todok().values()))
    else:
        check(name, s.simplify(difference) == 0)


I2 = s.SparseMatrix(s.eye(2))
X = s.SparseMatrix([[0, 1], [1, 0]])
Y = s.SparseMatrix([[0, -s.I], [s.I, 0]])
Z = s.SparseMatrix([[1, 0], [0, -1]])
P1 = {"I": I2, "X": X, "Y": Y, "Z": Z}


def tensor(*args):
    return s.SparseMatrix(s.kronecker_product(*args))


def pauli(word):
    return tensor(*(P1[c] for c in word))


def units(d):
    for a in range(d):
        for b in range(d):
            yield s.SparseMatrix(d, d, {(a, b): 1})


def dissipator(J, A):
    R = J.H * J
    return J * A * J.H - (R * A + A * R) / 2


def normalized_choi(f, d):
    result = s.zeros(d*d)
    for a in range(d):
        for b in range(d):
            e = s.SparseMatrix(d, d, {(a, b): 1})
            result += tensor(f(e), e) / d
    return s.SparseMatrix(result)


def partial_output(A, d):
    return s.Matrix(d, d, lambda a, b:
                    sum(A[o*d+a, o*d+b] for o in range(d)))


# 1. A reference-entangled three-data-qubit stabilizer orbit.
g1, g2 = pauli("ZZI"), pauli("IZZ")
I8 = s.SparseMatrix(s.eye(8))
projectors = {(a, b): (I8+a*g1)*(I8+b*g2)/4
              for a, b in product((1, -1), repeat=2)}
amplitudes = {(1, 1): 1+s.I, (1, -1): 2*s.I,
              (-1, 1): 0, (-1, -1): 3}
F = sum((amplitudes[k]*p for k, p in projectors.items()), s.zeros(8))
H = 3*g1+2*g2
bell = s.SparseMatrix(16, 1, {(0, 0): 1, (15, 0): 1})
rho0 = bell*bell.H/2
Qs = [pauli("XXI"), pauli("YZI"), pauli("IYI")]
for word_tuple in product("IXYZ", repeat=3):
    word = "".join(word_tuple)
    E = pauli(word)
    er = tensor(E, I2)
    rho = er*rho0*er.H
    synd = tuple(1 if g*E == E*g else -1 for g in (g1, g2))
    coeff = amplitudes[synd]
    rate = s.simplify(coeff*s.conjugate(coeff))
    eq("reference_syndrome_scalarity", tensor(F, I2)*rho, coeff*rho)
    eq("reference_syndrome_hamiltonian", tensor(H, I2)*rho-rho*tensor(H, I2), s.zeros(16))
    for Q in Qs:
        J = tensor(Q*F, I2)
        qr = tensor(Q, I2)
        eq("reference_entangled_conditional_dissipator", dissipator(J, rho), rate*(qr*rho*qr.H-rho))
        eq("reference_entangled_no_jump_rate", (J.H*J)*rho, rate*rho)
details["reference_orbit"] = {"data_qubits": 3, "reference_qubits": 1,
    "pauli_labels": 64, "multi_qubit_jump_strings": ["XXI", "YZI", "IYI"],
    "arithmetic": "exact rational and Gaussian-rational matrices"}

# 2. The complete correction channel is a different superoperator.
pi0 = s.SparseMatrix([[1, 0], [0, 0]])
pi1 = I2-pi0
J = X*pi1


def C(A):
    return J*A*J.H+pi0*A*pi0


for A in units(2):
    eq("completion_full_superoperator", C(A)-A,
       dissipator(J, A)+dissipator(pi0, A))
offdiag = s.SparseMatrix([[0, 1], [0, 0]])
eq("original_cross_syndrome_rate", dissipator(J, offdiag), -offdiag/2)
eq("completed_cross_syndrome_rate", C(offdiag)-offdiag, -offdiag)
rho_z0 = pi0
coherent_derivative = -s.I*(X*rho_z0-rho_z0*X)
check("coherent_error_leaves_pauli_mixture", coherent_derivative[0, 1] != 0)
euler_choi = normalized_choi(lambda A: A-s.I*(X*A-A*X)/5, 2)
bell_pair = s.Matrix([[1, 0], [0, 1], [0, 1], [1, 0]])
compressed_euler = bell_pair.H*euler_choi*bell_pair/2
eq("hamiltonian_uniformization_negative_minor", s.simplify(compressed_euler.det()), -s.Rational(1, 25))
check("hamiltonian_uniformization_not_cp", any(x < 0 for x in euler_choi.eigenvals()))

# 3. Independently construct the five-qubit code and its fixed full decoder.
gs = [pauli(w) for w in ("XZZXI", "IXZZX", "XIXZZ", "ZXIXZ")]
I32 = s.SparseMatrix(s.eye(32))
P0 = I32
for g in gs:
    P0 = P0*(I32+g)/2
v0 = 4*P0[:, 0]
v1 = pauli("XXXXX")*v0
V = s.SparseMatrix.hstack(v0, v1)
eq("five_qubit_encoding_isometry", V.H*V, I2)
eq("five_qubit_code_projector", V*V.H, P0)
error_words = ["IIIII"]
for q in range(5):
    for p in "XYZ":
        error_words.append("I"*q+p+"I"*(4-q))
errors = [pauli(w) for w in error_words]
Ps, Ks, syndromes = [], [], []
for E in errors:
    syndrome = tuple(1 if g*E == E*g else -1 for g in gs)
    syndromes.append(syndrome)
    P = I32
    for sign, g in zip(syndrome, gs):
        P = P*(I32+sign*g)/2
    Ps.append(P)
    K = V.H*E.H*P
    Ks.append(K)
    eq("five_qubit_decoder_single_kraus", K.H*K, P)
check("five_qubit_syndrome_surjectivity", len(set(syndromes)) == 16)
eq("five_qubit_decoder_trace_preserving", sum((K.H*K for K in Ks), s.zeros(32)), I32)
for a, K in enumerate(Ks):
    for b, E in enumerate(errors):
        eq("five_qubit_all_single_pauli_recovery", K*E*V, I2 if a == b else s.zeros(2))


def first_qubit(A):
    return tensor(A, s.eye(16))


U = (3*I2+4*s.I*X)/5
B0 = s.SparseMatrix([[1, 0], [0, s.Rational(3, 5)]])
B1 = s.SparseMatrix([[0, s.Rational(4, 5)], [0, 0]])
faults = [first_qubit(B0*U), first_qubit(B1*U)]
scalar_weight = 0
scalar_records = []
for f, F in enumerate(faults):
    for a, K in enumerate(Ks):
        L = K*F*V
        c = s.simplify(L[0, 0])
        eq("coherent_and_nonunitary_recovered_scalar", L, c*I2)
        scalar_weight += s.conjugate(c)*c
        if c:
            scalar_records.append({"fault_kraus": f, "syndrome": error_words[a], "scalar": str(c)})
eq("coherent_and_nonunitary_scalar_normalization", s.simplify(scalar_weight), 1)
details["scalar_kraus_example"] = scalar_records

# 4. Persistent, shared bath, with a selective ideal correction in between.
# Both scheduled memory interactions act on the first data qubit plus the
# same bath qubit. Their operator coefficients do not commute on the bath.
Ib = s.SparseMatrix(s.eye(64))
Ux = (3*Ib+4*s.I*tensor(first_qubit(X), X))/5
Uz = (5*Ib+12*s.I*tensor(first_qubit(Z), Z))/13
eq("persistent_bath_joint_unitary", Ux.H*Ux, Ib)
eq("persistent_bath_joint_unitary", Uz.H*Uz, Ib)
X0 = first_qubit(X)
Px = Ps[error_words.index("XIIII")]
correction_kraus = [X0*Px, I32-Px]
eq("persistent_bath_completed_correction", sum((A.H*A for A in correction_kraus), s.zeros(32)), I32)
bath_kraus, bath_records = [], []
for j, A in enumerate(correction_kraus):
    total = Uz*tensor(A, I2)*Ux
    for a, K in enumerate(Ks):
        L = tensor(K, I2)*total*tensor(V, I2)
        B = s.SparseMatrix(L[:2, :2]).applyfunc(s.simplify)
        eq("persistent_bath_recovered_factorization", L, tensor(I2, B))
        bath_kraus.append(B)
        if B != s.zeros(2):
            bath_records.append({"correction_record": j, "syndrome": error_words[a], "bath_matrix": str(B)})
eq("persistent_bath_normalization", sum((B.H*B for B in bath_kraus), s.zeros(2)), I2)
details["persistent_bath"] = {"bath_qubits": 1,
    "faults": "joint coherent interactions, same bath reused; selective syndrome correction between them",
    "nonzero_records": bath_records}

# 5. Sharp diamond inradius boundary. The norm is proved in REPORT.md;
# these finite checks corroborate exact Choi boundary and failure outside it.
radius_records = []
for d in (2, 3, 4, 8):
    Id = s.SparseMatrix(s.eye(d))
    om = s.SparseMatrix(d*d, 1, {(i*d+i, 0): 1 for i in range(d)})
    bell_projector = om*om.H/d
    JD = s.SparseMatrix(s.eye(d*d))/d**2
    a = s.Rational(1, d*d-1)
    JE = a*(JD-bell_projector)
    Jboundary = JD+JE
    eq("sharp_radius_trace_annihilation", partial_output(JE, d), s.zeros(d))
    eq("sharp_radius_zero_eigenvector", Jboundary*om, s.zeros(d*d, 1))
    eq("sharp_radius_positive_complement", Jboundary, (s.eye(d*d)-bell_projector)/(d*d-1))
    Joutside = JD+s.Rational(11, 10)*JE
    rayleigh = s.simplify((om.H*Joutside*om)[0]/d)
    eq("sharp_radius_outside_negative_eigenvalue", rayleigh, -s.Rational(1, 10*d*d))
    radius_records.append({"d": d, "sharp_diamond_radius_per_unit_floor": str(s.Rational(2, d*d)),
        "boundary_min_choi_eigenvalue": "0", "outside_rayleigh_quotient": str(rayleigh)})
details["sharp_radius"] = radius_records

# 6. Exact Hamiltonian directional criterion, balanced spectra at the boundary.
ham_records = []
for d in (2, 4):
    H = s.diag(*([-s.Rational(1, d*d)]*(d//2)+[s.Rational(1, d*d)]*(d//2)))
    D = lambda A: s.trace(A)*s.eye(d)/d
    E = lambda A: -s.I*(H*A-A*H)
    JE = normalized_choi(E, d)
    JN = normalized_choi(lambda A: D(A)+E(A), d)
    eigs = JN.eigenvals()
    check("hamiltonian_choi_boundary_positive", all(x.is_nonnegative for x in eigs))
    check("hamiltonian_choi_boundary_singular", 0 in eigs)
    sigma2 = s.trace(H*H)/d-(s.trace(H)/d)**2
    eq("hamiltonian_choi_exact_variance", s.trace(JE*JE), 2*sigma2)
    Jbad = normalized_choi(lambda A: D(A)+s.Rational(11, 10)*E(A), d)
    check("hamiltonian_choi_above_boundary_fails", any(x < 0 for x in Jbad.eigenvals()))
    ham_records.append({"d": d, "sigma_H_squared": str(sigma2), "floor_rate": "1",
        "boundary_eigenvalues": {str(k): int(v) for k, v in eigs.items()}})
details["hamiltonian_directional_criterion"] = ham_records

# 7. A variable proposal rate improves Hamiltonian scaling from d^-2 to d^-1.
rate_records = []
for d in (2, 4, 8):
    h = s.Rational(1, 2*d)
    H = s.diag(*([-h]*(d//2)+[h]*(d//2)))
    nu = s.Integer(1)
    gamma = nu*(1-s.Rational(1, d*d))+d*d*h*h/nu
    D = lambda A: s.trace(A)*s.eye(d)/d
    E = lambda A: -s.I*(H*A-A*H)
    JG = normalized_choi(lambda A: nu*(D(A)-A)+E(A), d)
    p = s.Matrix(d*d, 1, lambda i, j: 1 if i//d == i % d else 0)
    q = tensor(H/h, s.eye(d))*p
    bell_basis = s.Matrix.hstack(p, q)
    JId = p*p.H/d
    JN = JId+JG/gamma
    block = (bell_basis.H*JN*bell_basis/d).applyfunc(s.simplify)
    expected = s.Matrix([[1-nu/gamma+nu/(gamma*d*d), s.I*h/gamma],
                         [-s.I*h/gamma, nu/(gamma*d*d)]])
    eq("hamiltonian_variable_rate_exact_block", block, expected)
    eq("hamiltonian_variable_rate_boundary_determinant", s.simplify(block.det()), 0)
    check("hamiltonian_variable_rate_positive_trace", s.simplify(s.trace(block)) > 0)
    bad_gamma = s.Rational(9, 10)*gamma
    bad_block = (bell_basis.H*(JId+JG/bad_gamma)*bell_basis/d).applyfunc(s.simplify)
    check("hamiltonian_variable_rate_below_boundary_fails", s.simplify(bad_block.det()) < 0)
    rate_records.append({"d": d, "nu": str(nu), "sigma_H": str(h),
        "minimal_gamma": str(gamma), "fixed_gamma_nu_criterion_holds": bool(d*d*h <= nu)})
details["hamiltonian_variable_rate"] = rate_records

# 8. Sharpness also applies to the whole local-generator GKSL neighborhood:
# a negative conditional Choi direction perpendicular to the identity fails.
for d in (2, 3, 4, 8):
    om = s.SparseMatrix(d*d, 1, {(i*d+i, 0): 1 for i in range(d)})
    shift = s.SparseMatrix(d, d, {((i+1) % d, i): 1 for i in range(d)})
    w = tensor(shift, s.eye(d))*om
    phi, phi_w = om*om.H/d, w*w.H/d
    JD = s.SparseMatrix(s.eye(d*d))/d**2
    a = s.Rational(11, 10*(d*d-1))
    JL = JD-phi+a*(JD-phi_w)
    eq("gksl_ball_witness_orthogonal_identity", (om.H*w)[0], 0)
    eq("gksl_ball_witness_negative_conditional_choi", s.simplify((w.H*JL*w)[0]/d), -s.Rational(1, 10*d*d))

receipt = {"status": "PASS", "scope": "finite exact diagnostics, not a universal or asymptotic proof",
    "python": platform.python_version(), "sympy": s.__version__,
    "counted_assertions": sum(counts.values()), "counts": counts, "details": details,
    "elapsed_seconds": round(time.time()-started, 3),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/"CHECKS.json").write_text(json.dumps(receipt, indent=2)+"\n")
print(json.dumps({k: receipt[k] for k in ("status", "scope", "counted_assertions", "elapsed_seconds")}))
