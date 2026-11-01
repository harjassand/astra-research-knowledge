from fractions import Fraction as F
from pathlib import Path
import json
from exact_source_overlap import certify_overlap,sqrt_up
from certify_scalar_budget import receive
lam=F(4096);b=F(1,5);k=F(128);T=F(1);zeta=F(998001,1000000);switch=F(1,10000);tau=F(1,1000);impl=F(1,1000)
base=receive(lam,b,k,T,zeta)
R=F(base['coherent_receiver_UNCORRECTED_phase_and_dephasing_upper'])+24*b*b*switch
a=certify_overlap(lam,b,T+switch);alo=F(a['amplitude_interval'][0]);delta=1-alo*alo
before=R+2*delta+2*sqrt_up(2*delta*R)
handoff=16*b*b/lam+8*b*b*tau
upper=before+handoff+impl
assert upper<F(1,100)
out={'scope':'Declared complete released-memory budget; no source reset or source-coupling shutoff. Receiver chi-off and separate output-memory SWAP/isolation are supplied requirements, not acquired hardware.','parameters':{'lambda':str(lam),'b':str(b),'k':str(k),'chi_initial':str(k/2),'T_phase':str(T),'zeta':str(zeta),'switch_time':str(switch),'swap_time':str(tau),'supplied_other_complete_error':str(impl)},'source_overlap_at_end_of_switch':a,'coherent_reference_with_switch_upper':str(R),'before_swap_upper':str(before),'correlated_source_swap_upper':str(handoff),'total_upper':str(upper),'target':'1/100','passes_exact_rational_comparison':True,'display_only':{'before_swap':float(before),'swap':float(handoff),'total':float(upper)}}
Path(__file__).with_name('release_budget_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
