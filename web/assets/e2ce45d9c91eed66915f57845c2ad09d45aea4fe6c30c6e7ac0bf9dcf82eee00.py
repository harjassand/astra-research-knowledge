"""One exact noncommuting, cross-frequency d3 control of the frozen proof.

This script uses SymPy. It is not a scan or a proof of the universal endpoint.
It verifies the legal generator, exact energy/entropy coefficients, and all
frequency-kernel sums for one fully mixed state with no common sigma vector.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import sympy as sp

checks = {}


def require(condition, label):
    if not condition:
        raise AssertionError(label)
    checks[label] = True


def zero_matrix(M):
    return all(sp.simplify(value) == 0 for value in M)


S = sp.diag(3, 2, 1)
d = sp.diag(sp.sqrt(3), sp.sqrt(2), 1)
B = sp.Matrix([[1, 2, 3], [2, 0, 5], [3, 5, -1]])
v = sp.Matrix([1, 2, 3])
O = sp.eye(3)-v*v.T/7
q_numerators = [sp.Rational(4), sp.Rational(2), sp.Rational(1)]
Qr = O*sp.diag(*q_numerators)*O.T
rho = Qr*Qr/21
sigma = S*S/14
BsB = B*S*B
V = sp.Matrix(3, 3, lambda i, j: 2*BsB[i, j]/(S[i, i]+S[j, j]))
K, A = d*B*d.inv(), d*V*d.inv()
Lrho = (A*rho+rho*A.T)/2-K*rho*K.T
Lsigma = (A*sigma+sigma*A.T)/2-K*sigma*K.T
require(zero_matrix(O.T*O-sp.eye(3)), "exact_state_rotation_orthogonal")
require(all(value != 0 for value in O), "no_common_rho_sigma_eigenvectors")
require(sp.trace(rho) == 1 and sp.trace(sigma) == 1, "states_exactly_normalized")
require(zero_matrix((S*V+V*S)/2-BsB), "exact_Lyapunov_identity")
require(zero_matrix(A+A.T-2*K.T*K), "exact_Lindblad_trace_preservation")
require(zero_matrix(Lsigma), "exact_sigma_stationarity")
require(sp.simplify(sp.trace(Lrho)) == 0, "exact_state_trace_derivative_zero")

l2, l3 = sp.symbols("ln2 ln3", real=True)
logrho_without_scalar = O*sp.diag(4*l2, 2*l2, 0)*O.T
logsigma_without_scalar = sp.diag(2*l3, 2*l2, 0)
J_direct = sp.expand(sp.trace(Lrho*(logrho_without_scalar-logsigma_without_scalar)))
E_direct = sp.simplify(sp.trace(V*rho)-sp.trace(B*Qr*B*Qr)/21)
J2 = sp.radsimp(J_direct.coeff(l2))
J3 = sp.radsimp(J_direct.coeff(l3))
expected_J2 = (sp.Rational(1025424, 16807)
               +(-4337360*sp.sqrt(3)-1881840*sp.sqrt(2)
                 +2566816*sp.sqrt(6))/252105)
expected_J3 = (sp.Rational(4538, 441)
               +(2160*sp.sqrt(2)+1452*sp.sqrt(6)+5460*sp.sqrt(3))/1715)
require(E_direct == sp.Rational(158749, 15435), "exact_energy_value")
require(sp.simplify(J2-expected_J2) == 0, "exact_entropy_ln2_coefficient")
require(sp.simplify(J3-expected_J3) == 0, "exact_entropy_ln3_coefficient")

# Stationary frequencies represented by their positive exponential ratio.
ratios = sorted(set(S[i, i]/S[j, j] for i in range(3) for j in range(3)))
components = {}
for ratio in ratios:
    local = sp.Matrix(3, 3, lambda i, j: B[i, j] if S[i, i]/S[j, j] == ratio else 0)
    components[ratio] = O.T*local*O
require(len(ratios) == 7, "all_seven_coherent_stationary_frequencies")


def rational_log(ratio):
    numerator, denominator = sp.fraction(ratio)
    exponents = {2: 0, 3: 0}
    for integer, sign in [(int(numerator), 1), (int(denominator), -1)]:
        for prime, power in sp.factorint(integer).items():
            require(prime in exponents, "node_ratios_have_only_primes2_and3")
            exponents[prime] += sign*power
    return exponents[2]*l2+exponents[3]*l3


def kernels(rx, ry):
    sinhx, sinhy = (rx-1/rx)/2, (ry-1/ry)/2
    sinhx_half, sinhy_half = (sp.sqrt(rx)-1/sp.sqrt(rx))/2, (sp.sqrt(ry)-1/sp.sqrt(ry))/2
    cosh_difference_half = (sp.sqrt(rx/ry)+sp.sqrt(ry/rx))/2
    energy = sp.radsimp(2*sinhx_half*sinhy_half/cosh_difference_half)
    entropy_half = sp.radsimp((rational_log(rx)*sinhy+rational_log(ry)*sinhx)
                              /(2*cosh_difference_half))
    return energy, entropy_half


E_kernel, J_kernel = sp.Integer(0), sp.Integer(0)
for a in range(3):
    for b in range(3):
        t_ab = q_numerators[a]*q_numerators[b]/21
        beta_ratio = q_numerators[a]/q_numerators[b]
        for omega in ratios:
            for nu in ratios:
                element_product = components[omega][a, b]*components[nu][a, b]
                if element_product == 0:
                    continue
                energy_kernel, entropy_half_kernel = kernels(beta_ratio/omega, beta_ratio/nu)
                E_kernel += t_ab*energy_kernel*element_product
                J_kernel += 2*t_ab*entropy_half_kernel*element_product
require(sp.simplify(E_kernel-E_direct) == 0, "exact_full_energy_frequency_sum")
require(sp.simplify(sp.expand(J_kernel).coeff(l2)-J2) == 0, "exact_full_entropy_frequency_sum_ln2")
require(sp.simplify(sp.expand(J_kernel).coeff(l3)-J3) == 0, "exact_full_entropy_frequency_sum_ln3")

# A coarse exact positivity certificate suffices: ln2>2/3, ln3>1 from their
# atanh series. Brackets below follow by squaring rational endpoints.
s2_lo, s2_hi = F(7, 5), F(3, 2)
s3_lo, s3_hi = F(17, 10), F(9, 5)
s6_lo, s6_hi = F(12, 5), F(5, 2)
require(s2_lo*s2_lo < 2 < s2_hi*s2_hi, "exact_sqrt2_bracket")
require(s3_lo*s3_lo < 3 < s3_hi*s3_hi, "exact_sqrt3_bracket")
require(s6_lo*s6_lo < 6 < s6_hi*s6_hi, "exact_sqrt6_bracket")
j2_lo = F(1025424, 16807)+(-4337360*s3_hi-1881840*s2_hi+2566816*s6_lo)/252105
j3_lo = F(4538, 441)+(2160*s2_lo+1452*s6_lo+5460*s3_lo)/1715
require(j2_lo > 0 and j3_lo > 0, "exact_positive_entropy_coefficient_bounds")
margin = F(2, 3)*j2_lo+j3_lo-4*F(158749, 15435)
require(margin > 0, "exact_J_minus4E_positive")

result = {
    "status": "PASS_ONE_EXACT_NONCOMMUTING_CROSS_FREQUENCY_D3_CONTROL",
    "checks": checks,
    "rho_eigenvalues": ["16/21", "4/21", "1/21"],
    "sigma_eigenvalues": ["9/14", "4/14", "1/14"],
    "energy": str(E_direct),
    "J_ln2_coefficient": str(J2),
    "J_ln3_coefficient": str(J3),
    "J_minus4E_strict_lower_bound": {"numerator": str(margin.numerator), "denominator": str(margin.denominator)},
    "sympy_version": sp.__version__,
    "scope": "One exact physical control and frequency-sum identity replay; universal positivity is proved analytically in the frozen baseline.",
    "external_validation": False,
    "formal_verification": False,
}
Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"status": result["status"], "checks_passed": len(checks), "energy": str(E_direct), "strict_J_minus4E_lower_bound": str(margin)}, indent=2))
