"""One exact mixed-sign two-node check of the exposed sharpness congruence.

This checks a normalization identity, not sharpness, positivity, or an
optimized counterexample.  The general audit is analytic and separate.
"""
import json
import sympy as sp

eta = sp.Symbol("eta", real=True)
sqrt = sp.sqrt

# r=1/3, x_1=log(8), x_2=-log(27).
s0 = 8 / sqrt(46721)
sleaf = sp.Matrix([1 / sqrt(46721), 216 / sqrt(46721)])
A0 = sum(sleaf)
assert sp.simplify(s0**2 + sum(x**2 for x in sleaf) - 1) == 0
V = sp.Matrix(2, 2, lambda i, j: 2*A0/(sleaf[i]+sleaf[j]))
D = sp.diag(sp.Rational(5, 2), sp.Rational(10, 3))
C = sp.diag(7*sqrt(2)/6, 13*sqrt(3)/12)
d = sp.diag(8*sqrt(2)/3, -1/(4*sqrt(3)))
Lt = sp.Matrix([[sp.Rational(45, 16), -70*sqrt(6)/217],
                [-70*sqrt(6)/217, sp.Rational(320, 27)]])
L0 = sp.Matrix([[sp.Rational(49, 16), -sp.Rational(182, 217)],
                [-sp.Rational(182, 217), sp.Rational(338, 27)]])
direct = (D*V + V*D)/2 - eta*C*V*C
congruence = A0/(2*s0)*d*(Lt-eta*L0)*d
residual = (direct-congruence).applyfunc(sp.simplify)
assert residual == sp.zeros(2)

print(json.dumps({
    "purpose": "exact identity only; no numerical search or sharpness inference",
    "r": "1/3", "nodes": ["log(8)", "-log(27)"],
    "V": [[str(V[i,j]) for j in range(2)] for i in range(2)],
    "D": [str(D[i,i]) for i in range(2)],
    "C": [str(C[i,i]) for i in range(2)],
    "d": [str(d[i,i]) for i in range(2)],
    "prefactor": str(sp.simplify(A0/(2*s0))),
    "residual": [[str(residual[i,j]) for j in range(2)] for i in range(2)],
    "status": "PASS exact for symbolic real eta"
}, indent=2))
