"""Independent exact checks of the entropy-power audit's geometric identities.

These are finite symbolic diagnostics, not entropy or cocycle proof checks.
"""
from pathlib import Path
import json
import sympy as s


def frame_geometry(a, beta, speed):
    # Orthonormal frame (E0,E+,E-), X=speed*E0.
    # [E0,E+]=-a E+, [E0,E-]=a E-, [E+,E-]=beta E0.
    c = [[[s.S.Zero for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for i, j, k, v in [(0, 1, 1, -a), (0, 2, 2, a), (1, 2, 0, beta)]:
        c[i][j][k] = v
        c[j][i][k] = -v
    # Gamma[i][j][k] = <nabla_Ei Ej, Ek>, by Koszul.
    gamma = [[[s.simplify((c[i][j][k] - c[j][k][i] + c[k][i][j])/2)
               for k in range(3)] for j in range(3)] for i in range(3)]
    nx = s.Matrix(3, 3, lambda j, i: speed*gamma[i][0][j])
    strain = s.simplify((nx + nx.T)/2)
    div = s.Matrix(3, 1, lambda j, _: s.simplify(sum(
        -sum(gamma[i][i][k]*strain[k, j] + gamma[i][j][k]*strain[i, k]
             for k in range(3)) for i in range(3))))
    ric = s.Matrix(3, 3, lambda j, k: s.simplify(sum(
        sum(gamma[j][k][l]*gamma[i][l][i]
            - gamma[i][k][l]*gamma[j][l][i]
            - c[i][j][l]*gamma[l][k][i] for l in range(3))
        for i in range(3))))
    return nx, strain, 2*div, ric


a, beta, speed, nu = s.symbols('a beta speed nu', real=True, positive=True)
nx, strain, lx, ric = frame_geometry(a, beta, speed)
checks = {
    'homogeneous_divergence_zero': s.trace(nx) == 0,
    'homogeneous_strain_eigenvalues': strain == s.diag(0, a*speed, -a*speed),
    'homogeneous_strain_norm': s.simplify(s.trace(strain*strain)-2*a*a*speed*speed) == 0,
    'homogeneous_advection_zero': nx[:, 0] == s.zeros(3, 1),
    'homogeneous_deformation_laplacian': lx == s.Matrix([-4*a*a*speed, 0, 0]),
    'homogeneous_power_density': s.simplify((-nu*lx)[0]*speed-4*nu*a*a*speed*speed) == 0,
    'sol_ricci': ric.subs(beta, 0) == s.diag(-2*a*a, 0, 0),
}
# Sasaki hyperbolic-surface frame: E+=(H+V)/sqrt(2), E-=(H-V)/sqrt(2).
# It has a=1, beta=-1, speed=1.
gnx, gs, gl, gr = frame_geometry(s.S.One, -s.S.One, s.S.One)
checks.update({
    'hyperbolic_sasaki_strain': gs == s.diag(0, 1, -1),
    'hyperbolic_sasaki_strain_laplacian': gl == s.Matrix([-4, 0, 0]),
    'hyperbolic_sasaki_ricci_x': gr[0, 0] == -s.Rational(3, 2),
})
q, u, v, b1, b2 = s.symbols('q u v b1 b2', real=True)
block = s.Matrix([[q, b1, b2], [b1, u-q/2, v], [b2, v, -u-q/2]])
checks['normal_block_norm_identity'] = s.simplify(s.trace(block*block)
    - 2*(u*u+v*v)-s.Rational(3, 2)*q*q-2*b1*b1-2*b2*b2) == 0
z, lam = s.symbols('z lam', real=True, positive=True)
sol_g = s.diag(s.exp(2*a*z), s.exp(-2*a*z), 1)
deck_d = s.diag(s.exp(a), s.exp(-a), 1)
checks['sol_deck_metric_invariance'] = s.simplify(deck_d.T*sol_g.subs(z, z-1)*deck_d-sol_g) == s.zeros(3)
cat = s.Matrix([[2, 1], [1, 1]])
lam = (3+s.sqrt(5))/2
checks['cat_eigenvalue_and_volume'] = (cat.det() == 1 and s.simplify(cat.charpoly().as_expr().subs(s.Symbol('lambda'), lam)) == 0)
result = {
    'status': 'PASS' if all(checks.values()) else 'FAIL',
    'checks': checks,
    'generic_ricci': s.sstr(ric),
    'scope': 'Exact homogeneous-frame geometry, Sol gluing, cat eigenvalue, and strain algebra only. No entropy theorem, Oseledets, recurrence, or equality-classification proof is computationally verified.',
}
Path('work/cycle3/entropy_power_checks.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
if not all(checks.values()):
    raise SystemExit(1)
