"""Exact algebra and bounded diagnostics, not external/formal verification."""
from pathlib import Path
import json
import hashlib
import sympy as s
import mpmath as mp

BASE = Path(__file__).resolve().parent
x, b = s.symbols("x b", real=True, nonzero=True)
I = s.eye(2)
Z = s.diag(1, -1)
X = s.Matrix([[0, 1], [1, 0]])
K = b*s.sinh(x)/x*X
Q2 = b**2*s.diag(
    s.exp(-x)*(s.sinh(x)/x+s.cosh(x)/x-s.sinh(x)/x**2),
    s.exp(x)*(s.sinh(x)/x-s.cosh(x)/x+s.sinh(x)/x**2),
)
cost = b**2*(s.sinh(2*x)-2*x)/(2*x**2)
covariance_residual = (Q2-K*K+cost*Z).applyfunc(
    lambda v: s.simplify(s.expand(v.rewrite(s.exp))))
assert covariance_residual == s.zeros(2)

HJ = s.Matrix([[45, 20], [20, 5]])/9
v = s.Matrix([1, -2])/s.sqrt(5)
negative_witness = s.simplify((v.T*HJ*v)[0])
assert negative_witness == -s.Rational(1, 3)

n = s.symbols("n", integer=True, positive=True)
A = s.diag(3*n, n)
B = s.exp(-s.sqrt(n))*X
commutator_checks = []
current = B
for k in range(11):
    target = s.exp(-s.sqrt(n))*s.Matrix([[0, (2*n)**k], [(-2*n)**k, 0]])
    residual = (current-target).applyfunc(s.simplify)
    assert residual == s.zeros(2)
    commutator_checks.append(k)
    current = A*current-current*A

q, u = s.symbols("q u", positive=True)
geometric_product = s.cancel((1-q*s.exp(u))/(1-q)*(1-q)/(1-q*s.exp(u)))
assert geometric_product == 1

C = Z+s.I*X
assert C*C == s.zeros(2)
assert Z-C*s.Rational(1, 2)-C.conjugate().T*s.Rational(1, 2) == s.zeros(2)

mp.mp.dps = 80
numerics = []
tilt = mp.mpf("0.1")
for index in [10, 100, 1000, 10000]:
    xx = tilt*index
    log_bound = (-2*mp.sqrt(index)+mp.log(mp.sinh(2*xx)-2*xx)
                 -mp.log(2)-2*mp.log(index)-2*mp.log(tilt))
    numerics.append({"n":index, "s":"0.1", "log_variance_lower_bound":mp.nstr(log_bound, 40)})

result = {
    "status":"PASS exact identities and bounded numerical diagnostics",
    "scope":"No theorem-level formal proof or external verification; asymptotic divergence is proved in PROOFS.txt.",
    "exact_pauli_covariance_identity":str(covariance_residual),
    "negative_mh_witness":str(negative_witness),
    "commutator_entry_orders_checked":commutator_checks,
    "geometric_domain_counterexample_transform_product":str(geometric_product),
    "holomorphic_transfer_counterexample_C_squared":str(C*C),
    "block_diagnostics":numerics,
    "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(BASE/"CHECKS.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!="block_diagnostics"},indent=2))
