import json,numpy as np
from pathlib import Path
from fractions import Fraction
from embedded_chain import evaluate_fast,nb_tail
p=Path(__file__).parent;a=np.load(p/'reviewed_fixture_arrays.npz');ma=np.load(p/'matching_memory_maps.npz');mu=np.load(p/'two_MUB_XZ_maps.npz');maps={'six_state':(a['two_pass'],a['two_fail']),'matching':(ma['pass_map'],ma['fail_map']),'weighted_exact':(a['weighted_pass'],a['weighted_fail']),'two_MUB_XZ':(mu['pass_map'],mu['fail_map'])}
x=json.load(open(p/'policy_grid_v1.json'));errs=[]
for name,r in x['winners_guard_throughput'].items():
 tp,tf=maps[name];z=evaluate_fast(tp,tf,a['good']+a['bad'],a['sigma'],float(Fraction(r['s'])),r['J'],r['b']);errs.append({'test':name,'acceptance_error':abs(z['uncapped_acceptance']-r['uncapped_acceptance']),'expected_calls_error':abs(z['uncapped_expected_calls']-r['uncapped_expected_calls'])})
assert max(e['expected_calls_error'] for e in errs)<1e-7
checked=0
for r in json.load(open(p/'policy_grid_v2.json'))['all_policies']:
 R=Fraction(r['R']);C=Fraction(r['C']);s=Fraction(r['s']);t=r['t'];b=r['b'];assert R==C*s/(1-s)
 assert nb_tail(t,b,R)==Fraction(r['NB_tail_exact'])<=Fraction(1,128)
 assert t==0 or nb_tail(t-1,b,R)>Fraction(1,128)
 assert r['B']>=4*t+1 and r['J']==r['h']*r['B'] and r['payload_qubits']==r['h']*(r['B']-4*t)
 assert r['cap_native_calls']*s>=2*r['J']+256;assert r['finite_cap_loss_upper_bound']>0
 checked+=1
chois=[]
for name,(tp,tf) in maps.items():
 for typ,T in [('pass',tp),('fail',tf)]:
  J=T.reshape(2,2,2,2).transpose(0,2,1,3).reshape(4,4);v=float(np.linalg.eigvalsh(J).min());assert v>-1e-12 and np.linalg.norm(J-J.conj().T)<1e-12;chois.append({'test':name,'outcome':typ,'min_choi_eigenvalue':v})
out={'fast_vs_direct':errs,'exact_policy_checks':checked,'complete_test_CP_checks':chois};(p/'verify_policy_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
