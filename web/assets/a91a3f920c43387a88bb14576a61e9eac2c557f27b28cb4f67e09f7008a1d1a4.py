"""Exact checks for the independently derived constant-shear pressure protocol.

This is symbolic verification of a construction and finite fixtures. It is not
a finite-element solver, proof of the OpenAI release, or a physical experiment.
"""
from pathlib import Path
import json
import math
import time
import sympy as s

t0 = time.perf_counter()
x, y, z = xyz = s.symbols("x y z", real=True)
r2 = x*x + y*y + z*z
X = s.Matrix(xyz)
mu = s.Rational(1)


def lap(p):
    return s.expand(sum(s.diff(p, t, 2) for t in xyz))


def div(v):
    return s.expand(sum(s.diff(v[i], xyz[i]) for i in range(3)))


def grad(p):
    return s.Matrix([s.diff(p, t) for t in xyz])


def monomials(d, homogeneous=False):
    return [x**a * y**b * z**c
            for a in range(d+1) for b in range(d+1-a)
            for c in range(d+1-a-b)
            if not homogeneous or a+b+c == d]


def coefficients(p, mons):
    poly = s.Poly(s.expand(p), *xyz)
    return [poly.coeff_monomial(m) for m in mons]


def integrate(p, sphere=False):
    ans = 0
    for exponents, coeff in s.Poly(s.expand(p), *xyz).terms():
        if any(a % 2 for a in exponents):
            continue
        a, b, c = [q//2 for q in exponents]
        num = s.factorial2(2*a-1)*s.factorial2(2*b-1)*s.factorial2(2*c-1)
        den = s.factorial2(2*(a+b+c)+(1 if sphere else 3))
        ans += coeff * 4*s.pi*num/den
    return s.simplify(ans)


surface = s.groebner([r2-1], z, y, x, domain=s.QQ)


def on_surface(p):
    return s.expand(surface.reduce(s.expand(p))[1])


def harmonic_basis(d):
    mons = monomials(d, True)
    if d < 2:
        return mons
    lows = monomials(d-2, True)
    mat = s.Matrix([coefficients(lap(m), lows) for m in mons]).T
    return [s.expand(sum(v[i]*mons[i] for i in range(len(mons))))
            for v in mat.nullspace()]


product_ranks = []
for degree in (1, 2, 3):
    hs = [p for d in range(degree+1) for p in harmonic_basis(d)]
    ps = monomials(2*degree)
    products = [s.expand(a*b) for i, a in enumerate(hs) for b in hs[i:]]
    matrix = s.Matrix([coefficients(p, ps) for p in products]).T
    rank = matrix.rank()
    assert rank == len(ps)
    product_ranks.append({"L": degree, "loads": len(hs),
                          "symmetric_scalar_data": len(products),
                          "polynomial_dimension": len(ps), "rank": rank})

# Nonconstant reciprocal longitudinal modulus; lambda = 1/a - 2*mu.
# On the unit ball this a stays strictly between 0 and 3/(4*mu).
a = s.Rational(1, 3) + x/20 + x*x/40 + x*y/50 + z*z/60
lam = 1/a - 2*mu
loads = [s.Integer(1), x, y, z]
psi_mons = monomials(3)
poisson_matrix = s.Matrix([
    coefficients(lap((r2-1)*m), psi_mons) for m in psi_mons]).T
assert poisson_matrix.det() != 0
poisson_inverse = poisson_matrix.inv()
physical_checks = []
measured_moments = {}
single_load_q = None

for w in loads + [2+x]:
    ell = s.Poly(w, *xyz).total_degree()
    if ell == 0:
        v = s.zeros(3, 1)
    else:
        homogeneous_w = w - w.subs({x:0,y:0,z:0})
        v = (s.Rational(ell, 1)/(mu*(2*ell+3)*(ell+1))*X*homogeneous_w
             - s.Rational(ell+3, 2)/(mu*(2*ell+3)*(ell+1))*r2*grad(w))
    assert div(v) == 0
    assert all(s.expand(mu*lap(v[i])+s.diff(w, xyz[i])) == 0
               for i in range(3))
    rhs = s.Matrix(coefficients(a*w, psi_mons))
    cc = poisson_inverse*rhs
    psi = s.expand(sum(cc[i]*m for i, m in enumerate(psi_mons)))
    phi = s.expand((r2-1)*psi)
    assert s.expand(lap(phi)-a*w) == 0
    u = v + grad(phi)
    assert s.expand(div(u)-a*w) == 0
    strain = (u.jacobian(xyz)+u.jacobian(xyz).T)/2
    stress = s.eye(3)*(w-2*mu*a*w) + 2*mu*strain
    residual = s.Matrix([sum(s.diff(stress[i,j], xyz[j]) for j in range(3))
                         for i in range(3)])
    assert all(s.expand(p) == 0 for p in residual)
    vn = (X.T*v)[0]
    un = (X.T*u)[0]
    strain_v = (v.jacobian(xyz)+v.jacobian(xyz).T)/2
    tn = (X.T*stress*X)[0]
    tvn = (X.T*(2*mu*strain_v)*X)[0]
    control = tvn+w+4*mu*vn
    assert on_surface(tn+4*mu*un-control) == 0
    assert all(on_surface(p) == 0 for p in (s.eye(3)-X*X.T)*(u-v))
    q = 2*psi  # normal derivative of phi on the unit sphere
    if w == 2+x:
        single_load_q = q
    for h in loads:
        moment = integrate(q*h, True)
        assert s.simplify(moment-integrate(a*w*h)) == 0
        if w in loads:
            measured_moments[str(s.expand(w*h))] = moment
    physical_checks.append({"w": str(w), "PDE_residual_zero": True,
                            "mixed_controls_exact": True,
                            "four_moment_identities_exact": True})

# Recover all ten polynomial coefficients from the deduplicated moments.
quadratic_mons = monomials(2)
gram = s.Matrix([[integrate(p*q) for q in quadratic_mons]
                 for p in quadratic_mons])
observed = s.Matrix([measured_moments[str(p)] for p in quadratic_mons])
recovered = gram.inv()*observed
reconstructed = s.expand(sum(recovered[i]*p for i,p in enumerate(quadratic_mons)))
assert s.expand(reconstructed-a) == 0

# A biased affine harmonic pressure, w=2+x, alone reconstructs quadratic a.
# These ten sensors are all harmonic; the final one has degree three.
one_sensors = [1,x,y,z,x*y,x*z,y*z,x*x-y*y,x*x-z*z,
               x**3-s.Rational(3,2)*x*(y*y+z*z)]
one_matrix = s.Matrix([[integrate(p*(2+x)*h)/s.pi for p in quadratic_mons]
                       for h in one_sensors])
assert one_matrix.det() != 0
one_observed = s.Matrix([integrate(single_load_q*h, True)/s.pi
                        for h in one_sensors])
one_recovered = one_matrix.inv()*one_observed
assert one_recovered == s.Matrix(coefficients(a, quadratic_mons))

# The one-load claim fails already for cubic reciprocal moduli.
cubic_psi = (40*x*x+165*x-2*y*y-2*z*z+164)/40
cubic_hidden = s.expand(s.cancel(lap((r2-1)**2*cubic_psi)/(2+x)))
assert s.Poly(cubic_hidden,*xyz).total_degree() == 3
assert s.expand(lap((r2-1)**2*cubic_psi)-(2+x)*cubic_hidden) == 0
for h in [p for d in range(5) for p in harmonic_basis(d)]:
    assert integrate(cubic_hidden*(2+x)*h) == 0

# Exact finite-bandwidth blindness, including the lambda nonlinear map.
hidden = x**3-3*x*y*y  # harmonic degree three, |hidden| <= 1 on B
assert lap(hidden) == 0
for w in loads:
    for h in loads:
        assert integrate(hidden*w*h) == 0
blind_pair = {"a_plus": str(s.Rational(1,3)+hidden/10),
              "a_minus": str(s.Rational(1,3)-hidden/10),
              "all_degree_one_protocol_moments_equal": True,
              "lambda_sup_separation": str(s.Rational(2,10)/(s.Rational(1,9)-s.Rational(1,100)))}

# Shear calibration, independent of lambda, for f = diag(1,-1,0) x.
A = s.diag(1,-1,0)
f = A*X
calibration = integrate((2*mu*A*X).dot(f), True)
assert s.simplify(calibration-s.Rational(16,3)*s.pi*mu) == 0

depth_bounds = []
r0, beta, sigma = 0.5, 0.1, 0.001
factor = math.sqrt(1+4*r0*r0+r0**4)/(1-r0*r0)**2
for N in (10,20,40,80):
    # Operator difference for a_plus - a_minus = 2*beta chi(r) Y_N.
    delta_upper = 2*beta*r0**(N+3)*(N+1)**1.5*factor
    depth_bounds.append({"N": N, "r0": r0,
                         "Bergman_moment_operator_difference_upper": delta_upper,
                         "Gaussian_unit_scalar_probe_count_lower":
                             sigma*sigma/(delta_upper*delta_upper)})

result = {
    "status": "exact symbolic fixtures; general proofs are separate",
    "sympy": s.__version__,
    "product_span_checks": product_ranks,
    "constructed_physical_solution_checks": physical_checks,
    "quadratic_reconstruction": {"loads": 4, "independent_data": 10,
                                  "a": str(a), "exactly_recovered": True},
    "single_affine_pressure_reconstruction": {
        "w": "2+x", "loads": 1, "scalar_sensors": 10,
        "sensors": [str(h) for h in one_sensors],
        "matrix_rank": one_matrix.rank(),
        "matrix_determinant_without_pi": str(one_matrix.det()),
        "quadratic_a_exactly_recovered": True,
        "cubic_invisible_a": str(cubic_hidden),
        "cubic_zero_normal_response_potential": str((r2-1)**2*cubic_psi),
        "cubic_claim_refuted": True,
    },
    "blind_pair": blind_pair,
    "shear_calibration": str(calibration),
    "depth_sensitivity_bounds": depth_bounds,
    "DN_pressure_energy_constant": "not numerically evaluated",
    "executed_elasticity_FEM": False,
    "physical_experiment": False,
    "release_proof_validated": False,
    "elapsed_seconds": time.perf_counter()-t0,
}
out = Path(__file__).with_name("materials_pressure_check.json")
out.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
