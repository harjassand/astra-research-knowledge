"""Independent exact checks for the FK transition-certificate delta audit.

This script is intentionally separate from work/FK-root's numerical checker.
It checks one rational sector-weight witness, a finite clipping fixture, and
the exact Matsubara cosine functional.  General claims are proved in REPORT.md.
"""

from fractions import Fraction
import json
from pathlib import Path

import sympy as sp


# Sector weights: beta=log(2), d=eta=1, D=log(3)/log(2), c=1/2.
# Then exp(-beta)=1/2 and exp(-beta*D)=1/3, so the canonical first-block
# weight is 3/4.  The source mixture below instead has w=1/2.
r = Fraction(1, 2)
c2 = Fraction(1, 4)
w = Fraction(1, 2)
w_star = Fraction(3, 4)
tanh_beta_half = Fraction(1, 3)
folded_y = Fraction(1, 3)  # a=1, d=eta=1

def block_q_plus(weight):
    return (weight + (1 - weight) * c2) / (1 + r)

q_plus = block_q_plus(w)
q_minus = r * q_plus
q_plus_star = block_q_plus(w_star)
q_minus_star = r * q_plus_star
chi_mixture = Fraction(2, 1) * tanh_beta_half / 2 * (w + (1 - w) * c2)
chi_canonical = Fraction(2, 1) * tanh_beta_half / 2 * (w_star + (1 - w_star) * c2)
assert q_plus == Fraction(5, 12)
assert q_minus == Fraction(5, 24)
assert q_minus / q_plus == r
assert q_plus_star == Fraction(13, 24)
assert q_minus_star / q_plus_star == r
assert folded_y * (q_plus + q_minus) == chi_mixture == Fraction(5, 24)
assert chi_canonical == Fraction(13, 48)
assert chi_canonical - chi_mixture == Fraction(1, 16)


# Degeneracy guard: merely commuting Kraus operators (a weaker QND reading)
# can reshuffle populations inside an energy eigenspace.  H has a twofold
# E=0 sector and one E=1 level.  The trace-preserving channel below commutes
# with H but is not a function-of-H instrument.
H_deg = sp.diag(0, 0, 1)
rho_gibbs = sp.diag(sp.Rational(2, 5), sp.Rational(2, 5), sp.Rational(1, 5))
K0 = sp.diag(1, 0, 1)
K1 = sp.Matrix([[0, 1, 0], [0, 0, 0], [0, 0, 0]])
A_deg = sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]])
assert K0.H * K0 + K1.H * K1 == sp.eye(3)
assert H_deg * K0 == K0 * H_deg and H_deg * K1 == K1 * H_deg
rho_after_weak_qnd = K0 * rho_gibbs * K0.H + K1 * rho_gibbs * K1.H
assert rho_after_weak_qnd == sp.diag(sp.Rational(4, 5), 0, sp.Rational(1, 5))

def signed_transition_mass(rho, signed_gap):
    return sp.simplify(sum(
        rho[i, i] * abs(A_deg[i, j])**2
        for i in range(3) for j in range(3)
        if H_deg[j, j] - H_deg[i, i] == signed_gap
    ))

qplus_ideal = signed_transition_mass(rho_gibbs, 1)
qminus_ideal = signed_transition_mass(rho_gibbs, -1)
qplus_after = signed_transition_mass(rho_after_weak_qnd, 1)
qminus_after = signed_transition_mass(rho_after_weak_qnd, -1)
y_deg = sp.Rational(1, 3)  # beta=log(2), gap=eta=1, a=1
assert (qplus_ideal, qminus_ideal, qplus_after, qminus_after) == (
    sp.Rational(2, 5), sp.Rational(1, 5), sp.Rational(4, 5), sp.Rational(1, 5))
assert qminus_ideal / qplus_ideal == sp.Rational(1, 2)
assert qminus_after / qplus_after == sp.Rational(1, 4)
assert y_deg * (qplus_ideal + qminus_ideal) == sp.Rational(1, 5)
assert y_deg * (qplus_after + qminus_after) == sp.Rational(1, 3)


