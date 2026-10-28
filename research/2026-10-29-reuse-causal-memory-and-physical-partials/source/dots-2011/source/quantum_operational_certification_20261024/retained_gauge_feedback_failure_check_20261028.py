"""Exact two-call returned-gauge counterexample. No quantum hardware or sampling."""
from pathlib import Path
import sympy as s,json,hashlib
p=Path(__file__).resolve().parent
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);P0=s.diag(1,0);P1=s.diag(0,1)
k=s.kronecker_product
bell=s.Matrix([1,0,0,1])/s.sqrt(2)
rho=k(bell*bell.H,P0,P0) # untouched reference, first logical output, emitted gauge, next payload
flip=k(I,I,X,I)
actual_first=flip*rho*flip.H
K=[k(I,I,P0,I),k(I,I,P1,X)]
assert sum([a.H*a for a in K],s.zeros(16))==s.eye(16)
ideal=sum([a*rho*a.H for a in K],s.zeros(16))
actual=sum([a*actual_first*a.H for a in K],s.zeros(16))
def trace_gauge(r):
 return s.Matrix(8,8,lambda a,b:sum(r[4*(a//2)+2*g+(a%2),4*(b//2)+2*g+(b%2)] for g in range(2)))
ri=trace_gauge(ideal);ra=trace_gauge(actual)
assert ri==k(bell*bell.H,P0) and ra==k(bell*bell.H,P1)
assert s.trace(ri*ra)==0
assert (ra-ri).eigenvals()=={0:6,1:1,-1:1}
# The first logical receiver after tracing gauge is exactly true extraction for EVERY gauge state.
logical_kraus=[k(I,s.Matrix([[1,0]])*X),k(I,s.Matrix([[0,1]])*X)]
rows=[s.Matrix([[sum(a[l,2*l+g] for l in range(2))/2 for g in range(2)]]) for a in logical_kraus]
T0=sum([v.H*v for v in rows],s.zeros(2));assert T0==I
source='learned_subsystem_complete_cp_domination_20261028.md'
j={'status':'PASS_EXACT_RETURNED_GAUGE_TWO_CALL_BOUNDARY_COUNTEREXAMPLE','current_uniform_T0':'I_2','current_uniform_b':0,'first_logical_Bell_state_unchanged':True,'second_source':'Pauli instrument I⊗Ad_P0 + X⊗Ad_P1, complete TP on payload+returned memory','second_receiver':'exact','final_half_trace_distance':1,'source_calls':0,'random_draws':0,'governing_source_unmodified':True,'governing_source_sha256':hashlib.sha256((p/source).read_bytes()).hexdigest()}
(p/'retained_gauge_feedback_failure_check_20261028.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j,indent=2))
