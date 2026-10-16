#!/usr/bin/env python3
"""Exact identities supporting the exposure-certificate analytic audit."""
import json
from pathlib import Path
import sympy as S

L,a,tau,u = S.symbols("L a tau u",positive=True)
c = a/(L+2)
potential = c*(2-S.exp(-u)-S.exp(-(L-u))+S.exp(-u)+S.exp(-(L-u)))
assert S.simplify(potential-2*c) == 0
assert S.simplify(c*(L+2)-a) == 0
assert S.simplify(2*c*a-2*a*a/(L+2)) == 0
endtime = tau/(L+2)
middle = tau-2*endtime
rate = (L+2)/tau
assert S.simplify(rate*middle-L) == 0
assert S.simplify((a/tau)*endtime-c) == 0
assert S.simplify((a/tau)/rate-c) == 0
N = S.symbols("N",integer=True,nonnegative=True)
comparison_gap = S.factor(2*a*a/(N+2)-a*a/(N+1))
assert S.simplify(comparison_gap-a*a*N/((N+1)*(N+2))) == 0
g = L-2+(L+2)*S.exp(-L)
assert S.simplify(S.diff(g,L)-(1-(L+1)*S.exp(-L))) == 0
assert S.limit(g,L,0) == 0

# A finite rational kernel provides an independent strict-positivity check.
# Points at multiples of log(2) give K_ij=2^(-|i-j|).
K = S.Matrix(5,5,lambda i,j:S.Rational(1,2)**abs(i-j))
assert all(K[:n,:n].det() > 0 for n in range(1,6))
ones = S.ones(5,1)
w = K.inv()*ones
w /= (ones.T*w)[0]
assert w == S.Matrix([S.Rational(2,7),S.Rational(1,7),S.Rational(1,7),S.Rational(1,7),S.Rational(2,7)])
assert w.T*K*w == S.Matrix([[S.Rational(3,7)]])
assert K*w == S.Rational(3,7)*ones

result = {
    "constant_potential":"2a/(L+2)",
    "measure_optimum":"2a^2/(L+2)",
    "endpoint_time":"tau/(L+2)",
    "middle_intensity":"(L+2)/tau",
    "poisson_minus_deterministic_at_L_N":str(comparison_gap),
    "rational_five_point_optimal_weights":[str(v) for v in w],
    "rational_five_point_optimal_energy":"3/7",
    "status":"PASS: exact potential, mass, realization, comparator, derivative, and positive-kernel identities",
    "scope":"Finite identities support the analytic proof; no physical lower bound, device test, or priority claim."
}
Path(__file__).with_name("exposure_optimum_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
