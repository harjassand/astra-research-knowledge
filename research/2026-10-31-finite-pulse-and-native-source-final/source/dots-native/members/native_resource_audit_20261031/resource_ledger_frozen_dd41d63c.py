#!/usr/bin/env python3
"""Conservative displayed-cap ledger, NOT a complete gate counter.
mpmath interval arithmetic at 90 digits; upper endpoints for caps, lower for tolerances.
"""
import json, math
from fractions import Fraction
import mpmath as mp
mp.mp.dps=120; mp.iv.dps=90
I=mp.iv.mpf

def lo(x): return mp.mp.make_mpf(x._mpi_[0])
def hi(x): return mp.mp.make_mpf(x._mpi_[1])
def point(x): return I(x)
def ceil_up(x): return int(mp.mp.ceil(hi(x)))
def minlo(*xs): return I(min(lo(x) for x in xs))
def bits(x): return max(0,ceil_up(-mp.iv.log(x)/mp.iv.log(I(2))))
def fmt(x): return mp.mp.nstr(hi(x),14)
def rational(x): return I(x.numerator)/I(x.denominator)
def case(n,epsden,lam):
    eps=I(1)/epsden; g=I(19)/20; kap=I(20)/39; h=I(20*n)/19
    aH=h; aL2=I(40*n)/19; B=I(20)/19; mu=g*lam; Hs=I(1)
    c=mp.iv.sqrt(mu*B); r=mu/2; delta=r-2*c
    nu=mp.iv.sqrt(delta**2+8*c*c); down=(nu+delta)/2; slow=2*c*c/down
    tau=I(Fraction(1,256).numerator)/256
    Wcap=258 # ceil(1/tau)+p+1, with one extra safe slot
    u=kap/(16*h); theta=mp.iv.log(1+u)
    M=ceil_up((mp.iv.log(I(2))+mp.iv.log(1000/eps)+32*u*h*h*B/(kap*kap))/theta)+2
    S=M+Wcap+2
    target=Fraction(1)+2*Fraction(40*n,19); j=0
    while 4**j<target:j+=1
    A=32*2**j; dA=2*A+1
    e=eps/(1000*S); beta=(e/(10**6*dA*dA))**4; sigma=(beta/(100*A))**4; eta=beta/10**4
    Lphys=1+2*Hs+2*c+2*mu*aL2
    xmin=minlo(I(1),e/(100*Lphys))
    t0=sigma/4*minlo(xmin,1/(1+2*delta))
    # Round endpoint lower bounds downward by factor two as required by source.
    p0=I(lo(slow*t0/(1+nu*t0))/2)
    K=ceil_up((mp.iv.log(I(4))+7*slow*tau-mp.iv.log(eta)-mp.iv.log(p0))/mp.iv.log(I(2)))+2
    qr=nu+2*c
    zeta=minlo(t0/20,eta*p0/(100*(1+qr+qr*qr)))
    pz=I(lo(slow*(zeta/2)/(1+nu*zeta/2))/2)
    Lker=16*(1+qr)**2/pz**2
    ht=minlo(zeta/(100*(K+1)),eta/(100*(1+Lker+2*c)*(K+1)**2),beta/(100*(1+Hs+mu*(aH+1))*(K+1)**2))
    Lout=1+delta+mp.iv.sqrt(mu/B)*(Hs+c+mu*h)
    du=minlo(t0/10,beta/(100*(1+Lout)),e/(100*Lphys))
    J=ceil_up(mp.iv.log(tau/ht)/mp.iv.log(I(2)))+2
    Bouter=ceil_up(mp.iv.log(4*tau/(sigma*du))/mp.iv.log(I(2)))+2
    Binner=J+ceil_up(mp.iv.log(100*(K+1)/eta)/mp.iv.log(I(2)))+5
    primitive=beta/(10**4*(K+1)) # Necessary precision floor: actual capped operator count is >=K+1.
    proxy=S*dA*(K+1)
    return dict(n=n,epsilon=f'1/{epsden}',lambda_value=str(lam),mu=fmt(mu),B=fmt(B),tau='1/256',
        count_cap=M,window_cap=Wcap,call_cap=S,Aamp=A,OAA_degree=dA,virtual_cap=K,
        bits_beta=bits(beta),bits_sigma=bits(sigma),kernel_precision_bits_lower_bound=bits(primitive),
        bits_inner_time=bits(ht),bits_outer_time=bits(du),outer_uniform_bits=Bouter,
        inner_bisection_depth=J,inner_uniform_bits=Binner,
        padded_source_kernel_slot_proxy=str(proxy),
        generic_stack_action=fmt(Hs+c+mu*aL2),
        classical_uniformization_expected_ticks=str(n*lam),
        classical_flip_expected_lower=str(Fraction(400*n*lam,841)),
        classical_flip_expected_upper=str(Fraction(441*n*lam,841)),
        expected_count_MGF_upper=fmt(mp.iv.log(I(2))/theta+32*u*h*h*B/(kap*kap*theta)),
        log2_inverse_endpoint_floor=bits(p0),
        scope='Worst caps/precision proxies. No LCHS, encoding, arithmetic or consumer gate count inferred.')

def main():
 rows=[]
 for n in [4,8,16]:
  threshold=Fraction(4096)*Fraction(20,19)**2*Fraction(39*n,19)**2
  first=math.ceil(threshold)
  for epsden in [100,10000]:
   for lam in [first,10**8,10**12,10**18,10**24]: rows.append(case(n,epsden,lam))
 out={'method':'mpmath interval90 decimal digits; caps upward; lower tolerance endpoints; p0,pz halved; one extra window slot. Source formulas from frozen f503c800. No claimed implementation gate counts.', 'rows':rows}
 open('native_resource_audit_20261031/resource_ledger.json','w').write(json.dumps(out,indent=2)+'\n')
 for r in rows:
  if r['lambda_value'] in [str(10**24),str(math.ceil(Fraction(4096)*Fraction(20,19)**2*Fraction(39*r['n'],19)**2))]:
   print(r['n'],r['epsilon'],r['lambda_value'],r['call_cap'],r['Aamp'],r['virtual_cap'],r['padded_source_kernel_slot_proxy'],r['inner_uniform_bits'],r['kernel_precision_bits_lower_bound'])
if __name__=='__main__': main()
