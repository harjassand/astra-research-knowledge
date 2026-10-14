#!/usr/bin/env python3
"""Exact check that the finite-width potential does not extend unchanged."""
from fractions import Fraction as Q
from pathlib import Path
import json,sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'incoming_resonant'))
from profile_algebra import edge_coeffs,edge_value,poly_terms
from search_exact_cycles import energy

lam=Q(11,100); n,m=1,-1
vertices=[(Q(i,4),Q(j,4)) for i in range(9) for j in range(9)]
record=json.loads((ROOT/'exact_cycle_search_11_100.json').read_text())[0]
P=[Q(v) for v in record['potential']]
start=(Q(1),Q(2)); end=(Q(2),Q(1))
co=edge_coeffs(poly_terms(energy(n,m,lam)[0]),start,end)
idx=vertices.index(start); jdx=vertices.index(end)
potential_difference=P[jdx]-P[idx]
widths=[Q(1,8),Q(1,4),Q(1,2),Q(1),Q(2),Q(4,7)]
rows=[]
for tau in widths:
    action=edge_value(co,tau)
    rows.append({'width':str(tau),'raw_strip_action':str(action),
                 'potential_difference_Pend_minus_Pstart':str(potential_difference),
                 'slack_action_minus_potential_difference':str(action-potential_difference),
                 'is_in_certified_finite_width_set':tau in widths[:-1]})
assert all(Q(row['slack_action_minus_potential_difference'])>=0 for row in rows[:-1])
assert Q(rows[-1]['slack_action_minus_potential_difference'])<0
out={
 'status':'EXACT PASS',
 'claim':'This particular potential from the five-width graph fails to extend to every positive width.',
 'scope_limit':'The failure does not imply a negative closed walk, or rule out another all-width potential.',
 'integrand':'Fstar-(11/100)q^2','carriers':[n,m],
 'from':list(map(str,start)),'to':list(map(str,end)),
 'potential_difference':str(potential_difference),'edge_coefficients_tau_powers_1_minus_j':[str(v) for v in co],
 'width_checks':rows,
 'continuous_numeric_cycle_search':'No negative cycle found; discovery only, not exact certification.'
}
(ROOT/'width_quantifier_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
