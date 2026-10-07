"""Exact rational checks of analytic constants in the fresh contour audit."""
from fractions import Fraction as F
from math import factorial, comb
from pathlib import Path
import hashlib
import json

checks = {}
def test(name, value):
    assert value, name
    checks[name] = True

test("phase_cubic_constant_le_1_over_30", F(256, 7935) < F(1, 30))
test("quarter_phase_factor", F(15, 23) ** 4 > F(2, 15))
test("quarter_main_minus_vertical", F(31, 32) - F(1, 8) == F(27, 32))
test("quarter_exp4_lower", sum(F(4 ** j, factorial(j)) for j in range(5)) > 32)
test("quarter_exp7_over3_lower", sum(F(7, 3) ** j / factorial(j) for j in range(4)) > 8)
test("quarter_correction_ratio", F(40, 81) < F(1, 2))

c = F(127, 207)
phase_third_bound = F(25, 10935) / c ** 4
test("third_phase_loss", phase_third_bound < F(1, 60))
vertical_third_coefficient = F(27, 16) - F(25, 108) - F(15, 23)
test("third_vertical_exponent", vertical_third_coefficient > F(4, 5))
test("third_exp5_lower", sum(F(5 ** j, factorial(j)) for j in range(4)) > 36)
test("third_tail_loss", F(8, 27) / 36 < F(1, 120))
test("third_sqrt3_less_9_over5", F(9, 5) ** 2 > 3)
test("third_exp12_over5_lower", sum(F(12, 5) ** j / factorial(j) for j in range(4)) > 8)
test("third_main_minus_vertical", 1 - F(1, 60) - F(1, 120) - F(1, 8) == F(17, 20))
test("third_main_at_least_quarter_constant", F(17, 20) > F(27, 32))
test("third_sqrt3_ge_5_over3", F(5, 3) ** 2 < 3)
test("third_F3_prefactor_less_36", F(14336, 405) < 36)
test("third_F3_exponent", F(629, 144) > F(13, 3))
test("third_exp4_lower54", sum(F(4 ** j, factorial(j)) for j in range(10)) > 54)
test("third_exp13_over3_lower72", 54 * F(4, 3) == 72)
test("third_logF_derivative", F(1, 6) + 1 - F(77, 48) < 0)

# Reconstruct degree elevation and Legendre coefficient identities over Q.
def mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out

def bern(N, k):
    return [F(0)] * k + [F(comb(N, k) * comb(N-k, j) * (-1)**j)
                         for j in range(N-k+1)]

polynomial_fixtures = 0
for N in range(1, 13):
    for ell in range(N+1):
        deg_l_coeff = [F((-1)**(ell-j) * comb(ell,j)) for j in range(ell+1)]
        # Rodrigues formula: d^ell [x^ell(x-1)^ell]/dx^ell / ell!.
        rodrigues = [F((-1)**(ell-j) * comb(ell,j) * comb(ell+j,j)) for j in range(ell+1)]
        elevated = []
        for k in range(N+1):
            terms = [(j, F(comb(ell,j)*comb(N-ell,k-j), comb(N,k)))
                     for j in range(ell+1) if 0 <= k-j <= N-ell]
            assert sum(w for _, w in terms) == 1
            elevated.append(sum(deg_l_coeff[j]*w for j,w in terms))
        expanded = [F(0)] * (N+1)
        for k in range(N+1):
            for j,v in enumerate(bern(N,k)):
                expanded[j] += elevated[k]*v
        assert expanded == rodrigues + [F(0)]*(N-ell)
        assert max(map(abs,elevated)) <= 2**ell
        # Orthogonality to lower monomials and exact norm.
        for j in range(ell):
            assert sum(v/F(i+j+1) for i,v in enumerate(rodrigues)) == 0
        square = mul(rodrigues,rodrigues)
        assert sum(v/F(i+1) for i,v in enumerate(square)) == F(1,2*ell+1)
        polynomial_fixtures += 1

source = Path("work/cycle6/c07_s02/phase2/AXIAL_UNIFORM_SEPARABILITY.txt")
out = {
    "status": "EXACT_CONSTANT_AND_POLYNOMIAL_CHECKS_PASS",
    "scientific_role": "Arithmetic checks support the saved general analytic reconstruction; bounded fixtures are not the all-N proof.",
    "source_path": str(source),
    "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    "checks": checks,
    "polynomial_fixtures": polynomial_fixtures,
    "third_phase_upper_using_c_to_four": str(phase_third_bound),
    "third_vertical_exponent_coefficient": str(vertical_third_coefficient),
}
Path(__file__).with_suffix(".json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
