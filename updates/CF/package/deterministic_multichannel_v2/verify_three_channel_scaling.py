"""Exact algebraic prerequisite checks, not an end-to-end propagation benchmark."""
import json
from pathlib import Path
import sympy as s

u, t, eta = s.symbols('u t eta', real=True)
lam = s.Symbol('lam')
D2 = s.diag(1, 0, -1)
D1 = s.diag(0, s.Rational(1, 3), -s.Rational(1, 3))
D0 = s.Matrix([[-1, 1, s.Rational(1, 3)],
               [1, 0, 2],
               [s.Rational(1, 3), 2, 1]])
Hstar = D2*u*u + D1*u + D0
x = t-s.Rational(1, 2)
Heta = D2*x*x + D1*eta*x + D0*eta*eta
scaled = (Heta.subs(t, s.Rational(1, 2)+eta*u) - eta**2*Hstar)
assert all(s.expand(v) == 0 for v in scaled)

char = s.expand(Hstar.charpoly(lam).as_expr())
disc = s.factor(s.discriminant(char, lam))
disc_poly = s.Poly(disc, u)
root_count = int(disc_poly.count_roots(-s.oo, s.oo))
roots = s.nroots(disc_poly, n=35, maxsteps=200)

def vec(M):
    return s.Matrix(list(M))

# Real Lie algebra of skew-Hermitian traceless matrices. Exact complex rank
# agrees with real rank for a collection within this real form.
basis = []
def add(M):
    if M == s.zeros(3):
        return False
    new = s.Matrix.hstack(*(vec(B) for B in basis), vec(M))
    if new.rank() > len(basis):
        basis.append(M)
        return True
    return False

for D in (D2, D1, D0):
    add(s.I*D)
changed = True
while changed:
    changed = False
    for A in list(basis):
        for B in list(basis):
            changed = add(A*B-B*A) or changed
    if len(basis) == 8:
        break
assert len(basis) == 8

out = {
    'purpose': 'exact prerequisites for a non-spin-1 three-channel coalescence family',
    'sympy_version': s.__version__,
    'Hstar': [[str(v) for v in Hstar.row(i)] for i in range(3)],
    'Heta': [[str(v) for v in Heta.row(i)] for i in range(3)],
    'scaling_identity_exact': True,
    'frequency_choice': 'Omega = eta^(-3), eta = 2^(-B)',
    'rescaled_equation': 'i dpsi/du = Hstar(u) psi',
    'rescaled_endpoints': 'u = +/-1/(2 eta)',
    'characteristic_polynomial': str(char),
    'discriminant': str(disc),
    'discriminant_degree': disc_poly.degree(),
    'real_discriminant_root_count_exact': root_count,
    'complex_discriminant_roots_approximate': [str(z) for z in roots],
    'smallest_imaginary_root_height_approximate': str(min(abs(s.im(z)) for z in roots)),
    'skew_hermitian_lie_algebra_dimension_exact': len(basis),
    'not_spin_1_reduction': True,
    'no_propagator_or_runtime_advantage_tested': True,
}
Path(__file__).with_name('three_channel_scaling_results.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({k: out[k] for k in (
    'scaling_identity_exact', 'discriminant_degree',
    'real_discriminant_root_count_exact',
    'skew_hermitian_lie_algebra_dimension_exact',
    'smallest_imaginary_root_height_approximate')}, indent=2))
