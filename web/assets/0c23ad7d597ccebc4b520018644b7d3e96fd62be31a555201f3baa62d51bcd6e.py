"""Exact small checks of the reconstructed pair bridge; not a theorem test."""
from pathlib import Path
import json
import sympy as sp

checks = []


def check(name, condition):
    ok = bool(condition)
    checks.append({"name": name, "passed": ok})
    if not ok:
        raise AssertionError(name)


def partial_trace(matrix, keep):
    return sp.Matrix(2, 2, lambda a, b: sum(
        matrix[2*a+k, 2*b+k] if keep == 0 else matrix[2*k+a, 2*k+b]
        for k in range(2)))


def hermitian_full_norm(matrix):
    return sp.simplify(sum(abs(value)*multiplicity
                           for value, multiplicity in matrix.eigenvals().items()))


Q = sp.Rational
c, s = Q(3, 5), Q(4, 5)
rho0 = sp.Matrix([[Q(9, 10), Q(3, 10)], [Q(3, 10), Q(1, 10)]])
rho1 = sp.Matrix([[Q(1, 10), Q(3, 10)], [Q(3, 10), Q(9, 10)]])
v0 = sp.Matrix([9, 3, 3, 1])/10
v1 = sp.Matrix([1, 3, 3, 9])/10
K0 = v0*sp.Matrix([[1, 0]])
K1 = v1*sp.Matrix([[0, 1]])


def broadcaster(matrix):
    return K0*matrix*K0.T+K1*matrix*K1.T


def eb(matrix):
    return matrix[0, 0]*rho0+matrix[1, 1]*rho1


check("both density matrices are trace-one rank-one projectors",
      rho0*rho0 == rho0 and rho1*rho1 == rho1
      and rho0.trace() == rho1.trace() == 1)
check("explicit broadcasting Kraus operators are trace preserving",
      K0.T*K0+K1.T*K1 == sp.eye(2))
check("Kraus output vectors have exactly the promised product states",
      v0*v0.T == sp.kronecker_product(rho0, rho0)
      and v1*v1.T == sp.kronecker_product(rho1, rho1))
for label, rho in enumerate((rho0, rho1)):
    out = broadcaster(rho)
    check(f"label {label}: both broadcast marginals equal the same EB output",
          partial_trace(out, 0) == eb(rho) == partial_trace(out, 1))
    check(f"label {label}: exact half-trace marginal error is 2/25",
          hermitian_full_norm(eb(rho)-rho)/2 == Q(2, 25))
check("pure-state root fidelity equals 3/5",
      (rho0*rho1).T*(rho0*rho1) != sp.zeros(2)
      and ((rho0*rho1).T*(rho0*rho1)).trace() == c*c)
check("affinity equals 9/25 and gap equals 6/25",
      (rho0*rho1).trace() == c*c and c-(rho0*rho1).trace() == Q(6, 25))
check("error agrees with the symbolic half-trace convention s(1-s)/2",
      s*(1-s)/2 == Q(2, 25))

# Exact conditional classical joint/product TV identity.
q = [Q(2, 7), Q(5, 7)]
r = [[Q(3, 4), Q(1, 4)], [Q(1, 5), Q(4, 5)]]
joint = [[q[x]*r[x][y] for y in range(2)] for x in range(2)]
y_marg = [sum(joint[x][y] for x in range(2)) for y in range(2)]
tv = sum(abs(joint[x][y]-q[x]*y_marg[y])
         for x in range(2) for y in range(2))/2
trace_distance_laws = sum(abs(r[0][y]-r[1][y]) for y in range(2))/2
check("binary joint/product TV is exactly 2q0q1 TV(r0,r1)",
      tv == 2*q[0]*q[1]*trace_distance_laws == Q(11, 49))

# Two prefix histories: p_h=1/2, posterior q0=(1/4,3/4).
# Construct the conditional state preparation and both actual residuals.
z0, z1 = sp.diag(1, 0), sp.diag(0, 1)
tau = [[rho0, rho1], [z0, z1]]
post = [[Q(1, 4), Q(3, 4)], [Q(3, 4), Q(1, 4)]]
xi = [sum((post[h][x]*tau[h][x] for x in range(2)), sp.zeros(2))
      for h in range(2)]
residuals, bounds = [], []
for x in range(2):
    marginal = sum((post[h][x]*tau[h][x] for h in range(2)), sp.zeros(2))
    reconstructed = sum((post[h][x]*xi[h] for h in range(2)), sp.zeros(2))
    residuals.append(marginal-reconstructed)
    bounds.append(sum(post[h][x]*hermitian_full_norm(tau[h][x]-xi[h])/2
                      for h in range(2)))
check("both per-label convexity bounds equal 27/80",
      bounds == [Q(27, 80), Q(27, 80)])
check("conditional preparation residuals are opposite and saturate that bound",
      residuals[0] == -residuals[1]
      and hermitian_full_norm(residuals[0])/2 == Q(27, 80))

# Exact noncommuting parallel-sum variational identity used in Appendix A.
left = sp.Matrix([[2, 1], [1, 3]])
right = sp.Matrix([[3, 1], [1, 2]])
t = 2
v = sp.Matrix([1, 2])
parallel = (left.inv()+t*right.inv()).inv()
w = parallel*v
x, y = left.inv()*w, t*right.inv()*w
check("noncommuting parallel-sum minimizer and value are exact",
      x+y == v and (x.T*left*x+y.T*(right/t)*y)[0] == (v.T*parallel*v)[0])

record = {
    "status": "ALL_EXACT_CHECKS_PASSED",
    "check_count": len(checks),
    "checks": checks,
    "qubit_fixture": {"c": "3/5", "s": "4/5", "half_trace_error": "2/25",
                      "root_fidelity": "3/5", "affinity": "9/25", "gap": "6/25"},
    "scope": "Rational algebraic controls only; the universal proof is in PAIR_BRIDGE_PROOF.txt.",
}
Path(__file__).with_name("exact_bridge_replay.json").write_text(
    json.dumps(record, indent=2)+"\n")
print(json.dumps({"status": record["status"], "checks": len(checks)}))
