"""Exact finite-local-oscillator / finite-counter receiving for accepted beta=8 bus."""
from fractions import Fraction as Q
from pathlib import Path
from math import factorial
import json
from accepted_certify_bus import IV,iv,sqrt,exp_neg,pi_interval,certify,atan_small

def rec(x):return iv(x).record()
def fromrec(r):return IV(*map(Q,r['interval']))
def atan(x):
 x=iv(x);assert 0<=x.lo<=x.hi<1
 return IV(atan_small(x.lo).lo,atan_small(x.hi).hi)
def receive(nlo,M=20,readout_delay=Q(1)):
 base=certify(8);S=fromrec(base['captured_displacement_energy']);ell=fromrec(base['inaccessible_displacement_energy'])
 nlo=Q(nlo);a=exp_neg(2*ell);d=exp_neg(8*ell)
 v=exp_neg((sqrt(nlo+4*S)-sqrt(nlo))**2/2);t=a*v;w=1-t;q=1-d
 margin=2*t-1-d
 if margin.lo>=0:diamond=q;branch='minimax_extreme_pair'
 elif margin.hi<0:diamond=4*w*w/(4*w-q);branch='three_sector_interior'
 else:raise ValueError('unresolved branch: refine interval')
 lam=nlo+4*S
 if lam.hi<M+2:
  pover=exp_neg(lam)*lam**(M+1)/factorial(M+1)/(1-lam/(M+2))
  pover=IV(min(Q(1),pover.lo),min(Q(1),pover.hi))
 else:pover=IV(0,1)
 # Remove the ideal homodyne ADC/saturation terms: this is a different finite instrument.
 data=fromrec(base['continuing_data_upper'])+Q(4,10000)*readout_delay
 correction=IV(Q(4,10**6));other=IV(Q(1,1000))
 total=diamond+2*pover+data+correction+other
 theta=atan(2*sqrt(S/nlo))/2
 table=[];pi=pi_interval()
 for delta in range(-M,M+1):
  angle=delta*theta;mid=(angle.lo+angle.hi)/2;pimid=(pi.lo+pi.hi)/2
  k=(mid/pimid+Q(1,2)).numerator//(mid/pimid+Q(1,2)).denominator
  wrapped=angle-k*pi;mid=(wrapped.lo+wrapped.hi)/2
  quantum=Q(1,10**9);command=Q(round(mid/quantum))*quantum
  err=max(abs(command-wrapped.lo),abs(command-wrapped.hi));assert err<Q(1,10**8)
  assert max(abs(wrapped.lo),abs(wrapped.hi))<pi.lo/2
  table.append(dict(count_difference=delta,local_Z_coefficient_angle=str(command),computation_error_upper=str(err)))
 return {'parameters':{'observed_LO_mean':str(nlo),'total_count_cap':M,'additional_PNR_readout_time':str(readout_delay),'per_qubit_correction_angle_error':str(Q(1,10**6)),'eta_both_detectors':'999/1000','other_complete_error_allowance':'1/1000'},'source_beta8_collected_energy':S.record(),'source_beta8_lost_energy':ell.record(),'LO_adjacent_factor':v.record(),'minimax_condition_margin':margin.record(),'diamond_branch':branch,'exact_bus_receiver_diamond':diamond.record(),'maximum_total_count_mean':lam.record(),'uniform_overflow_probability_upper':pover.record(),'continuing_data_error_upper':data.record(),'finite_correction_error_upper':correction.record(),'total_complete_error_upper':total.record(),'meets_0_01':total.hi<Q(1,100),'theta_interval':theta.record(),'finite_correction_table':table}

def main():
 rows=[receive(n) for n in [1,2,3,4,6,7,8,13,16]]
 base=certify(8);S=fromrec(base['captured_displacement_energy']);eta=Q(999,1000)
 # Lower bound under a stipulated average system efficiency .314, not a transplanted apparatus claim.
 I=pi_interval()/8;uncaptured=I/5-Q(314,1000)*S/eta
 lower=1-exp_neg(8*uncaptured)
 result={'format':'exact-finite-LO-bus-receiver-v1','scope':'Vacuum/coherent three-eigenvalue gate, exact number instrument below finite cap, same beta8 filter; detector quality and response are supplied physical services','rows':rows,'average_efficiency_0_314_extreme_pair_lower':lower.record()}
 out=Path(__file__).with_name('finite_lo_certificates.json');out.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'rows':len(rows),'passing_LO_means':[r['parameters']['observed_LO_mean'] for r in rows if r['meets_0_01']],'LO4_upper':rows[3]['total_complete_error_upper']['decimal_diagnostic'][1],'counter_cap':20,'added_readout_time':1},indent=2))
if __name__=='__main__':main()
