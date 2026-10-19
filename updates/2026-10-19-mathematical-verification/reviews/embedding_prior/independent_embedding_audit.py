# Public selected edition: retain rational-P and older-H verification only.
"""Independent local reconstruction. Does not import or execute the source archive.

Public H is transcribed from arXiv:2005.00821v1, Example 3.2.
The rational P and Q0 are rebuilt from their spectral blocks, not copied from a
prior checker. Symbolic identities give the proof; high precision expm is a
separate diagnostic. Outputs stay in this review directory.
"""
from pathlib import Path
import json
import platform
import hashlib
import sympy as s
import mpmath as mp

BASE = Path(__file__).resolve().parent
z = s.symbols("z")
one = s.ones(4, 1)
I = s.eye(4)
Zero = s.zeros(4)
checks = {}

def exact(name, expression):
    ok = all(s.simplify(x) == 0 for x in expression) if isinstance(expression, s.MatrixBase) else s.simplify(expression) == 0
    checks[name] = bool(ok)
    assert ok, name

def entries(M):
    return [[str(x) for x in M.row(i)] for i in range(M.rows)]

def mp_matrix(M):
    return mp.matrix([[mp.mpf(str(s.N(M[i, j], mp.mp.dps + 10))) for j in range(M.cols)] for i in range(M.rows)])

def maxabs(M):
    return max(abs(x) for x in M)

def digits(x):
    return mp.nstr(x, 65)

# Rational observation, reconstructed in an orthonormal spectral basis.
v = s.Matrix([1, -1, 0, 0]) / s.sqrt(2)
u = s.Matrix([1, 1, -1, -1]) / 2
w = s.Matrix([0, 0, 1, -1]) / s.sqrt(2)
J = one * one.T / 4
V, U, W = v * v.T, u * u.T, w * w.T
E = U + W
exact("rational_projectors_sum_identity", J + V + E - I)
for name, X in [("J", J), ("V", V), ("E", E)]:
    exact("rational_projector_" + name, X * X - X)
exact("rational_projectors_orthogonal", V * E)

a, b, t = s.symbols("a b t", real=True)
L = -a * V - b * E
R = t * (U - W) + 2 * s.sqrt(2) * t * (u * w.T - w * u.T)
Q = s.simplify(L + R)
exact("rational_R_squared", R * R + 7 * t**2 * E)
exact("rational_L_R_commute", L * R - R * L)
exact("rational_Q_rows_zero", Q * one)
exact("rational_Q_columns_zero", one.T * Q)
exact("rational_Q_charpoly", Q.charpoly(z).as_expr() - z * (z + a) * ((z + b)**2 + 7 * t**2))
av, bv, tv = 8 * s.log(2), 18 * s.log(2), 2 * s.pi / s.sqrt(7)
P = J + s.Rational(1, 2**8) * V + s.Rational(1, 2**18) * E
L0 = L.subs({a: av, b: bv})
Q0 = Q.subs({a: av, b: bv, t: tv})
R0 = R.subs(t, tv)
expected_num = s.Matrix([[264193,260097,262143,262143],
                         [260097,264193,262143,262143],
                         [262143,262143,262147,262143],
                         [262143,262143,262143,262147]])
exact("rational_P_exact_entries", P - expected_num / 1048576)
exact("rational_P_row_sums", P * one - one)
exact("rational_P_symmetric", P - P.T)
exact("rational_P_eigen_one", P * one - one)
exact("rational_P_eigen_v", P * v - v / 2**8)
exact("rational_P_eigen_u", P * u - u / 2**18)
exact("rational_P_eigen_w", P * w - w / 2**18)
exact("rational_log_negative_entry", L0[0, 1] + s.log(2) / 2)
exact("rational_R0_squared", R0**2 + 4 * s.pi**2 * E)

# A public older generator, transcribed before using any private H algebra.
H = s.Matrix([[-21,4,16,1], [7,-9,1,1], [1,1,-9,7], [1,16,4,-21]])
exact("old_H_rows_zero", H * one)
exact("old_H_charpoly", H.charpoly(z).as_expr() - z * (z + 28) * ((z + 16)**2 + 36))
# Derive the stationary vector, the isolated real eigenvector, and projectors.
pi_raw = H.T.nullspace()[0]
pi_vec = pi_raw / sum(pi_raw)
r_raw = (H + 28 * I).nullspace()[0]
r = s.Matrix([s.simplify(x * (-5) / r_raw[0]) for x in r_raw])
D = s.diag(*pi_vec)
E1 = one * pi_vec.T
E28 = r * (r.T * D) / (r.T * D * r)[0]
E16 = I - E1 - E28
T = -28 * E28 - 16 * E16
C = H - T
for name, X in [("E1", E1), ("E28", E28), ("E16", E16)]:
    exact("old_projector_" + name, X * X - X)
