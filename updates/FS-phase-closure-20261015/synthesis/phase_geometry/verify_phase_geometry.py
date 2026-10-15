"""Exact finite checks for phase_geometry's analytic constructions.

This script does not prove the continuum variational arguments, quasiconvexity,
or historical novelty. No optimizer or sampled phase data is a proof input.
"""
from pathlib import Path
import json
import sympy as S

ROOT = Path(__file__).resolve().parent
checks = []


def check(name, details):
    checks.append({"name": name, "status": "PASS", "details": details})
    print("PASS:", name, flush=True)


y = S.symbols("y", real=True)
pi = S.pi
mean = lambda expr, lo=0, hi=2*pi: S.simplify(S.integrate(expr, (y, lo, hi))/(2*pi))
assert mean(S.cos(y)**4) == S.Rational(3, 8)
q4 = S.Rational(32, 3)
q_mass = q4*mean(S.sin(2*y)**4, 0, pi/2)
q_energy = 16*q4*mean(S.cos(2*y)**4, 0, pi/2)
q_mixed = 4*q4*mean(S.sin(2*y)**2*S.cos(2*y)**2, 0, pi/2)
assert (q_mass, q_energy, q_mixed) == (1, 16, S.Rational(4, 3))
check("Compact arc bump", {"fourth_mass": str(q_mass), "derivative_energy": str(q_energy),
                          "mixed_moment": str(q_mixed)})

p4 = S.Rational(8, 3)
p_mass = p4*mean(S.sin(y/2)**4)
p_energy = p4*mean(S.cos(y/2)**4)/16
p_mixed = p4*mean(S.sin(y/2)**2*S.cos(y/2)**2)/4
assert (p_mass, p_energy, p_mixed) == (1, S.Rational(1, 16), S.Rational(1, 12))
bump_energy = p_energy*q_mass + 2*p_mixed*q_mixed + p_mass*q_energy
assert bump_energy == S.Rational(2345, 144)
check("Two-dimensional separated bump", {"fourth_mass": str(p_mass*q_mass),
                                        "energy": str(bump_energy)})

t = S.symbols("t", real=True)
H = 3*t*t-2*t*t*t
assert H.subs(t, 0) == 0 and H.subs(t, 1) == 1
assert S.diff(H, t).subs(t, 0) == 0 and S.diff(H, t).subs(t, 1) == 0
assert S.expand(S.Rational(3, 2)-S.diff(H, t)-6*(t-S.Rational(1, 2))**2) == 0
check("Cutoff step derivative maximum", {"max_H_prime": "3/2", "max_chi_prime": "3/pi < 1"})

assert S.Rational(1, 256*3**4) < S.Rational(3, 32768)
periodic_N = 32
assert S.Rational(periodic_N**4, 256*4**4) == 16
check("Periodic nonconvexity thresholds", {"N": periodic_N,
      "midpoint_lower": "(8/pi)^4 > 16 using pi < 4", "endpoint_upper": "16"})

N = 1024
delta4 = S.Rational(1, 4*N**4)
assert delta4 <= S.Rational(1, 16)
endpoint_upper = bump_energy+S.Rational(1, 4)
assert endpoint_upper == S.Rational(2381, 144) and endpoint_upper < 17
boundary_upper = S.Rational(1, 24)+S.Rational(17, 128)
assert boundary_upper == S.Rational(67, 384) and boundary_upper < S.Rational(1, 2)
midpoint_contradiction_lower = S.Rational(N**4, 2**33)
assert midpoint_contradiction_lower == 128 and midpoint_contradiction_lower > 17
check("Positive affine-boundary counterexample constants", {
      "N": N, "delta_fourth": str(delta4), "endpoint_upper": str(endpoint_upper),
      "boundary_mass_upper_under_energy_17": str(boundary_upper),
      "midpoint_energy_lower_under_energy_17": ">128", "comparison_threshold": 17})

