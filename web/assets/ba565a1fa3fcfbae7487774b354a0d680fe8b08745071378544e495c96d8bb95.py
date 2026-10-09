"""Exact symbolic replay of the three-node matrix identity, without scans.

The analytic PSD proof is in INDEPENDENT_BASELINE.txt. This optional replay
uses SymPy; it verifies identities, not Hardy positivity or the supplied
physical spectral reduction. a=exp(alpha/2), b=exp(beta/2) are left symbolic.
"""
from pathlib import Path
import json
import sympy as sp

a, b = sp.symbols("exp_alpha_half exp_beta_half", positive=True)
alpha, beta, lam = sp.symbols("alpha beta lambda", real=True)
A, B = (a+1/a)/2, (a-1/a)/2
C, S = (a*a+1/(a*a))/2, (a*a-1/(a*a))/2
Hb, Sb = (b*b+1/(b*b))/2, (b*b-1/(b*b))/2


def sinh_exp_half(value):
    return (value-1/value)/2


def sinh_exp(value):
    return (value*value-1/(value*value))/2


def cosh_exp(value):
    return (value*value+1/(value*value))/2


def diagonal_node(node, exp_half):
    return node*sinh_exp(exp_half)-lam*(cosh_exp(exp_half)-1)


def kernel(node1, exp1, node2, exp2, difference_cosh):
    numerator = (node1*sinh_exp(exp2)+node2*sinh_exp(exp1)
                 -4*lam*sinh_exp_half(exp1)*sinh_exp_half(exp2))
    return numerator/(2*difference_cosh)


u, v, w = beta+alpha, beta-alpha, beta
eu, ev, ew = a*b, b/a, b
ku, kv, kw = [diagonal_node(node, e) for node, e in [(u, eu), (v, ev), (w, ew)]]
kuv = kernel(u, eu, v, ev, C)
kuw = kernel(u, eu, w, ew, A)
kvw = kernel(v, ev, w, ew, A)
gram = sp.Matrix([[ku, kuv, kuw], [kuv, kv, kvw], [kuw, kvw, kw]])
T = sp.Matrix([[sp.Rational(1, 2), sp.Rational(-1, 2), 0],
               [sp.Rational(1, 2), sp.Rational(1, 2), 0], [0, 0, 1]])

m_beta, n_beta = 2*beta*Sb/Hb, 1-1/Hb
d_alpha, d_beta = 2*(alpha*S-lam*(C-1))/C, 2*kw/Hb
P = S*beta+(alpha*C-lam*S)*Sb/Hb
Q = 2*B*beta+(alpha-2*lam*B)*Sb/(A*Hb)
M = sp.Matrix([[A*A*m_beta-2*lam*n_beta+B*B*d_alpha, -P,
                A*m_beta-2*lam*n_beta],
               [-P, B*B*m_beta+A*A*d_alpha, -Q],
               [A*m_beta-2*lam*n_beta, -Q, d_beta]])
difference = Hb*M/2-T.T*gram*T
checks = {}
for i in range(3):
    for j in range(i, 3):
        residual = sp.cancel(difference[i, j])
        if residual != 0:
            raise AssertionError((i, j, residual))
        checks[f"entry_{i+1}{j+1}"] = "EXACT_ZERO"
assert T.det() == sp.Rational(1, 2)
checks["T_determinant"] = "EXACT_ONE_HALF"

result = {
    "status": "PASS_EXACT_SYMBOLIC_CONGRUENCE",
    "checks": checks,
    "sympy_version": sp.__version__,
    "symbolic_domain": "Independent alpha,beta,lambda and positive exp_alpha_half,exp_beta_half; physical exponential substitutions are a specialization.",
    "scope": "Universal matrix identity only. Hardy positivity is analytic and the physical spectral reduction is supplied separately.",
    "external_validation": False,
    "formal_verification": False,
}
Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"status": result["status"], "exact_checks": len(checks)}, indent=2))