exact("old_projectors_orthogonal", E28 * E16)
exact("old_C_supported_on_E16", C * E16 - C)
exact("old_C_squared", C**2 + 36 * E16)
exact("old_T_C_commute", T * C - C * T)
exact("old_pi_stationary_H", pi_vec.T * H)
exact("old_weighted_reversible_E28", D * E28 - E28.T * D)
exact("old_weighted_reversible_E16", D * E16 - E16.T * D)
exact("old_weighted_reversible_log", D * T - T.T * D)
exact("old_log_negative_entry", T[0, 3] + 2)
alpha, beta = s.symbols("alpha beta", positive=True)
Pold_formal = E1 + alpha * E28 + beta * E16
exact("old_P_row_sums", Pold_formal * one - one)
exact("old_P_weighted_reversibility", D * Pold_formal - Pold_formal.T * D)

mp.mp.dps = 100
qmp, pmp = mp_matrix(Q0), mp_matrix(P)
hmp, tmp = mp_matrix(H), mp_matrix(T)
pold_formula = mp_matrix(E1) + mp.exp(-28 * mp.pi) * mp_matrix(E28) + mp.exp(-16 * mp.pi) * mp_matrix(E16)
pold_expm = mp.expm(mp.pi * hmp)
numeric = {
    "precision_decimal_digits": mp.mp.dps,
    "rational_expm_Q0_error_max": digits(maxabs(mp.expm(qmp) - pmp)),
    "rational_min_offdiagonal_Q0": digits(min(qmp[i,j] for i in range(4) for j in range(4) if i != j)),
    "rational_log_12": digits(mp.mpf(str(s.N(L0[0,1],110)))),
    "rational_Q0_matrix": [[digits(qmp[i,j]) for j in range(4)] for i in range(4)],
    "old_expm_piH_error_max": digits(maxabs(pold_expm - pold_formula)),
    "old_expm_piT_error_max": digits(maxabs(mp.expm(mp.pi * tmp) - pold_formula)),
    "old_log_14": digits(-2 * mp.pi),
    "old_min_offdiagonal_piH": digits(mp.pi),
    "old_smallest_P_entry": digits(min(pold_formula)),
    "old_H_not_reversible_max_balance_error": digits(maxabs(mp_matrix(D*H - H.T*D))),
}
assert mp.mpf(numeric["rational_expm_Q0_error_max"]) < mp.mpf("1e-95")
assert mp.mpf(numeric["old_expm_piH_error_max"]) < mp.mpf("1e-95")
assert mp.mpf(numeric["old_expm_piT_error_max"]) < mp.mpf("1e-95")
assert mp.mpf(numeric["rational_min_offdiagonal_Q0"]) > 0

out = {
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "python": platform.python_version(), "sympy": s.__version__, "mpmath": mp.__version__,
    "all_symbolic_checks_pass": all(checks.values()), "symbolic_checks": checks,
    "rational_P": entries(P), "rational_Q0_symbolic": entries(Q),
    "rational_principal_log": entries(L0),
    "old_H": entries(H), "old_H_charpoly": str(s.factor(H.charpoly(z).as_expr())),
    "old_stationary_vector": [str(x) for x in pi_vec],
    "old_real_eigenvector_minus_28": [str(x) for x in r],
    "old_E1": entries(E1), "old_E28": entries(E28), "old_E16": entries(E16),
    "old_principal_log_div_pi": entries(T), "old_C": entries(C),
    "numeric_checks": numeric,
    "limits": "Symbolic identities plus mathematical arguments establish the stated counterexamples. Numerical expm is a diagnostic, not independent peer or formal proof. No archive scripts imported or executed."
}
(BASE / "independent_checks.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({"all_symbolic_checks_pass":out["all_symbolic_checks_pass"], "symbolic_check_count":len(checks),"numeric_checks":numeric},indent=2))