# G is the supplied left-invariant rank-one-convex quartic. Its global acoustic
# certificate is in the immutable source packet; this script checks only the
# local mixed-phase algebra used by this worker.
a, b, c, d, k, ell = S.symbols("a b c d k ell", real=True)
u = a*a+c*c
v = b*b+d*d
det = a*d-b*c
G = 3*(u+v-2*det)**2+S.Rational(35, 24)*u*u+det*det-S.Rational(5, 2)*det*u
variables = (a, b, c, d)
Hessian = S.hessian(G, variables).subs({a: 1, b: 0, c: 0, d: 1})
expected_Hessian = S.Matrix([[S.Rational(9,2),0,0,-S.Rational(7,2)],
 [0,0,S.Rational(1,2),0], [0,S.Rational(1,2),S.Rational(5,6),0],
 [-S.Rational(7,2),0,0,2]])
assert Hessian == expected_Hessian
T = S.Matrix([[k,0],[ell,0],[0,k],[0,ell]])
acoustic = S.simplify(T.T*Hessian*T)
expected_acoustic = S.Matrix([[S.Rational(9,2)*k*k, -3*k*ell],
 [-3*k*ell, S.Rational(5,6)*k*k+2*ell*ell]])
assert acoustic == expected_acoustic
assert S.factor(acoustic.det()) == S.Rational(15,4)*k**4
schur = S.cancel(acoustic[1,1]-acoustic[0,1]**2/acoustic[0,0])
assert schur == S.Rational(5,6)*k*k
check("G exact acoustic Schur complement at I", {
      "Hessian": str(Hessian), "acoustic": str(acoustic),
      "det_acoustic": str(S.factor(acoustic.det())),
      "schur_for_k_nonzero": str(schur), "value_at_k_zero": "2 ell^2"})

ax, ay, bx, by = S.symbols("ax ay bx by", real=True)
z = S.Matrix([ax, ay, bx, by])
quadratic = S.expand((z.T*Hessian*z)[0])
squares = S.Rational(9,2)*(ax-S.Rational(2,3)*by)**2+S.Rational(5,6)*bx*bx
assert S.expand(quadratic-squares+(ax*by-ay*bx)) == 0
check("G integrated quadratic compensation identity", {
      "pointwise_difference": "D2G(I)[H,H] = squares - det(H)",
      "squares": str(squares)})

p, q, r, s = S.symbols("p q r s", real=True)
A = S.Matrix([[1+S.Rational(2,3)*s*q, S.Rational(2,3)*s*r], [s*p, 1+s*q]])
expansion = S.Poly(S.expand(G.subs(dict(zip(variables, list(A))), simultaneous=True)), s)
c1 = expansion.coeff_monomial(s)
c2 = expansion.coeff_monomial(s**2)
c3 = expansion.coeff_monomial(s**3)
c4 = expansion.coeff_monomial(s**4)
assert S.expand(c1+S.Rational(5,18)*q) == 0
assert S.expand(c2-(5*p*p+4*p*r-4*q*q)/12) == 0
assert S.expand(c3+S.Rational(5,162)*q*(9*p*p+4*q*q)) == 0
assert not c3.has(r)
assert S.simplify(c4.subs({p:1,q:0,r:-S.Rational(3,2)})) == -S.Rational(1,24)
check("G soft-potential exact expansion", {
      "linear": str(S.factor(c1)), "quadratic": str(S.factor(c2)),
      "cubic": str(S.factor(c3)), "quartic": str(S.factor(c4)),
      "cubic_independent_of_vyy": True,
      "quartic_not_pointwise_nonnegative": "p=1,q=0,r=-3/2 gives -1/24"})

receipt = {"status": "PASS", "groups": len(checks), "checks": checks,
           "scope": "exact finite constants and algebra only; analytic proofs in notes",
           "quasiconvexity_theorem": "NOT_ESTABLISHED", "novelty": "UNKNOWN"}
(ROOT/"exact_checks.json").write_text(json.dumps(receipt, indent=2)+"\n")
