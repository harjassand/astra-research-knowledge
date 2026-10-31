#!/usr/bin/env python3
"""Same physical fixtures; explicit source/attenuation invocation proxies, NOT gates."""
import json,sys,math
from fractions import Fraction
sys.path.insert(0,'native_first_event_optimization_20261031')
import sharp_ledger as sh
mp,I,lo,hi,ceil_up,minlo,bits=sh.mp,sh.I,sh.lo,sh.hi,sh.ceil_up,sh.minlo,sh.bits

def acosh(x):return mp.iv.log(x+mp.iv.sqrt(x*x-1))
def odd_degree(xi,pmin):
    x=acosh(1/mp.iv.sqrt(xi))/acosh(1/mp.iv.sqrt(1-I(pmin.numerator)/pmin.denominator))
    L=ceil_up(x)+2 # certified slack before odd rounding
    return L if L%2 else L+1

def case(n,epsden,lam):
    old=sh.case(n,epsden,lam);S=old['call_cap'];A=old['Aamp'];dA=old['OAA_degree'];K=old['virtual_cap'];D=K+4
    eps=I(1)/epsden;mu=I(19)*lam/20;B=I(20)/19;hsource=I(20*n)/19;Hs=I(1);tau=I(1)/256
    c=mp.iv.sqrt(mu*B);r=mu/2;_,de,nu,down,slow=sh.masses(c,r,mu,2*hsource,tau)
    e=eps/(1000*S);beta=e/(128*A);eta=beta/10000;xi=eta/(100*D)
    Le=odd_degree(xi,Fraction(1,4));Lh=odd_degree(xi,Fraction(1,2))
    Qrate=1+nu+2*c;Lword=1+Hs+mu*(hsource+1)
    Lphys=1+2*Hs+2*c+4*mu*hsource
    Lout=1+nu+mp.iv.sqrt(mu/B)*(Hs+c+mu*hsource)
    ht=minlo(eta/(10**7*D**3*(Qrate+Lword)),beta/(100*(1+Lout)),e/(100*Lphys))
    hbits=bits(ht);mesh=I(2)**(-hbits)
    pi0=down/nu;pi1=slow/nu;a0=(c+slow)/down
    thresholds=[mp.iv.log(1/x)/nu for x in [pi0,pi1,a0]]
    need=I(max([hi(2*tau)]+[hi(x) for x in thresholds]))+2*mesh
    wpow=ceil_up(mp.iv.log(need)/mp.iv.log(I(2)));W=I(2)**wpow
    Bclock=wpow+hbits
    assert Bclock>=1 and lo(W)>=hi(need)
    # At most one clock per race proposal or conditional-gap proposal.
    raw=3*K+3;factory=Le+2*Lh
    pathprepclock=raw+factory
    allclock=2*S*dA*pathprepclock
    clockrot=2*S*dA*((K+1)*(2*Bclock+2)+(2*K+2)*(Bclock+1)+factory*(Bclock+5)) # prefix state selects q0/q1: two rotations per multiplexed bit
    # Kernel acceptance bit-grid. This is its own acquired time arithmetic,
    # not the physical timestamp grid. Paid actual kernel error eta_k.
    eta_k=beta/(10000*(K+1));dsbits=bits(eta_k/(100*(hsource+1)));ds=I(2)**(-dsbits)
    scut=2*mp.iv.log(1/eta_k);Bkernel=ceil_up(mp.iv.log(scut/ds)/mp.iv.log(I(2)))+1
    slots=int(old['padded_source_kernel_slot_proxy'])
    filterrot=slots*2*n*Bkernel
    return dict(n=n,epsilon=f'1/{epsden}',lambda_value=str(lam),call_cap=S,Aamp=A,OAA_degree=dA,virtual_cap=K,
      time_grid_bits=hbits,clock_window_power_of_two=wpow,clock_register_bits=Bclock,
      factory_failed_probability_bits=bits(xi),YLC_event_PREP_calls=Le,YLC_atom_or_gap_PREP_calls=Lh,
      unconditional_clock_draw_cap_per_path_PREP=raw,conditional_factory_PREP_call_cap_per_path_PREP=factory,
      all_fixed_clock_PREP_invocation_proxy=str(allclock),all_source_clock_controlled_rotation_proxy=str(clockrot),
      kernel_allocated_error_bits=bits(eta_k),kernel_time_register_bits=Bkernel,
      padded_kernel_slot_proxy=str(slots),kernel_binary_attenuation_rotation_proxy=str(filterrot),
      old_three_call_conditional_PREP_invocation_proxy=str(6*S*dA*K),
      excluded='Not elementary gates or T gates. Reflection/comparison/routing/phase synthesis, physical coupling/jump/H0 operations, Gaussian basis rotations and preprocessing remain separate. No crossover.')

def main():
 rows=[]
 for n in [4,8,16]:
  first=math.ceil(Fraction(4096)*Fraction(20,19)**2*Fraction(39*n,19)**2)
  for ep in [100,10000]:
   for lam in [first,10**8,10**12,10**18,10**24]:rows.append(case(n,ep,lam))
 out=dict(status='UNREVIEWED operation-ledger candidate, same frozen physical/count/window/aggregate-word fixtures. YLC mean-only factory option and received geometric clocks; separate Gaussian attenuation interface.',
  scope='Clock rotations are controlled invocation proxies, not synthesized gates; kernel time bits are explicitly allocated to kernel approximation, not a final gate-synthesis tolerance. No execution benchmark or practical crossover.',rows=rows)
 open('native_first_event_optimization_20261031/last_refresh_operation_ledger.json','w').write(json.dumps(out,indent=2)+'\n')
 for x in rows:
  if x['lambda_value']=='1000000000000000000000000':
   print(*(x[k] for k in ['n','epsilon','clock_register_bits','YLC_event_PREP_calls','YLC_atom_or_gap_PREP_calls','all_source_clock_controlled_rotation_proxy','kernel_binary_attenuation_rotation_proxy']))
if __name__=='__main__':main()
