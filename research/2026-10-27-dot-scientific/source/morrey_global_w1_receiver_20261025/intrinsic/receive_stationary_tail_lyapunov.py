"""Exact positive-vector tail for the already received stationary actual law.
No solve is rerun; every inequality is rational. No cutoff law changes here.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib,time
P=Path(__file__).parent;start=time.time();read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pp=P/'three_axis_control_actual_paid_policy.json';vp=P/'stationary_tail_lyapunov_vector.json';d=read(pp);c=read(vp);assert c['policy_sha256']==sha(pp)
st=d['states'];idx={tuple(s['state']):i for i,s in enumerate(st)};assert len(idx)==len(st)==len(c['numerators']);v=[Q(n,c['denominator'])for n in c['numerators']];D=int(d['policy_denominator']);rho=Q(15,16);assert min(v)>=1 and max(v)<=15;root=idx[tuple(d['root'])];assert v[root]<=13
slack=[];edges=0
for i,s in enumerate(st):
 counts=list(map(int,s['axis_stop_counts']));assert len(counts)==3 and min(counts)>=0
 pv=Q();mass=sum(counts)
 for a in s['splits']:
  count=int(a['policy_count']);prob=Q(a['left_probability']);assert count>0 and 0<prob<1;mass+=count
  j=idx[tuple(a['left'])];k=idx[tuple(a['right'])];pv+=Q(count,D)*(prob*v[j]+(1-prob)*v[k]);edges+=2
 assert mass==D
 delta=rho*v[i]-pv;assert delta>=0;slack.append(delta)
# If T is the number of performed ordinary transitions before axis stopping,
# Pr(T>=N) <= (P^N 1)(root) <= 13*(15/16)^N. Completing at ANY
# valid full boundary chord after N ordinary transitions costs at most4 times
# this mass. The bound also covers a convention shifted by one by using N-1.
records=[]
for N,bits in [(21504,1024),(19968,1024),(1024,80)]:
 assert 52*pow(15,N-1)*(1<<bits)<=pow(16,N-1)
 records.append({'ordinary_step_cutoff':N,'survival_steps_used_for_safe_off_by_one':N-1,'conditional_W1_tail_upper':str(Q(1,1<<bits)),'dyadic_tail_bits':bits,'exact_integer_power_inequality_pass':True,'same_existing_finite_instance':N in [21504,19968],'scope':'21504 and19968 reprice existing finite instances;1024 is an OPTIONAL DISTINCT shorter finite law, not adopted by this receipt.'})
out={'status':'EXACT_POLICY_SPECIFIC_POSITIVE_LYAPUNOV_TAIL_PASS','actual_policy_sha256':sha(pp),'dyadic_vector_sha256':sha(vp),'states':len(st),'ordinary_transition_edges':edges,'rho':str(rho),'minimum_v':str(min(v)),'maximum_v':str(max(v)),'root_v':str(v[root]),'minimum_exact_row_slack':str(min(slack)),'maximum_v_declared':'15','root_v_declared':'13','all_substochastic_row_mass_and_transition_targets_checked':True,'all_Pv_le_rho_v_checked':True,'cutoff_bounds':records,'seconds':time.time()-start,'scope':'Exact positive Lyapunov certificate for this hash-bound previously received stationary null policy. The same existing21504 and19968 cutoff laws get sharper conditional W1 tail bounds without any change of controls, terminal completion, root law, or AC law. Optional1024-cutoff statement is explicitly a different finite instance and is not adopted. Atomic/AC scopes remain separate; no source membership or optimum.'}
(P/'stationary_tail_lyapunov_receipt.json').write_text(json.dumps(out,indent=2));print(out,flush=True)
