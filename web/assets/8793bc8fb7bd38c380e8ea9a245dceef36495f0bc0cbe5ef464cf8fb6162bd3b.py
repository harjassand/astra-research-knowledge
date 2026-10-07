"""Independent finite rational confidence certificate for the executed sampler.

The 24-state certificate does not depend on the imported all-size gap theorem.
It proves this finite matrix's Poincare bound, not the general XXZ algorithm.
"""
from fractions import Fraction as F
from pathlib import Path
import json

from xxz_quadratic_gates import compile_quadratic_trace
from xxz_local_chain import LocalExchange, enumerate_supports, product_fraction


gates = [("edge", (0,1), F(1,80), F(1), F(1,2))]
instance = compile_quadratic_trace(2, gates)
t = F(1,4096)
states = enumerate_supports(instance)
rows, weights = {}, {}
for state in states:
    chain = LocalExchange(instance, t=t, state=state)
    rows[state] = chain.kernel_row()
    weights[state] = chain.supported_weight()
    assert min(rows[state].values()) >= 0 and sum(rows[state].values(), F(0)) == 1
Z = sum(weights.values(), F(0))
pi = [weights[state]/Z for state in states]
for state,row in rows.items():
    for target,p in row.items():
        assert weights[state]*p == weights[target]*rows[target].get(state,F(0))
gap = t/(2*instance.n)
A = []
for i,state in enumerate(states):
    row = []
    for j,target in enumerate(states):
        identity = int(i==j)
        row.append(pi[i]*(identity-rows[state].get(target,F(0))) -
                   gap*(identity*pi[i]-pi[i]*pi[j]))
    A.append(row)
pivots = []
for k in range(len(A)):
    pivot = A[k][k]
    assert pivot >= 0
    pivots.append(str(pivot))
    if pivot == 0:
        assert all(A[k][j] == 0 for j in range(k+1,len(A)))
        continue
    for i in range(k+1,len(A)):
        for j in range(i,len(A)):
            A[i][j] -= A[i][k]*A[k][j]/pivot
            A[j][i] = A[i][j]
phard = sum((pi[i] for i,state in enumerate(states) if state[0].isdisjoint(state[1])),F(0))
assert phard >= F(3,4)
R = product_fraction(max(f.table.values())/min(f.table.values()) for f in instance.factors)
assert min(pi) >= t**2/(4**4*R)
out = {"status":"EXACT_FINITE_CONFIDENCE_CERTIFICATE","states":len(states),
       "discrete_gap_lower_bound":str(gap),"psd_pivots":pivots,
       "hard_probability":str(phard),"stationary_min":str(min(pi)),
       "coarse_stationary_min_lower_bound":str(t**2/(4**4*R)),
       "independent_of_imported_general_gap":True,
       "scope":"This executed 24-state instance only. Confidence also assumes independent fair input bits; recorded seed is pseudorandom replay, not an entropy certificate."}
Path(__file__).with_name("executed_sampler_certificate.json").write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='psd_pivots'},indent=2))
