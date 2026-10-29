"""Independent exact full-alphabet dual check of unchanged measured receiver."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,math,numpy as np
D=Path(__file__).parent;A=D.parent;Q=A.parent;P=Q/'label_observed_quantum_flag_recovery_20261028'
c=json.loads((A/'certificate_v2.json').read_text());old=json.loads((P/'results_v2.json').read_text());data=np.load(P/'training_counts_v1.npz');counts=data['counts'];mom=data['mom'];N=int(counts.sum());size=len(counts)
y=list(map(F,c['dual_Pauli_coefficients']));coeff=[]
for x in range(size):coeff.append([F(int(counts[x]),2*N)]+[F(3*int(v),2*N) for v in mom[x]])
# Every full alphabet inequality, including ALL unobserved labels independently.
min_det=None
for a in coeff:
 v=[u-w for u,w in zip(y,a)];det=v[0]*v[0]-sum(x*x for x in v[1:]);assert v[0]>=0 and det>=0
 min_det=det if min_det is None else min(min_det,det)
observed=[x for x in range(size) if counts[x]];missing=[x for x in range(size) if not counts[x]]
assert len(observed)==53 and len(missing)==203 and c['one_zero_dummy_label'] in missing
assert all(coeff[x]==[0,0,0,0] for x in missing)
chosen=sorted(sorted(range(size),key=lambda x:(-counts[x],x))[:2]);assert chosen==[0,255]==old['selected_words']
tx=F(old['projector_parameters']['tx']);ty=F(old['projector_parameters']['ty']);norm=1+tx*tx+ty*ty;v=[2*tx/norm,2*ty/norm,(1-tx*tx-ty*ty)/norm];assert sum(x*x for x in v)==1
# Pi0=(I+v·sigma)/2, Pi1=(I-v·sigma)/2.
primal=coeff[chosen[0]][0]+sum(v[j]*coeff[chosen[0]][j+1] for j in range(3))+coeff[chosen[1]][0]-sum(v[j]*coeff[chosen[1]][j+1] for j in range(3));dual=2*y[0];gap=dual-primal
assert primal==F(c['certified_empirical_primal']) and dual==F(c['certified_empirical_dual']) and gap==F(c['empirical_gap']) and gap>=0
sqrt3upper=F(173206,100000);assert sqrt3upper**2>3
opdelta=(F(1,500)+sqrt3upper*F(1,200))/2;regret=4*opdelta+gap
assert opdelta==F(c['uniform_operator_error_upper']) and regret==F(c['full_CPTP_oracle_regret_upper'])
failure=2*size*math.exp(-2*N*float(F(1,500))**2)+6*size*math.exp(-N*float(F(1,200))**2/(6+F(8,3)*F(1,200)))
assert abs(failure-old['simultaneous_failure_bound_float'])<1e-15
files=[A/'certificate_v2.json',A/'certify_existing_measurement_v2.py',P/'training_counts_v1.npz',P/'results_v2.json',P/'independent_audit/RECEIPT_v1.json',Path(__file__)]
out={'status':'PASS_EXACT_FEATURE_FREE_FULL_ALPHABET_CERTIFICATE','full_alphabet_constraints_checked':size,'observed_labels':len(observed),'unobserved_labels':len(missing),'exact_projector_Bloch_norm_squared':'1','empirical_gap':str(gap),'oracle_regret_upper':str(regret),'oracle_regret_upper_float':float(regret),'training_failure_bound_recomputed':failure,'new_source_calls':0,'scope':'Same preserved receiver and records; full alphabet proof does not use shared flag feature or tree','sha256':{str(p.relative_to(Q)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(D/'check_same_bank_v1.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ['sha256','empirical_gap','oracle_regret_upper']})
