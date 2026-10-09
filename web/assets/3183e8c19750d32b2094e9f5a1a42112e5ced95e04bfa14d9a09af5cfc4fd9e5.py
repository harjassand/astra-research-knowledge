#!/usr/bin/env python3
"""Exact rational-function check of all entries; no PSD scan."""
import hashlib
import json
import pathlib
import time
import sympy as sp

started = time.perf_counter()
r, v = sp.symbols("r v", positive=True)
alpha, beta, kappa = sp.symbols("alpha beta kappa", real=True)
A, B = (r+1/r)/2, (r-1/r)/2
c, h = (r*r+r**-2)/2, (r*r-r**-2)/2
C, H = (v*v+v**-2)/2, (v*v-v**-2)/2
m, n = 2*beta*H/C, 1-1/C
dalpha = 2*alpha*h/c-kappa*(1-1/c)
P = h*beta+(alpha*c-kappa*h/2)*H/C
Q = 2*B*beta+(alpha-kappa*B)/A*H/C
M = sp.Matrix([[A*A*m-kappa*n+B*B*dalpha, -P, A*m-kappa*n],
               [-P, B*B*m+A*A*dalpha, -Q],
               [A*m-kappa*n, -Q, m-kappa*n]])
S = sp.Matrix([[1, 1, 0], [1, -1, 0], [0, 0, 1]])
nodes = [beta-alpha, beta+alpha, beta]
half_exponentials = [v/r, v*r, v]

def hyperbolic_kernel(i, j):
    x, y = nodes[i], nodes[j]
    e, f = half_exponentials[i], half_exponentials[j]
    sx, sy = (e*e-e**-2)/2, (f*f-f**-2)/2
    sx2, sy2 = (e-1/e)/2, (f-1/f)/2
    denominator = e/f+f/e
    return (x*sy+y*sx-2*kappa*sx2*sy2)/denominator

G = sp.Matrix(3, 3, hyperbolic_kernel)
diff = C*S.T*M*S/2-G
checks = []
for i in range(3):
    for j in range(3):
        numerator = sp.together(diff[i, j]).as_numer_denom()[0]
        assert sp.expand(numerator) == 0, (i, j)
        checks.append(f"generic congruence entry {i},{j}")
assert S.det() == -2
checks.append("congruence invertible determinant -2")
root = pathlib.Path(__file__).resolve().parent
result = {"status": "PASS", "checks": len(checks), "check_names": checks,
          "purpose": "generic exact factorization, arbitrary real alpha,beta,kappa with r=e^(alpha/2), v=e^(beta/2)",
          "elapsed_seconds": time.perf_counter()-started,
          "sympy_version": sp.__version__,
          "invocation": "python3 work/agents/tensor_frame_sol/cycle08_complete_qubit/check_three_point_congruence.py",
          "script_sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
(root/"three_point_congruence_checks.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({k: result[k] for k in ["status", "checks", "elapsed_seconds"]}))
