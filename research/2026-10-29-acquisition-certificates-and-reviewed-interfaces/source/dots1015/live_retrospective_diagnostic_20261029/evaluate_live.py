"""Retrospective arithmetic only; three-role simulation has no outer code."""
import sys,json,hashlib
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,'producer-workspace/acquisition_only_quantum_certificate_20261029')
from exact_data_certificate import root_upper,empirical_score
p=Path('producer-workspace/bounded_live_three_role_result.json');j=json.loads(p.read_text())
T=j['T'];m=3;d=35;L=720;prob=F(j['p']);R=F(j['perturbation_radius']);M=2**j['perturbation_bits_per_coordinate'];N=j['shared_probe_count']
assert not j['verified_outer_code_deployed'] and not j['unknown_payload_transmitted']
assert sum(j['roles'].values())==T and N==j['roles']['learn']
edges=[dict(quaternion=j['retrospective_candidates'][i]['quaternion'],coefficients=list(zip(j['feedback_exponents'],j['final_feedback'][i]))) for i in range(m)]
score=empirical_score(edges,N,prob);assert score==F(j['retrospective_empirical_score'])
E=sum(F(c['certified_gap_sum_upper']) for c in j['reported_gap_counters']);V=sum(F(v) for v in j['observed_squared_feedback_per_edge'])
analytical_B=(T-1)*L/prob+d*R;B=max(F(c['public_per_query_cap']) for c in j['reported_gap_counters']);assert B>=analytical_B
# Pointwise source certificates are independently received elsewhere; verify counters exactly against their gap entries.
for i in range(m):
 true=sum(F(rows[i]['certificate']['gap']) for rows in j['oracle_calls']);c=j['reported_gap_counters'][i];assert true<=F(c['certified_gap_sum_upper'])<=true+F(c['maximum_total_rounding_excess'])
results=[]
for k in [1,5,10,20]:
 U=2*E+2*m*B*k
 terms={'potential_width':F(m*d,4)*R,'observed_stability':V/(4*R),'solver_and_midpoint_bias':L*root_upper(F(m*T,R)*U+F(m*m*d*T*T,M)),'action_martingale':m*(1+F(45,2*prob))*root_upper(2*T*k)}
 bound=max(F(0),score+sum(terms.values()))
 results.append(dict(failure_exponent_per_event=k,loss_bound_exact=str(bound),loss_bound_float=float(bound),components={a:float(b) for a,b in terms.items()},realized_gap_contribution_without_predictable_penalty=float(L*root_upper(F(m*T,R)*2*E+F(m*m*d*T*T,M))),scope='Last contribution is decomposition only, NOT a valid replacement bound.'))
out=dict(source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),T=T,role_counts=j['roles'],empirical_score_exact=str(score),empirical_score=float(score),reported_total_gap=str(E),feedback_square_sum=str(V),public_gap_cap=str(B),evaluations=results,readiness_pass=False,reason='No verified outer code or payload; all bounds also exceed trivial star loss maximum mT=360. Three-role trajectory is not the new two-role protocol.',scope='Actual simulated learning-bank diagnostic. Exact rational counter evaluation; source propagation itself remains floating simulation.')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