# Exact two-level clipping fixture: H=diag(0,1), beta=log(2), eta=L=1,
# A=2 sigma_x and clip(A,[-1,1])=sigma_x.
beta_symbol = sp.log(2)
p_low, p_high = sp.Rational(2, 3), sp.Rational(1, 3)
gap = sp.Integer(1)
eta = sp.Integer(1)
def chi_two_level(matrix_element):
    return sp.cancel(2 * gap * (p_low - p_high) * matrix_element**2 /
                     (gap**2 + eta**2))

chi_A = chi_two_level(sp.Integer(2))
chi_Aclip = chi_two_level(sp.Integer(1))
M2, M4, clip_L = sp.Integer(4), sp.Integer(16), sp.Integer(1)
tail_bound = sp.simplify(2 * beta_symbol * sp.sqrt(M2 * M4) / clip_L)
assert chi_A == sp.Rational(4, 3)
assert chi_Aclip == sp.Rational(1, 3)
assert chi_A - chi_Aclip == 1
# log(2)>1/2 follows by integrating 1/x on [1,2], hence this exact lower
# bound already proves the certificate's right side exceeds the error.
assert sp.simplify((tail_bound - 8) - (16 * sp.log(2) - 8)) == 0


# Exact Matsubara functional: with omega=2*pi/beta, the real signed measure
# cos(omega*tau) d tau represents 2d/(d^2+omega^2).
b, d = sp.symbols("b d", positive=True, finite=True)
omega = 2 * sp.pi / b
laplace_cos = (d * (1 - sp.exp(-b * d) * sp.cos(omega * b)) +
               omega * sp.exp(-b * d) * sp.sin(omega * b)) / (d**2 + omega**2)
euclidean_functional = sp.simplify(2 * laplace_cos / (1 - sp.exp(-b * d)))
assert sp.simplify(euclidean_functional - 2 * d / (d**2 + omega**2)) == 0

# The residues of (1-exp(-beta*z))*2z/(z^2+eta^2) at z=+/- i eta are
# respectively 1-exp(-i beta eta) and 1-exp(+i beta eta); both vanish exactly
# at beta*eta in 2*pi*Z and otherwise are nonzero.
I = sp.I
be, et = sp.symbols("beta eta", positive=True, real=True)
res_plus = 1 - sp.exp(-I * be * et)
res_minus = 1 - sp.exp(I * be * et)
assert sp.simplify(res_plus.subs(et, 2 * sp.pi / be)) == 0
assert sp.simplify(res_minus.subs(et, 2 * sp.pi / be)) == 0


result = {
    "status": "PASS",
    "sector_witness": {
        "beta": "log(2)", "gap": "1", "eta": "1", "D": "log(3)/log(2)",
        "c": "1/2", "source_w": "1/2", "canonical_w": "3/4",
        "q_plus_source": str(q_plus), "q_minus_source": str(q_minus),
        "q_minus_over_q_plus": str(q_minus / q_plus),
        "folded_mean_source": str(chi_mixture),
        "folded_mean_canonical": str(chi_canonical),
        "canonical_minus_source_response": str(chi_canonical - chi_mixture),
        "interpretation": "local balance holds; source-weighted and canonical targets differ",
    },
    "degenerate_qnd_guard": {
        "H": "diag(0,0,1)", "rho": "diag(2/5,2/5,1/5)",
        "kraus": ["diag(1,0,1)", "|0a><0b|"],
        "kraus_commute_with_H": True, "kraus_are_functions_of_H": False,
        "q_ratio_before": "1/2", "q_ratio_after": "1/4",
        "folded_mean_before": "1/5", "folded_mean_after": "1/3",
        "interpretation": "commutation alone can disturb Gibbs populations inside a degenerate energy sector",
    },
    "finite_clipping_fixture": {
        "chi_A": str(chi_A), "chi_Aclip": str(chi_Aclip),
        "absolute_error": str(chi_A - chi_Aclip), "M2": str(M2), "M4": str(M4),
        "L": str(clip_L), "claimed_bound": str(tail_bound),
        "exact_sufficient_comparison": "16*log(2)>1",
    },
    "euclidean_functional": {
        "matsubara_identity": "cos(2*pi*tau/beta) d tau gives 2d/(d^2+(2*pi/beta)^2)",
        "residues": ["1-exp(-i*beta*eta)", "1-exp(i*beta*eta)"],
        "nonremovable_except": "beta*eta in 2*pi*Z",
    },
}
out = Path(__file__).with_name("exact_delta_results.json")
out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
