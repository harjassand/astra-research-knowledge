"""Exact, bounded verification of implementation interfaces, not novelty evidence."""
import json,time,platform,random
from pathlib import Path
from fractions import Fraction as F
from math import comb
from compiler import compile_channels
from verify_certificate import verify
from runtime import Replacement,Table,binomial_tail,budget_for_error,BudgetExceeded
root=Path(__file__).resolve().parent
started=time.perf_counter();cpu=time.process_time();checks={}
cert=json.loads((root/'NONDEGRADED_COMPILED.json').read_text());verify(cert)
K=[[F(v) for v in row] for row in cert['K']];L=[[F(v) for v in row] for row in cert['L']];U=[[F(v) for v in row] for row in cert['U']]
D=[[F(v) for v in row] for row in cert['checked']['residual']];qx=list(map(F,cert['checked']['q_by_input']));q=F(cert['q'])
checks['one_step_rational_identity']=all(sum(U[y][z]*L[z][x] for z in range(3))+D[y][x]==K[y][x] for y in range(3) for x in range(3))
# Enumerate the full causal law for a controller that uses ONLY past Y.
# This verifies the implementation's branch normalization with changing inputs.
T=4;state={((),0):F(1)};ideal={():F(1)}
for t in range(T):
    nxt={};ni={}
    for (hist,n),mass in state.items():
        x=(t+sum((j+1)*y for j,y in enumerate(hist)))%3
        for z in range(3):
            r=1-sum(U[y][z] for y in range(3))
            for y in range(3):
                key=(hist+(y,),n);nxt[key]=nxt.get(key,F(0))+mass*L[z][x]*U[y][z]
                if qx[x]:
                    key=(hist+(y,),n+1);nxt[key]=nxt.get(key,F(0))+mass*L[z][x]*r*D[y][x]/qx[x]
    for hist,mass in ideal.items():
        x=(t+sum((j+1)*y for j,y in enumerate(hist)))%3
        for y in range(3):ni[hist+(y,)]=mass*K[y][x]
    state=nxt;ideal=ni
assert sum(state.values())==1
assert all(sum(state.get((hist,n),0) for n in range(T+1))==prob for hist,prob in ideal.items())
checks['four_step_feedback_record_law_exact']=True
for B in range(-1,T+1):
    actual=sum(m for (_,n),m in state.items() if n>B)
    # Here q(z) is constant, so the binomial upper bound is equality for EVERY controller.
    assert actual==binomial_tail(T,q,B)
checks['feedback_cost_tail_exact']=True
for tt in range(8):
    for b in range(-1,tt+1):
        brute=sum((F(comb(tt,k))*q**k*(1-q)**(tt-k) for k in range(max(b+1,0),tt+1)),F(0))
        assert binomial_tail(tt,q,b)==brute
checks['tail_recurrence_exact']=True
# An adversarial callback fails if a no-read branch accidentally accesses raw X.
class FixedRng:
    def __init__(self,n):self.n=n
    def getrandbits(self,k):return self.n if k else 0
module=Replacement(cert,FixedRng(0));called=[]
y,cost=module.step(1,lambda:called.append(True) or 0)
assert not cost and not called
checks['no_read_callback_isolation']=True
# Force a query branch, and ensure hard budget aborts before touching X.
module=Replacement(cert,FixedRng(module.branch[0].den-1),budget=0)
try:module.step(0,lambda:called.append(True) or 0)
except BudgetExceeded:pass
else:raise AssertionError('budget did not abort')
assert not called;checks['budget_abort_precedes_raw_access']=True
module=Replacement(cert,FixedRng(module.branch[0].den-1));called=[]
y,cost=module.step(0,lambda:called.append(True) or 0)
assert cost and called==[True] and module.reads==1 and D[y][0]==qx[0]
checks['queried_callback_and_residual_output']=True
# Verify q=0 and q=1 endpoint acquisition, not additional scientific instances.
h03=json.loads((root/'H03_COMPILED.json').read_text());assert F(h03['q'])==0;verify(h03)
checks['H03_degradation_exact']=True
one=compile_channels({'id':'endpoint_q1','K':[['1','0'],['0','1']],'L':[['1','1']]})
assert F(one['q'])==1;verify(one);checks['q1_endpoint_exact']=True
# LP certificate mutations must fail independently.
bad=json.loads(json.dumps(cert));bad['q']='0'
try:verify(bad)
except AssertionError:pass
else:raise AssertionError('bad certificate accepted')
checks['bad_primal_rejected']=True
bad=json.loads(json.dumps(cert));bad['dual'][0]['weight']='0'
try:verify(bad)
except AssertionError:pass
else:raise AssertionError('bad dual accepted')
checks['bad_dual_rejected']=True
Tbudget=1000;delta=F(1,10**6);B=budget_for_error(Tbudget,q,delta);tail=binomial_tail(Tbudget,q,B)
assert tail<=delta and (B==0 or binomial_tail(Tbudget,q,B-1)>delta)
summary={'checks':checks,'adaptive_example':{'T':T,'record_count':len(ideal),'joint_cost_record_entries':len(state)},
 'charged_budget':{'T':Tbudget,'q':str(q),'target_error':str(delta),'smallest_binomial_certified_budget':B,
 'exact_tail':str(tail),'diagnostic_decimal_tail':float(tail),'mean_reads':str(Tbudget*q)},
 'verification_wall_s_including_endpoint_compile':time.perf_counter()-started,
 'verification_cpu_s_including_endpoint_compile':time.process_time()-cpu,
 'python':platform.python_version(), 'claim':'Exact arithmetic implementation checks. General adaptive and quantum-reference statements require the supplied proof. No independent audit or historical novelty inferred.'}
(root/'CHECKS.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({**summary,'charged_budget':{k:v for k,v in summary['charged_budget'].items() if k!='exact_tail'}},indent=2))
