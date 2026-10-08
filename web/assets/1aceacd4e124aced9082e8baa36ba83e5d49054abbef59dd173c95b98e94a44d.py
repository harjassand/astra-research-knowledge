"""Exact small-matrix check for leaf_03.txt (requires SymPy)."""

import sympy as sp

sqrt2, sqrt5 = sp.sqrt(2), sp.sqrt(5)
t = (sqrt5 - 1) / 2

H = sp.diag(0, 1, 2)
E = sp.Matrix(
    [
        [1, 0, 0],
        [0, sp.Rational(1, 2), sqrt2 / 4],
        [0, sqrt2 / 4, sp.Rational(3, 4)],
    ]
)
I = sp.eye(3)

# |chi> = (|ll> - t (|lh>+|hl>)/sqrt(2))/sqrt(1+t^2),
# in tensor basis |0>, |l>, |h>.
chi = sp.zeros(9, 1)
chi[4] = 1 / sp.sqrt(1 + t**2)  # |ll>
chi[5] = -t / sp.sqrt(2 * (1 + t**2))  # |lh>
chi[7] = -t / sp.sqrt(2 * (1 + t**2))  # |hl>

def expect(A):
    return sp.simplify((chi.T * A * chi)[0])


energies = (0, 1, 2)
legal_pairs = [(i, j) for i in range(3) for j in range(3) if energies[i] + energies[j] <= 3]
indices = [3 * i + j for i, j in legal_pairs]
E2_cut = sp.kronecker_product(E, E).extract(indices, indices)
eigenvalues = E2_cut.eigenvals()

miss = expect(sp.kronecker_product(E, E))
first_survival = expect(sp.kronecker_product(E, I))
click_first = sp.simplify(1 - first_survival)
click_second = expect(sp.kronecker_product(E, I - E))
energy_first = expect(sp.kronecker_product(H, I))
energy_second_if_reached = expect(sp.kronecker_product(E, H))
energy_alt = sp.simplify(energy_first + energy_second_if_reached)
energy_alt_if_both_calls = expect(sp.kronecker_product(H, I) + sp.kronecker_product(I, H))

assert sp.simplify(miss - (sp.Rational(3, 8) - sqrt5 / 8)) == 0
assert sp.simplify(first_survival - (sp.Rational(9, 16) - 9 * sqrt5 / 80)) == 0
assert sp.simplify(click_first - (sp.Rational(7, 16) + 9 * sqrt5 / 80)) == 0
assert sp.simplify(click_second - (sp.Rational(3, 16) + sqrt5 / 80)) == 0
assert sp.simplify(click_first + click_second + miss - 1) == 0
assert sp.simplify(energy_first - (sp.Rational(5, 4) - sqrt5 / 20)) == 0
assert sp.simplify(energy_second_if_reached - (sp.Rational(11, 16) - 11 * sqrt5 / 80)) == 0
assert sp.simplify(energy_alt - (sp.Rational(31, 16) - 3 * sqrt5 / 16)) == 0
assert sp.simplify(energy_alt_if_both_calls - (sp.Rational(5, 2) - sqrt5 / 10)) == 0
assert min(sp.N(x) for x in eigenvalues) == sp.N(miss)

print("legal cutoff eigenvalues:", eigenvalues)
print("click at 1:", click_first)
print("click at 2:", click_second)
print("miss both:", miss)
print("expected queries under alternative:", sp.simplify(1 + first_survival))
print("expected input energy under alternative:", energy_alt)
print("alternative input energy if both calls are executed:", energy_alt_if_both_calls)
print("null input energy for ground-state queries:", 0)
