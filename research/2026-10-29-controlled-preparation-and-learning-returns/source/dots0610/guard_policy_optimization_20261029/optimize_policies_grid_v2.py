"""Predeclared finite policy grid, actual stationary retained-memory CP maps.
Source-known benchmark, not an acquired optimal controller.
"""
import numpy as np,json,math,itertools
from fractions import Fraction
from pathlib import Path
p=Path(__file__).parent;a=np.load(p/'reviewed_fixture_arrays.npz');match=np.load(p/'matching_memory_maps.npz');sigma=a['sigma'].reshape(-1);tr=np.array([1,0,0,1]);service=a['good']+a['bad']
P=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
def superof(fun):return np.stack([fun(z.reshape(2,2)).reshape(-1) for z in np.eye(4)],axis=1)
def effect(T):return (T.conj().T@tr).reshape(2,2)
# Predeclared complementary bases X and Z; no data-dependent choice of basis pair.
states=[]
for axis in [1,3]:
 _,V=np.linalg.eigh(P[axis]);states.extend(V.T)
M=[]
for fail in [False,True]:
 Bs=[]
 for psi in states:
  other=np.array([-psi[1].conjugate(),psi[0].conjugate()]);outket=other if fail else psi
  sourceout=a['Ugood']@np.kron((a['E']@psi).reshape(16,1),np.eye(2))
  for A in a['Ds']:Bs.append(np.kron(outket.conj().reshape(1,2),np.eye(2))@np.kron(A,np.eye(2))@sourceout/2)
 M.append(superof(lambda sig:sum(B@sig@B.conj().T for B in Bs)))
assert np.linalg.norm(effect(M[0]+M[1])-np.eye(2))<1e-12
assert np.linalg.eigvalsh(2*effect(M[1])-effect(a['bad'])).min()>-1e-12
families=[('matching',Fraction(2),match['pass_map'],match['fail_map']),('weighted_exact',Fraction(3),a['weighted_pass'],a['weighted_fail']),('six_state',Fraction(3,2),a['two_pass'],a['two_fail']),('two_MUB_XZ',Fraction(2),M[0],M[1])]
np.savez(p/'two_MUB_XZ_maps.npz',pass_map=M[0],fail_map=M[1])
# NB bad-before-(b+1)-test-fail tail. Exact integer computation, no float threshold.
def tail(t,b,R):
 r,q=R.numerator,R.denominator;N=t+b+1
 num=sum(math.comb(N,j)*q**j*r**(N-j) for j in range(b+1));den=(q+r)**N
 return Fraction(num,den)
def radius(b,R):
 t=0
 while tail(t,b,R)>Fraction(1,128):t+=1
 return t

def embedded(tp,tf,s,J,b):
 G=np.linalg.inv(np.eye(4)-(1-s)*tp);S=s*service@G;F=(1-s)*tf@G
 state=np.zeros((J+1,b+1,4),complex);state[0,0]=sigma;acc=np.zeros(4,complex);abort=np.zeros(4,complex);calls=0.
 for j in range(J):
  for f in range(b+1):
   v=state[j,f];calls+=float((tr@G@v).real);sv=S@v;fv=F@v
   if j+1==J:acc+=sv
   else:state[j+1,f]+=sv
   if f==b:abort+=fv
   else:state[j,f+1]+=fv
 A=float((tr@acc).real);Ab=float((tr@abort).real);assert abs(A+Ab-1)<2e-8
 return A,calls,Ab
rows=[]
from embedded_chain import evaluate_fast
def embedded(tp,tf,s,J,b):
 r=evaluate_fast(tp,tf,service,sigma,s,J,b);return r['uncapped_acceptance'],r['uncapped_expected_calls'],r['test_failure_abort_probability']
Rs=[Fraction(1,4),Fraction(1,2),Fraction(1),Fraction(2),Fraction(4),Fraction(8),Fraction(16),Fraction(32),Fraction(64)];bs=[0,1,2,4,8];Bs=[31,63,127,255,511,1023,2047]
for name,C,tp,tf in families:
 for R,b,B in itertools.product(Rs,bs,Bs):
  t=radius(b,R)
  if B<4*t+1:continue
  h=(B+1).bit_length()-1;assert 2**h-1==B
  J=h*B;payload=h*(B-4*t);sf=R/(C+R);s=float(sf);A,E,Ab=embedded(tp,tf,s,J,b)
  # Exact rational cap ensures cap*s >= 2J+256 >=2J.
  cap=math.ceil(Fraction(2*J+256)/sf);caperr=math.exp(max(-float(cap*sf)/8,-700.));tailcost=caperr/(-math.expm1(-s/8))
  tailval=tail(t,b,R);lower=payload*max(0,A-caperr)/E;upper=payload*A/(E-tailcost)
  rows.append({'test':name,'C':str(C),'R':str(R),'b':b,'t':t,'NB_tail_exact':str(tailval),'s':str(sf),'B':B,'h':h,'J':J,'payload_qubits':payload,'cap_native_calls':cap,'uncapped_acceptance':A,'uncapped_expected_calls':E,'test_failure_abort_probability':Ab,'finite_cap_log_upper_bound':-float(cap*sf)/8,'finite_cap_loss_upper_bound':caperr,'expected_calls_truncation_upper_bound':tailcost,'finite_guard_payload_per_call_lower':lower,'finite_guard_payload_per_call_upper':upper,'single_training_plus_guard_payload_per_call_lower':payload*max(0,A-caperr)/(1000000+E)})
winners={name:max([x for x in rows if x['test']==name],key=lambda x:x['finite_guard_payload_per_call_lower']) for name,*_ in families}
out={'status':'new benchmark pending independent review','source':'same learned n4 candidate and final retained bath; same fixed U0; conditional on one million-shot learning history','grid':{'R':[str(x) for x in Rs],'b':bs,'B':Bs,'tail_target':'1/128','cap_rule':'ceil((2J+256)/s)'},'policy_count':len(rows),'two_MUB_effect_slack_min':float(np.linalg.eigvalsh(2*effect(M[1])-effect(a['bad'])).min()),'winners_guard_throughput':winners,'all_policies':rows,'scope':'Actual CP retained-memory embedded chain, with analytic finite-cap truncation bounds; floating probabilities not interval-certified. Grid is source-known benchmark selection, not physically learned optimal policy. All controls/routing/storage excluded from native-call score; each operation still pays trusted buffers and outer code.'}
(p/'policy_grid_v2.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'policy_count':len(rows),'winners':winners},indent=2))
