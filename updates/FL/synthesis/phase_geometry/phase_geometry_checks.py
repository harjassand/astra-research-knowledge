#!/usr/bin/env python3
"""Independent exact checks for the FL phase-geometry derivation.

SymPy-only identities. These finite symbolic checks support, but do not replace,
the analytic proofs in REPORT.md. No source packet or capital file is modified.
"""
from __future__ import annotations

from itertools import combinations_with_replacement
import sympy as S


def check(name: str, identity) -> None:
    reduced = S.simplify(S.expand(identity))
    if reduced != 0:
        raise AssertionError(f"{name}: {S.factor(reduced)}")
    print("PASS", name)


# Row-major coordinates for a general 2x2 quartic.
a, b, c, d = S.symbols("a b c d", real=True)
xvars = (a, b, c, d)
u = a*a + c*c
v = b*b + d*d
w = a*b + c*d
q = a*d - b*c
quartic_basis = [u*u, v*v, u*v, w*w, u*w, v*w, q*u, q*v, q*w]
monomials = [S.prod(xvars[j] for j in inds)
             for inds in combinations_with_replacement(range(4), 4)]
assert len(monomials) == 35


# Exact variable-phase flux identity at theta=0 for every quartic monomial.
# There V=e1, W=e2, V'=W, W'=-V. Variables h_ij are Hess(theta).
B = S.Matrix(S.symbols("B0:4", real=True))
k1, k2, amp, rx, ry, s = S.symbols("k1 k2 amp rx ry s", real=True)
h11, h12, h22 = S.symbols("h11 h12 h22", real=True)
K = S.Matrix([[h11, h12], [h12, h22]])
Pvec = S.Matrix([0, 0, k1, k2])
Vdir = (S.eye(4)[:, 0], S.eye(4)[:, 1])
Wdir = (S.eye(4)[:, 2], S.eye(4)[:, 3])
grad_r = (rx, ry)
kvec = (k1, k2)
Qvec = S.Matrix([rx, ry, 0, 0])

for f in monomials:
    df = S.Matrix([S.diff(f, z) for z in xvars])
    hf = S.hessian(f, xvars)
    base = B + s * Pvec
    sub = dict(zip(xvars, base))
    dfs = df.subs(sub, simultaneous=True)
    hfs = hf.subs(sub, simultaneous=True)

    # Flux derivative in r, theta, and k. The theta derivative includes
    # both W'=-V in the base matrix and V'=W in the test matrix.
    div_flux = 0
    carrier_defect = 0
    for i in range(2):
        vi = Vdir[i]
        wi = Wdir[i]
        div_flux += grad_r[i] * df.subs(
            dict(zip(xvars, B + amp * Pvec)), simultaneous=True).dot(vi)
        # W' tensor k is -V tensor k; its contraction is written explicitly.
        neg_Vk = S.Matrix([-k1, -k2, 0, 0])
        theta_integrand = s * (neg_Vk.T * hfs * vi)[0] + dfs.dot(wi)
        div_flux += kvec[i] * S.integrate(S.expand(theta_integrand), (s, 0, amp))

        hi = S.Matrix([0, 0, K[i, 0], K[i, 1]])
        carrier_defect += S.integrate(
            S.expand(s * (hi.T * hfs * vi)[0]), (s, 0, amp)
        )

    acoustic_direction = S.Matrix([k1, k2, 0, 0])
    acoustic = S.integrate(
        S.expand(s * (acoustic_direction.T * hfs * acoustic_direction)[0]),
        (s, 0, amp),
    )

    div_flux += carrier_defect
    # The r-derivative term equals DF(B+P)[Q].
    df_end = df.subs(dict(zip(xvars, B + amp * Pvec)), simultaneous=True)
    q_term = df_end.dot(Qvec)
    f_end = f.subs(dict(zip(xvars, B + amp * Pvec)), simultaneous=True)
    f_start = f.subs(dict(zip(xvars, B)), simultaneous=True)
    # div A = DF(B+P)[Q] + F(B+P)-F(B) - acoustic + defect.
    check_name = "variable-phase flux monomial " + str(monomials.index(f) + 1)
    check(check_name, div_flux - (q_term + f_end - f_start - acoustic + carrier_defect))


# For left-SO(2)-invariant quartics, the B=0 phase-curvature vector field.
Lc, Mc, Nc = S.symbols("L M N", real=True)
odd = q * (Lc*u + Mc*v + Nc*w)
Wk = S.Matrix([0, 0, k1, k2])
Vei = (S.eye(4)[:, 0], S.eye(4)[:, 1])
df_odd = S.Matrix([S.diff(odd, var) for var in xvars])
df_odd_at_carrier = df_odd.subs(dict(zip(xvars, Wk)), simultaneous=True)
Xi = S.Matrix([df_odd_at_carrier.dot(Vei[i]) for i in range(2)])
M2 = Lc*k1*k1 + Mc*k2*k2 + Nc*k1*k2
check("orientation-odd Xi formula", Xi[0] - M2*k2)
check("orientation-odd Xi formula", Xi[1] + M2*k1)
for even_f in quartic_basis[:6]:
    df_even = S.Matrix([S.diff(even_f, var) for var in xvars])
    df_even_at_carrier = df_even.subs(dict(zip(xvars, Wk)), simultaneous=True)
    xi_even = S.Matrix([df_even_at_carrier.dot(Vei[i]) for i in range(2)])
    check("orientation-even Xi vanishes", xi_even[0])
    check("orientation-even Xi vanishes", xi_even[1])

