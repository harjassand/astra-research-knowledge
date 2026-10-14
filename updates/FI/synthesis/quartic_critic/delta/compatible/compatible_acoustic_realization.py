"""Independent exact audit of a compatible periodic realization of covariance flatness."""
import sympy as s

a, b, c, d, e = s.symbols("a b c d e", real=True)
u = a*a + c*c
v = b*b + d*d
w = a*b + c*d
q = a*d - b*c
G = s.expand(3*(u+v-2*q)**2 + s.Rational(35, 24)*u**2 + q**2 - s.Rational(5, 2)*q*u)
variables = s.Matrix([a, b, c, d])
gradG = s.Matrix([s.diff(G, x) for x in variables])
HG = s.hessian(G, variables)

# m is an integer for periodicity, e=1/(2m); formulas are kept symbolic in e.
m = 1/(2*e)
ap = s.Matrix([1, 3*e])
am = s.Matrix([1, -3*e])
kp_over_m = s.Matrix([1/m, 1])
km_over_m = s.Matrix([-1/m, 1])
rp = s.Matrix([ap[0]*kp_over_m[0], ap[0]*kp_over_m[1], ap[1]*kp_over_m[0], ap[1]*kp_over_m[1]])
rm = s.Matrix([am[0]*km_over_m[0], am[0]*km_over_m[1], am[1]*km_over_m[0], am[1]*km_over_m[1]])
B = s.Matrix([0, 1, 6*e**2, 0])
T = s.Matrix([2, 0, 0, 3])
D = 1 + 13*e**2 + 36*e**4
assert rp.applyfunc(s.factor) == (B + e*T).applyfunc(s.factor)
assert rm.applyfunc(s.factor) == (B - e*T).applyfunc(s.factor)
assert s.factor(rp.dot(rp) - D) == 0
assert s.factor(rm.dot(rm) - D) == 0

# The wavevectors k+=(1,m), k-=(-1,m) define a torus endomorphism of degree 2m.
# For integer m>=1 it is a finite cover, so the two cosine phases are independent
# Haar coordinates. E cos=0, E cos^2=1/2, E[cos(theta+)cos(theta-)]=0.
det_wave = s.det(s.Matrix([[1, m], [-1, m]]))
assert s.factor(det_wave - 2*m) == 0
unitp, unitm = rp/s.sqrt(D), rm/s.sqrt(D)
C = s.simplify((unitp*unitp.T + unitm*unitm.T)/2)
assert s.factor(s.trace(C) - 1) == 0
assert C.rank() == 2
dot = s.factor(unitp.dot(unitm))
assert s.factor(dot - (1-4*e**2)*(1-9*e**2)/D) == 0
assert s.factor(1-dot**2 - 52*e**2*(1+36*e**4)/D**2) == 0
lam_c = s.symbols("lam_c")
expected_cov_char = lam_c**2*(lam_c-(1+dot)/2)*(lam_c-(1-dot)/2)
assert s.factor(C.charpoly(lam_c).as_expr() - expected_cov_char) == 0

# Exact product-phase moments for cos(theta_+),cos(theta_-).
y, zphase = s.symbols("y zphase", real=True)
Xphase = unitp*y + unitm*zphase
phase_sub = dict(zip(variables, Xphase))
moments = {0: s.Integer(1), 1: s.Integer(0), 2: s.Rational(1, 2),
           3: s.Integer(0), 4: s.Rational(3, 8)}
def product_phase_average(poly):
    if isinstance(poly, s.MatrixBase):
        return poly.applyfunc(product_phase_average)
    ppoly = s.Poly(s.expand(poly), y, zphase)
    return s.factor(sum(coeff*moments[i]*moments[j]
                        for (i, j), coeff in ppoly.terms()))
assert product_phase_average(G.subs(phase_sub)) > 0
mean_gradient = product_phase_average(Xphase)
mean_cubic = product_phase_average(gradG.subs(phase_sub))
mean_det = product_phase_average(Xphase[0]*Xphase[3]-Xphase[1]*Xphase[2])
assert mean_gradient == s.zeros(4, 1)
assert mean_cubic == s.zeros(4, 1)
assert mean_det == 0
mean_energy = product_phase_average(G.subs(phase_sub))

# For small e, dot>0; the nonzero covariance eigenvalues are (1 +/- dot)/2.
tau = s.factor((1-dot)/2)
assert s.factor(tau - 13*e**2/D) == 0

def evaluate_hessian_at(x):
    return HG.subs(dict(zip(variables, x))).applyfunc(s.factor)

# Hessian is quadratic in its evaluation point. Independent phases remove cross
# terms, giving H=E D^2G(Dphi)=1/2(D^2G(unit R+)+D^2G(unit R-)).
H = s.simplify((evaluate_hessian_at(rp) + evaluate_hessian_at(rm))/(2*D))
minors = [s.factor(H[:j, :j].det()) for j in range(1, 5)]
expected_minors = [
    2*(321*e**4+104*e**2+6)/D,
    24*(6*e**2+1)*(19*e**2+3)*(321*e**4+104*e**2+6)/D**2,
    24*(321*e**4+104*e**2+6)*(15201*e**8+9752*e**6+2129*e**4+192*e**2+6)/D**3,
    240*e**4*(243*e**4+192*e**2+13)*(15201*e**8+9752*e**6+2129*e**4+192*e**2+6)/D**4,
]
assert all(s.factor(x-y) == 0 for x, y in zip(minors, expected_minors))
assert all(all(coef >= 0 for coef in s.Poly(s.together(mn).as_numer_denom()[0], e).all_coeffs()) for mn in minors)
assert all(s.limit(mn, e, 0, dir="+") > 0 for mn in minors[:3])
assert s.factor(H.det() - expected_minors[3]) == 0

H0 = H.subs(e, 0)
assert H0.rank() == 3
assert H0.nullspace() == [s.Matrix([1, 0, 0, 1])]
H0_expected = s.Matrix([[12, 0, 0, -12], [0, 36, 36, 0], [0, 36, 38, 0], [-12, 0, 0, 12]])
assert H0 == H0_expected
lam_h = s.symbols("lam_h")
assert s.factor(H0.charpoly(lam_h).as_expr() - lam_h*(lam_h-24)*(lam_h**2-74*lam_h+72)) == 0
det_coefficient = s.limit(H.det()/e**4, e, 0, dir="+")
# The nonzero eigenvalues of H0 are 24 and the two roots of x^2-74x+72;
# their product is 24*72=1728. The zero eigenvalue is simple.
nonzero_product = s.Integer(24*72)
small_eigen_coefficient = s.factor(det_coefficient/nonzero_product)
assert det_coefficient == 18720
assert small_eigen_coefficient == s.Rational(65, 6)
ratio = s.factor(small_eigen_coefficient/169)
assert ratio == s.Rational(5, 78)

print("compatible realization exact checks passed")
print("mean gradient, mean determinant, cubic vector, mean energy:", mean_gradient.T, mean_det, mean_cubic.T, mean_energy)
print("wave map determinant:", s.factor(det_wave))
print("D, dot, tau:", D, dot, tau)
print("C trace/rank:", s.simplify(s.trace(C)), C.rank())
print("H leading minors:", minors)
print("det(H)/e^4 limit:", det_coefficient)
print("small eigenvalue/e^4 limit:", small_eigen_coefficient)
print("lambda_min(H)/tau^2 limit:", ratio)
