"""Re-evaluate frozen policy parameters for the different full-field B=2048 code."""
import sys,json,numpy as np
from pathlib import Path
from fractions import Fraction
p=Path(__file__).parent;dep=p.parent/'guard_policy_optimization_20261029';sys.path.insert(0,str(dep))
from embedded_chain import evaluate_fast,finite_bounds,nb_tail
w=json.load(open(dep/'policy_grid_v2.json'))['winners_guard_throughput'];a=np.load(dep/'reviewed_fixture_arrays.npz');ma=np.load(dep/'matching_memory_maps.npz');mu=np.load(dep/'two_MUB_XZ_maps.npz');maps={'six_state':(a['two_pass'],a['two_fail']),'matching':(ma['pass_map'],ma['fail_map']),'weighted_exact':(a['weighted_pass'],a['weighted_fail']),'two_MUB_XZ':(mu['pass_map'],mu['fail_map'])};rows=[]
for name,pol in w.items():
 B=2048;h=11;J=B*h;t=pol['t'];payload=h*(B-4*t);sf=Fraction(pol['s']);tp,tf=maps[name];r=evaluate_fast(tp,tf,a['good']+a['bad'],a['sigma'],float(sf),J,pol['b']);bounds=finite_bounds(r['uncapped_acceptance'],r['uncapped_expected_calls'],sf,J,payload)
 tr=0
 while nb_tail(tr,pol['b'],Fraction(pol['R']))>Fraction(1,256):tr+=1
 rows.append({'test':name,'R':pol['R'],'s':pol['s'],'b':pol['b'],'t_guard_1_over128':t,'B':B,'h':h,'J':J,'payload_qubits':payload,**r,**bounds,'radius_for_guard_1_over256_same_policy':tr,'payload_for_guard_1_over256':h*(B-4*tr)})
out={'scope':'Nearby different full-field code, frozen R,b policies from B2047 grid; no optimization rerun or identical-fixture claim. Source-known conditional mathematical CP evaluation.','rows':rows,'CNOTs_encoder_plus_inverse_decoder':2*651264,'illustrative_CNOT_halfdiamond_budget':str(Fraction(1,256)),'sufficient_per_CNOT_halfdiamond_for_that_budget':float(Fraction(1,256)/(2*651264)),'budget_warning':'Guard1/128 plus CNOT1/256 yields3/256 before all other errors. To targettotal1/128, retune guard and reserve all other control/storage budgets. This is a sufficient worst-case composable hybrid budget, not a necessary threshold or achieved hardware calibration.'};(p/'nearby_B2048_policies.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
