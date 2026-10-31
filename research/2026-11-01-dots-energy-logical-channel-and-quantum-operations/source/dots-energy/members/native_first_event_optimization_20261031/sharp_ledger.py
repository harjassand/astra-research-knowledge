#!/usr/bin/env python3
"""High-branch assembly revision: same frozen fixtures, not a gate counter."""
import sys,json,math
from fractions import Fraction
sys.path.insert(0,'native_resource_audit_20261031')
import resource_ledger as old
mp=old.mp; I=old.I; lo=old.lo; hi=old.hi; ceil_up=old.ceil_up; minlo=old.minlo; bits=old.bits; fmt=old.fmt

def exprel(x):
    # All growing arguments here are bounded; the zero case is exact.
    if lo(x)==hi(x)==0:return I(1)
    return mp.iv.expm1(x)/x

def masses(c,r,mu,aL2,tau,z=1):
    c=z*c; delta=r-2*c; nu=mp.iv.sqrt(delta**2+8*c*c)
    d=(nu+delta)/2; s=2*c*c/d
    a=2*(c+s)/nu; b=2*(d-c)/nu
    sn=((d+2*s+4*c)/nu)*mp.iv.exp(s*tau)+((2*d+s-4*c)/nu)*mp.iv.exp(-d*tau)
    integ=a*a*tau*exprel(2*s*tau)+2*a*b*tau*exprel(-delta*tau)+b*b*tau*exprel(-2*d*tau)
    Z=I(max(mp.mpf(9),hi(sn*sn)))+aL2*mu*integ
    return Z,delta,nu,d,s

def case(n,epsden,lam):
    baseline=old.case(n,epsden,lam)
    eps=I(1)/epsden; mu=I(19)*lam/20; B=I(20)/19; Hs=I(1)
    h=I(20*n)/19; aH=h; aL2=2*h; c=mp.iv.sqrt(mu*B); r=mu/2; tau=I(1)/256
    Z,delta,nu,d,s=masses(c,r,mu,aL2,tau)
    Z2,*_=masses(c,r,mu,aL2,tau,2)
    A=ceil_up(mp.iv.sqrt(Z))+1 # strictly certified, one integer slack
    dA=2*A+1; S=baseline['call_cap']; e=eps/(1000*S)
    beta=e/(128*A); eta=beta/10000; sigma=(beta/100)**2
    K=ceil_up(mp.iv.log(8*mp.iv.sqrt(Z2)/(A*beta))/mp.iv.log(I(2)))+2
    Lphys=1+2*Hs+2*c+2*mu*aL2
    xmin=minlo(I(1),e/(100*Lphys))
    t0=sigma/4*minlo(xmin,1/(1+2*nu))
    p0=I(lo(s*t0/(1+nu*t0))/2)
    qr=nu+2*c
    zeta=minlo(t0/20,eta*p0/(100*(1+qr+qr*qr)))
    pz=I(lo(s*(zeta/2)/(1+nu*zeta/2))/2)
    Lker=16*(1+qr)**2/pz**2
    ht=minlo(zeta/(100*(K+1)),eta/(100*(1+Lker+2*c)*(K+1)**2),beta/(100*(1+Hs+mu*(aH+1))*(K+1)**2))
    Lout=1+nu+mp.iv.sqrt(mu/B)*(Hs+c+mu*h)
    du=minlo(t0/10,beta/(100*(1+Lout)),e/(100*Lphys))
    J=ceil_up(mp.iv.log(tau/ht)/mp.iv.log(I(2)))+2
    Bout=ceil_up(mp.iv.log(8*tau/(sigma*du))/mp.iv.log(I(2)))+2
    Bin=J+ceil_up(mp.iv.log(100*(K+1)/eta)/mp.iv.log(I(2)))+5
    proxy=S*dA*(K+1)
    return dict(n=n,epsilon=f'1/{epsden}',lambda_value=str(lam),call_cap=S,
      proposal_mass_upper=fmt(Z),tilted_mass_upper=fmt(Z2),Aamp=A,OAA_degree=dA,virtual_cap=K,
      bits_beta=bits(beta),bits_sigma=bits(sigma),bits_inner_time=bits(ht),bits_outer_time=bits(du),
      inner_uniform_bits=Bin,outer_uniform_bits=Bout,
      kernel_precision_bits_lower_bound=bits(beta/(10000*(K+1))),
      padded_source_kernel_slot_proxy=str(proxy),baseline_proxy=baseline['padded_source_kernel_slot_proxy'],
      proxy_reduction=float(int(baseline['padded_source_kernel_slot_proxy'])/proxy),
      generic_stack_action=baseline['generic_stack_action'],classical_uniformization_expected_ticks=baseline['classical_uniformization_expected_ticks'])

def main():
    rows=[]
    for n in [4,8,16]:
      first=math.ceil(Fraction(4096)*Fraction(20,19)**2*Fraction(39*n,19)**2)
      for epsden in [100,10000]:
       for lam in [first,10**8,10**12,10**18,10**24]:rows.append(case(n,epsden,lam))
    out={'status':'UNREVIEWED candidate; same count/window caps and physical fixtures as frozen baseline. Exact positive proposal, sharp OAA lemma and aggregate word tail. No quantum gate backend.',
     'precision_scope':'Necessary kernel precision floor only. Full LCHS/arithmetic and supplied operator gate counts remain uninstantiated. Interval90 arithmetic with upward caps/downward tolerances.', 'rows':rows}
    open('native_first_event_optimization_20261031/sharp_ledger.json','w').write(json.dumps(out,indent=2)+'\n')
    for row in rows:
     if row['lambda_value']=='1000000000000000000000000' or row==next(r for r in rows if r['n']==row['n'] and r['epsilon']==row['epsilon']):
      print(*(row[k] for k in ['n','epsilon','lambda_value','Aamp','virtual_cap','padded_source_kernel_slot_proxy','proxy_reduction','bits_beta','inner_uniform_bits']))
if __name__=='__main__':main()