g1, g2, n = S.symbols("g1 g2 n", real=True)
div_shear = (
    S.diff(Xi[0], k1) * g2
    + S.diff(Xi[1], k1) * 0
    + S.diff(Xi[1], k2) * 0
    + S.diff(Xi[0], k2) * 0
)
# Substitute k=(g', n), Hess(theta)=diag(g'',0) in the spatial divergence.
div_shear = (S.diff(Xi[0], k1) * g2).subs({k1: g1, k2: n})
check("sheared phase curvature", div_shear - n * (2*Lc*g1 + Nc*n) * g2)


# The all-background defect is not universally zero for non-affine phase.
# For F0(A)=|A|^4, its leading small-amplitude term is 4 r^2 beta^T H alpha.
F0 = (a*a + b*b + c*c + d*d)**2
df0 = S.Matrix([S.diff(F0, z) for z in xvars])
hf0 = S.hessian(F0, xvars)
alpha1, alpha2, beta1, beta2 = S.symbols("alpha1 alpha2 beta1 beta2", real=True)
Hsym = S.Matrix([[h11, h12], [h12, h22]])
alpha = S.Matrix([alpha1, alpha2])
beta = S.Matrix([beta1, beta2])
# At theta=0, B's columns are alpha_j W + beta_j V.
Blocal = S.Matrix([beta1, beta2, alpha1, alpha2])
hrows = (S.Matrix([0, 0, h11, h12]), S.Matrix([0, 0, h12, h22]))
leading = 0
for i in range(2):
    vi = Vei[i]
    leading += (hrows[i].T * hf0.subs(
        dict(zip(xvars, Blocal)), simultaneous=True
    ) * vi)[0]
check("general-background leading curvature contraction",
      leading - 8 * (beta.T * Hsym * alpha)[0])


# Exact signed curvature example with convex F_c=(u+v-2q)^2.
# Directly known coefficients: Fc = even + q*(-4u-4v).
fcL, fcM, fcN = -4, -4, 0
y = S.symbols("y", real=True)
eps, amp_sign = S.symbols("eps amp_sign", real=True)
kk1, kk2 = 1, S.cos(y)
xi1 = (fcL*kk1**2 + fcM*kk2**2 + fcN*kk1*kk2) * kk2
xi2 = -(fcL*kk1**2 + fcM*kk2**2 + fcN*kk1*kk2) * kk1
div_fc = S.diff(xi2, y)
check("convex example div Xi", div_fc + 4*S.sin(2*y))
weighted = (1 - S.Rational(1, 2)*S.sin(2*y)) * div_fc / 4
mean_defect = S.integrate(S.expand_trig(weighted), (y, 0, 2*S.pi)) / (2*S.pi)
assert mean_defect == S.Rational(1, 4)
print("PASS signed convex example mean defect = 1/4")
weighted_reversed = (1 + S.Rational(1, 2)*S.sin(2*y)) * div_fc / 4
mean_reversed = S.integrate(S.expand_trig(weighted_reversed), (y, 0, 2*S.pi)) / (2*S.pi)
assert mean_reversed == -S.Rational(1, 4)
print("PASS reversed amplitude mean defect = -1/4")


# Explicit two-variable amplitude has constant fourth-power transport moment.
eps_amp = S.Rational(1, 5)
zphase = S.symbols("zphase", real=True)
rho = 1 + eps_amp*S.cos(2*zphase)
mean_rho4 = S.integrate(S.expand(rho**4), (zphase, 0, 2*S.pi)) / (2*S.pi)
check("amplitude fourth moment", mean_rho4 - (1 + 3*eps_amp**2 + S.Rational(3, 8)*eps_amp**4))
shift = S.symbols("shift", real=True)
rho_shifted = 1 + eps_amp*S.cos(2*(zphase + shift))
mean_shifted = S.integrate(S.expand(rho_shifted**4), (zphase, 0, 2*S.pi)) / (2*S.pi)
check("transported amplitude fourth moment", mean_shifted - mean_rho4)

# For theta=n*y+g(x), the curvature density is an exact x derivative.
check("shear curvature is a total derivative",
      n*(2*Lc*g1 + Nc*n)*g2
      - S.diff(n*(Lc*g1**2 + Nc*n*g1), g1)*g2)

# The universal zero-background phase PDE is compatible with straight fronts:
# H=lambda k tensor k makes each L/M/N curvature coefficient vanish.
lam = S.symbols("lam", real=True)
straight = {h11: lam*k1**2, h12: lam*k1*k2, h22: lam*k2**2}
div_L = 2*k1*k2*h11 - 2*k1**2*h12
div_M = 2*k2**2*h12 - 2*k1*k2*h22
div_N = k2**2*h11 - k1**2*h22
for expression in (div_L, div_M, div_N):
    check("straight-front curvature vanishes", expression.subs(straight))

print("ALL EXACT PHASE-GEOMETRY CHECKS PASSED")
