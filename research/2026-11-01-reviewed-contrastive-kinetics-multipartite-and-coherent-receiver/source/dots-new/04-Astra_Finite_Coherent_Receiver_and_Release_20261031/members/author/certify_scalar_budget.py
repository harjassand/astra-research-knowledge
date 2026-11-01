#!/usr/bin/env python3
"""Exact rational sufficient finite-lambda network budgets. No hardware parameters acquired."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
from exact_source_overlap import certify_overlap

def sqrt_up(x,bits=100):
 assert x>=0
 d=1<<bits;n=(x.numerator*d*d+x.denominator-1)//x.denominator
 r=isqrt(n)
 if r*r<n:r+=1
 out=F(r,d);assert out*out>=x
 return out

def receive(lam,b,k,T,zeta,remaining=F(0),target=F(1,100)):
 assert lam>0 and k>0 and T>=0 and b>=0 and 0<=zeta<=1
 E=(4*b*b+32*b**4*T)/lam
 assert E<=1
 moment_delta=2*(sqrt_up(2*E)+2*b*sqrt_up(1/lam)+16*b**3*sqrt_up(T)/lam)
 overlap=certify_overlap(lam,b,T)
 delta=min(moment_delta,F(overlap['complete_channel_comparison_upper']))
 q=(1+k*T/F(32))**(-16) # exp(-kT/2)<=q, exact Bernoulli exponential inequality
 R=8*b*b*(1-zeta)*T+4*sqrt_up(F(2))*zeta*b*b/k*(3+4*q+q*q)
 # Re(log f)<=0 from the actual coherent CPTP channel, so |1-f|<=|log f|.
 a_lower=F(overlap['amplitude_interval'][0]);orthogonal_weight=1-a_lower*a_lower
 refined=R+2*orthogonal_weight+2*sqrt_up(2*orthogonal_weight*R)
 upper=min(F(2),R+delta+remaining,refined+remaining)
 # Exact unchanged-source finite-rate benchmark bracket, without receiver.
 U=4*b*b*T;A=max(F(0),U-8*b*b/lam)
 bare_lower=2*A*max(F(0),1-2*U)
 return {'parameters':{n:str(x) for n,x in [('lambda',lam),('b',b),('receiver_total_k',k),('receiver_shift_chi',k/2),('T',T),('total_routing_external_efficiency_zeta',zeta),('remaining_complete_error_budget',remaining),('comparison_target',target)]},'source_orthogonal_weight_upper':str(orthogonal_weight),'variance_sensitive_uncorrected_upper':str(refined),'source_exact_overlap':overlap,'source_moment_comparison_upper':str(moment_delta),'source_excitation_plus_displaced_photon_upper':str(E),'finite_source_coherent_comparison_upper':str(delta),'coherent_receiver_UNCORRECTED_phase_and_dephasing_upper':str(R),'actual_total_complete_channel_upper':str(upper),'unchanged_source_complete_channel_lower':str(bare_lower),'meets_declared_model_budget':upper<=target,'unchanged_source_fails_declared_budget':bare_lower>target,'display_only':{'upper':float(upper),'bare_lower':float(bare_lower),'source_comparison':float(delta),'receiver_uncorrected':float(R)},'scope':'Sufficient exact known-model bound, no phase correction assumed; remaining budget is supplied, not acquired. No finite-mode truncation or floating expm enters.'}

if __name__=='__main__':
 rows=[receive(F(l),F(1,5),F(k),F(1),z,remaining=F(1,1000)) for l in [64,256,1024,4096,16384,65536,10**6] for k in [2,8,32,128,512] for z in [F(1),F(998001,1000000)]]
 out={'scope':'Exact parameter grid, including failures. No claim of measured availability or new mechanism over ordinary coherent feedback. Source coupling remains on at endpoint.','rows':rows}
 p=Path(__file__).with_name('scalar_budget_certificates.json');p.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps([r for r in rows if r['meets_declared_model_budget']],indent=2))
