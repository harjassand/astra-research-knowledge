"""Small exact geometry/SOS checks; this does not certify entropy theorems."""
from pathlib import Path
import json
import sympy as sp

x, y, t = sp.symbols('x y t', real=True)
coords = (x, y, t)
f = sp.Function('f')(t)
fp, fpp = sp.diff(f, t), sp.diff(f, t, 2)
g = sp.diag(sp.exp(2*f), sp.exp(-2*f), 1)
gi = g.inv()
zero = sp.Integer(0)
checks = {}

def simp(z):
    return sp.simplify(sp.trigsimp(z))

def check(name, z):
    checks[name] = all(simp(e) == 0 for e in z) if isinstance(z, (list, tuple, sp.MatrixBase)) else simp(z) == 0

Gamma = [[[simp(sum(gi[i,l]*(sp.diff(g[l,k], coords[j])+sp.diff(g[l,j], coords[k])-sp.diff(g[j,k], coords[l])) for l in range(3))/2) for k in range(3)] for j in range(3)] for i in range(3)]
A = sp.Matrix(3, 3, lambda i,j: Gamma[i][j][2])
S = simp((A + gi*A.T*g)/2)
Scov = g*S
check('strain_from_metric', S-sp.diag(fp, -fp, 0))
check('divergence_X', sum(Gamma[i][i][2] for i in range(3)))
check('unit_speed', g[2,2]-1)
check('constant_volume_density', g.det()-1)

divcov = sp.Matrix(3, 1, lambda i,_: simp(sum(gi[j,j]*(sp.diff(Scov[j,i], coords[j])-sum(Gamma[l][j][j]*Scov[l,i]+Gamma[l][j][i]*Scov[j,l] for l in range(3))) for j in range(3))))
check('stress_divergence_from_connection', gi*divcov-sp.Matrix([0,0,-2*fp**2]))

Ric = sp.Matrix(3, 3, lambda i,j: simp(sum(sp.diff(Gamma[k][i][j],coords[k])-sp.diff(Gamma[k][i][k],coords[j])+sum(Gamma[k][k][l]*Gamma[l][i][j]-Gamma[k][j][l]*Gamma[l][i][k] for l in range(3)) for k in range(3))))
check('ricci_from_connection', gi*Ric-sp.diag(-fpp, fpp, -2*fp**2))
check('scalar_curvature', sp.trace(gi*Ric)+2*fp**2)

def sectional(i,j):
    r = sp.diff(Gamma[i][j][j],coords[i])-sp.diff(Gamma[i][i][j],coords[j])+sum(Gamma[i][i][m]*Gamma[m][j][j]-Gamma[i][j][m]*Gamma[m][i][j] for m in range(3))
    return simp(r/g[j,j])

check('three_sectional_curvatures', [sectional(0,1)-fp**2, sectional(0,2)+fpp+fp**2, sectional(1,2)-fpp+fp**2])

a, eps, omega, nu = sp.symbols('a eps omega nu', positive=True)
z = sp.symbols('z', real=True)
fpert = a*t+eps/omega*sp.sin(omega*t)
pressure = -8*nu*a*eps/omega*sp.sin(omega*t)-nu*eps**2/omega*sp.sin(2*omega*t)
force = 4*nu*(a*a+eps*eps/2)
check('constant_force_with_periodic_pressure', 4*nu*sp.diff(fpert,t)**2+sp.diff(pressure,t)-force)
mean = lambda h: simp(sp.integrate(sp.expand_trig(h), (z,0,2*sp.pi))/(2*sp.pi))
check('exact_deficit', mean((a+eps*sp.cos(z))**2)-a*a-eps*eps/2)
check('exact_ricci_energy', mean(2*(eps*omega*sp.sin(z))**2+4*(a+eps*sp.cos(z))**4)-(eps**2*omega**2+4*a**4+12*a*a*eps*eps+sp.Rational(3,2)*eps**4))

q,u,v,b1,b2,h,theta = sp.symbols('q u v b1 b2 h theta', real=True)
Sm = sp.Matrix([[u-q/2,v,b1],[v,-u-q/2,b2],[b1,b2,q]])
xi = sp.Matrix([sp.cos(theta),sp.sin(theta),0])
P = sp.diag(1,1,0)
K = h*(2*xi*xi.T-P)
norm2 = lambda T: sp.trace(T.T*T)
ray = u*sp.cos(2*theta)+v*sp.sin(2*theta)
check('projective_tensor_identity', norm2(Sm-K)-norm2(Sm)-2*h*h+4*h*ray)
check('corrected_rate_SOS', u*u+v*v+h*h-2*h*ray-(ray-h)**2-(u*sp.sin(2*theta)-v*sp.cos(2*theta))**2)
d,qq,c,bx,by = sp.symbols('d qq c bx by', real=True)
Rm=sp.Matrix([[d,c,bx],[c,-d-qq,by],[bx,by,qq]])
check('raw_rate_tracefree_SOS', norm2(Rm)-sp.Rational(3,2)*d*d-2*(qq+d/2)**2-2*c*c-2*bx*bx-2*by*by)

result = {
    'status': 'PASS' if all(checks.values()) else 'FAIL',
    'checks': checks,
    'scope': 'Exact metric connection, strain, stress, curvature, periodic-pressure force, integrals and tensor SOS. No entropy/cocycle theorem or geometric stability certification.',
    'sympy_version': sp.__version__,
}
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert all(checks.values())
