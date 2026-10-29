#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import json,numpy as np,math,hashlib
H=Path(__file__).parent;P=H.parent/'label_observed_quantum_flag_recovery_20261028';z=np.load(P/'training_counts_v1.npz');counts=z['counts'];mom=z['mom'];N=int(counts.sum());D=len(counts)
res=json.loads((P/'results_v2.json').read_text());tx=F(res['projector_parameters']['tx']);ty=F(res['projector_parameters']['ty']);norm=1+tx*tx+ty*ty;bloch=[2*tx/norm,2*ty/norm,(1-tx*tx-ty*ty)/norm]
chosen=sorted(sorted(range(D),key=lambda x:(-counts[x],x))[:2]);assert chosen==res['selected_words']
c0,c1=map(int,counts[chosen]);v0=[int(x)*3 for x in mom[chosen[0]]];v1=[int(x)*3 for x in mom[chosen[1]]];h=[a-b for a,b in zip(v0,v1)];t=c0-c1;L=sum(x*x for x in h);assert t*t<L
scale=2**120;slo=F(math.isqrt(L*scale*scale),scale);shi=slo+F(1,scale);smid=(slo+shi)/2
# Rational dual encloses Y=(A0+A1+|A0-A1|)/2 in operator norm.
gamma=(shi-slo)/(4*N)*(1+abs(t)*shi/(slo*smid))
y=[F(c0+c1,4*N)+smid/(4*N)+gamma]+[(F(a+b)+F(t)*F(k)/smid)/(4*N) for a,b,k in zip(v0,v1,h)]
def psd_coeff(coeff):return coeff[0]>=0 and coeff[0]*coeff[0]>=sum(a*a for a in coeff[1:])
observed=[i for i in range(D) if counts[i]>0];unseen=next((i for i in range(D) if not counts[i]),None)
checks=[]
for x in observed:
 a=[F(int(counts[x]),2*N)]+[F(3*int(v),2*N) for v in mom[x]];diff=[u-v for u,v in zip(y,a)];checks.append(psd_coeff(diff))
if unseen is not None:checks.append(psd_coeff(y))
assert all(checks)
primal=F(c0+c1,2*N)+sum(F(k)*b for k,b in zip(h,bloch))/(2*N);dual=2*y[0];gap=dual-primal;assert gap>=0
# Existing simultaneous component confidence gives operator error at most this.
delta=(F(1,500)+F(173206,100000)*F(1,200))/2
regret=4*delta+gap # r=2, 2r delta.
out={'status':'EXACT_RATIONAL_FULL_OBSERVED_DUAL_PASS','feature_used_by_certificate':False,'tree_used_by_certificate':False,'chosen_global_top_count_labels':chosen,'observed_label_count':len(observed),'one_zero_dummy_label':unseen,'full_alphabet_size':D,'exact_PSD_constraints_passed':len(checks),'dual_Pauli_coefficients':[str(x) for x in y],'certified_empirical_primal':str(primal),'certified_empirical_dual':str(dual),'empirical_gap':str(gap),'empirical_gap_float':float(gap),'uniform_operator_error_upper':str(delta),'full_CPTP_oracle_regret_upper':str(regret),'oracle_regret_float':float(regret),'training_failure_bound_from_existing_certificate':res['simultaneous_failure_bound_float'],'new_source_calls':0,'POVM_nonzero_effects':2,'maximum_required_qubit_flag_effects':4,'depends_on':{str(p.relative_to(H.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'training_counts_v1.npz',P/'results_v2.json',P/'GOVERNING_LABEL_OBSERVED_FLAG_RECOVERY_v1.md',P/'PAULI_BASIS_CLARIFICATION_v2.md']}}
(H/'certificate_v2.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ['depends_on','dual_Pauli_coefficients'] and not isinstance(v,str) or k in ['status']})
