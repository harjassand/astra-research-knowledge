"""Small exact diagnostics for c08_s02. No entropy/ergodic theorem is tested."""
from pathlib import Path
import json
import sympy as s

x, y, t = s.symbols('x y t', real=True)
u = s.Function('u')(x, y, t)
coords = (x, y, t)
g = s.diag(s.exp(2*u), s.exp(-2*u), 1)
gi = g.inv()
G = [[[s.simplify(sum(gi[k,l]*(s.diff(g[l,j],coords[i])
              +s.diff(g[l,i],coords[j])-s.diff(g[i,j],coords[l]))
              for l in range(3))/2) for k in range(3)]
              for j in range(3)] for i in range(3)]
ric = s.zeros(3)
for j in range(3):
    for k in range(3):
        ric[j,k] = s.simplify(sum(
            s.diff(G[j][k][i],coords[i])-s.diff(G[i][k][i],coords[j])
            +sum(G[j][k][l]*G[i][l][i]-G[i][k][l]*G[j][l][i]
                 for l in range(3)) for i in range(3)))
scalar = s.simplify(sum(gi[i,j]*ric[i,j] for i in range(3) for j in range(3)))
scalar_expected = (2*s.exp(-2*u)*(s.diff(u,x,2)-2*s.diff(u,x)**2)
                   -2*s.exp(2*u)*(s.diff(u,y,2)+2*s.diff(u,y)**2)
                   -2*s.diff(u,t)**2)
strain_upper = s.diag(s.diff(u,t)*s.exp(-2*u),
                      -s.diff(u,t)*s.exp(2*u),0)
div = s.Matrix([s.simplify(sum(s.diff(strain_upper[i,j],coords[j])
          +sum(G[j][k][i]*strain_upper[j,k]+G[j][k][j]*strain_upper[i,k]
                 for k in range(3)) for j in range(3))) for i in range(3)])
div_expected = s.Matrix([
    s.exp(-2*u)*(s.diff(u,t,x)-2*s.diff(u,t)*s.diff(u,x)),
    -s.exp(2*u)*(s.diff(u,t,y)+2*s.diff(u,t)*s.diff(u,y)),
    -2*s.diff(u,t)**2])

h, a, q, b1, b2, z = s.symbols('h a q b1 b2 z', real=True)
v = s.Matrix([0,(1-z*z)/(1+z*z),2*z/(1+z*z)])
P = s.diag(0,1,1)
S = s.Matrix([[q,b1,b2],[b1,a-q/2,0],[b2,0,-a-q/2]])
ideal = h*(2*v*v.T-P)
residual_half = s.simplify(s.trace((S-ideal)**2)/2)
angle_expected = ((a-h)**2+4*a*h*v[2]**2
                  +s.Rational(3,4)*q*q+b1*b1+b2*b2)
contraction_expected = h*(2*(v.T*S*v)[0]+q)

checks = {
    'determinant_one': g.det() == 1,
    'scalar_curvature_formula': s.simplify(scalar-scalar_expected) == 0,
    'strain_divergence_formula': s.simplify(div-div_expected) == s.zeros(3,1),
    'unit_projective_vector': s.simplify((v.T*v)[0]-1) == 0,
    'projective_frobenius_defect': s.simplify(residual_half-angle_expected) == 0,
    'projective_contraction': s.simplify(s.trace(S*ideal)-contraction_expected) == 0,
    'ideal_norm_two_h_squared': s.simplify(s.trace(ideal*ideal)-2*h*h) == 0,
}
# The global power defect is exactly integral f_t^2: integral f_t vanishes.
# For epsilon=n^-2, amplitude=n^-3, two transverse dimensions:
n = s.symbols('n', positive=True)
checks['defect_scale_n_minus_10'] = s.simplify((n**-3)**2*(n**-2)**2-n**-10) == 0
checks['curvature_scale_n'] = s.simplify(n**-3/(n**-2)**2-n) == 0
checks['first_derivative_scale_n_minus_1'] = s.simplify(n**-3/n**-2-n**-1) == 0
result = {'status':'PASS' if all(checks.values()) else 'FAIL',
          'checks':checks,
          'scope':'Exact tensor, curvature, force and scaling identities only. '
                  'No entropy, projective invariant measure, recurrence, '
                  'rigidity theorem, or priority is certified by this script.'}
out = Path(__file__).with_name('geometry_checks.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if not all(checks.values()):
    raise SystemExit(1)
