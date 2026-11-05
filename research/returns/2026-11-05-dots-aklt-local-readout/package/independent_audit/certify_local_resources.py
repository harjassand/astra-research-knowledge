# Portable audit copy: only ROOT below differs from the preserved original.
"""Rational first moments and a branching-MGF resource certificate."""
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np

B=F('0.523943909811')+F('1.690182152836')+F('0.046531016280')
q=F('0.907806'); vmin=F('0.711122124'); amin=F('3.749901596')
lam=F(66455976045001,166988328468480)
length=B/(vmin*(1-q));count=B/(amin*(1-q));proposals=lam*(1+length)
assert length<F('34.481635') and count<F('6.539013') and proposals<F('14.120548')

# c < log(1+10^-6), proved using log(1+x)>=x/(1+x).
c=F(9,10**7);s=t=F(1,10**8)
assert c<F(1,1000001)
# exp(t)<=1/(1-t). All three resource terms are checked rationally.
rhs=s+(lam/vmin)*t/(1-t)+c*q/(1-t)
assert rhs<c
H=lam*t/(1-t)+c*B/(1-t)
assert H<F('0.000002039')
rho=F(709007,750000)
assert H<1-rho
R=1/(1-H)
assert R*rho<1
# Check the deliberately loose global Doob prefactor exactly.
ROOT=Path(__file__).resolve().parents[1]
vv=np.load(ROOT/'square_aklt_loop_audit_20261105/trail_certificate_m6.npz')['v']
gg=np.load(ROOT/'square_aklt_boundary_operation_20261105/torus_green_m6_L16.npz')['q']
global_doob=F(int(gg.max())*int(vv.max()),int(gg.min())*int(vv.min()))
assert global_doob<421
source_mgf=R**7*(1+(R-1)*421*rho/(1-R*rho))
def pair(x):return {'exact':str(x),'decimal':float(x)}
out={
 'source': 'SHORT_TAIL_GREEN_THEOREM.md, certified_geometry_m10_L32.json, short_tail_exact_certificate.json',
 'root_length_mass_per_query_vertex_upper':pair(B),
 'type_weighted_kernel_q_upper':pair(q),'minimum_weight_per_edge':pair(vmin),
 'minimum_weight_per_loop':pair(amin),'proposal_rate_per_query_vertex':pair(lam),
 'expected_total_clan_length_per_query_vertex_upper':pair(length),
 'expected_clan_count_per_query_vertex_upper':pair(count),
 'expected_all_oracle_proposals_per_query_vertex_upper':pair(proposals),
 'joint_mgf':{'c':pair(c),'s':pair(s),'t':pair(t),
              'supersolution_left_side_per_a':pair(rhs),'strict_margin':pair(c-rhs),
              'log_mgf_upper_per_query_vertex':pair(H),
              'statement':'E exp(s A + t P) <= exp(H |K|), where A sums type weights of all retained clan cylinders and P counts every seed and parent oracle proposal, including nulls. The proof uses the discovery forest, not the all-order connected derivative lemma.'},
 'random_source_path_join':{'continuation_tail_ratio':pair(rho),
                           'uniform_doob_prefactor_upper_checked_below_421':pair(global_doob),
                           'comparison_margin_1_minus_rho_minus_H':pair(1-rho-H),
                           'upper_exp_H_times_rho':pair(R*rho),
                           'unconditional_joint_mgf_upper':pair(source_mgf),
                           'statement':'For a path query K with |K|<=6+T+1 and Pr(T>=n)<=421 rho^n, E exp(H |K|) is bounded by the displayed rational. Thus the physical attempt retains a positive proposal-count exponential moment.'},
 'scope':'Uniform over finite query sets on Z^2 and open finite boxes. Expected oracle calls and finite moments of history scans; not an expected bit-complexity or wall-time bound.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
