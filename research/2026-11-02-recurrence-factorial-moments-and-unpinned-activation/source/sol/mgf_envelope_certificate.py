#!/usr/bin/env python3
"""Acquire rational alpha certificates for the multiplicative scalar envelope.

All logarithm enclosures and acceptance inequalities use exact Fractions.
This certifies the finite scalar operation, NOT a network's terminal rarity,
the location of its finite head, or a numerical stationary moment value.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json,time

P=Path(__file__).resolve().parent

def atanh_log_interval(r,J=80):
    assert 1<=r<=2
    t=(r-1)/(r+1);s=F(0);power=t
    for j in range(J):s+=2*power/(2*j+1);power*=t*t
    tail=2*power/((2*J+1)*(1-t*t))
    return s,s+tail

@lru_cache(None)
def log2_interval(J=80):return atanh_log_interval(F(2),J)

def log_interval(a,J=80):
    assert a>0
    k=a.numerator.bit_length()-a.denominator.bit_length()
    r=a/(1<<k) if k>=0 else a*(1<<(-k))
    if r<1:k-=1;r*=2
    if r>=2:k+=1;r/=2
    lo,hi=atanh_log_interval(r,J);l2,u2=log2_interval(J)
    return (lo+k*l2,hi+k*u2) if k>=0 else (lo+k*u2,hi+k*l2)

def floor_fraction(x,den=10**9):return F((x*den).numerator//(x*den).denominator,den)

def certify(m,R,q,K,max_path_edges=None):
    assert m>=2 and R>=1 and 0<q<=1 and K>=64
    alpha=F(1,1<<K);C0hi=log_interval(F(m)*R)[1]
    delta=F(1,10**12);eps=F(1,10**9)
    assert alpha<=delta/(1+delta)
    L=F(1)/(2*alpha);rows=[];minimum=None
    path_depth=m-1 if max_path_edges is None else max_path_edges
    assert 1<=path_depth<=m-1
    for depth in range(1,path_depth+1):
        Hlo=log_interval(q*L)[0]-C0hi
        # u = -log(1-alpha)/alpha + [log(qL)-C0]/(1-alpha).
        ulo=1+(Hlo if Hlo>=0 else (1+delta)*Hlo)
        if ulo<=0:return None
        # (1-exp(-alpha*u))/alpha >= u-alpha*u^2/2.
        # Use a proved uniform tiny remainder, avoiding catastrophic cancellation.
        assert alpha*ulo*ulo/2<=eps
        L=floor_fraction(ulo-eps)
        if L<=0:return None
        minimum=L if minimum is None else min(minimum,L)
        rows.append({'backward_edges':depth,'certified_c_over_alpha_lower':str(L),
                     'decimal_lower_display':float(L)})
    assert minimum>0 and alpha*minimum<F(1,2)
    return {'complexes':m,'outgoing_constant_ratio':str(R),'minimum_designated_fraction':str(q),
            'maximum_acquired_path_edges':path_depth,
            'alpha_exact':'2^(-'+str(K)+')','alpha_power_two_exponent':-K,
            'eta_ge_alpha_times_exact':str(minimum),
            'beta_physical_factorial_moment':'alpha/2',
            'terminal_probability_threshold_exact':'(1/('+str(F(m)*R)+')) * 2^(-2^'+str(K)+')',
            'log_series_terms':80,'proof_arithmetic':'Exact rational atanh-series logarithm enclosures and rational remainder comparisons.',
            'backward_bounds':rows}

def acquire(m,R,q,maxK=None,max_path_edges=None):
    K=64
    while maxK is None or K<=maxK:
        cert=certify(m,R,q,K,max_path_edges)
        if cert is not None:return cert
        K*=2
    return {'status':'NOT_ACQUIRED_WITHIN_THIS_SEARCH','maxK':maxK}

if __name__=='__main__':
    begin=time.monotonic()
    fixtures=[('three_complex_directed_cycle',3,F(3),F(1),2),
              ('five_complex_coupled_ACK_diagnostic',5,F(1),F(1),4),
              ('four_complex_ordered_obstruction_scalar_only',4,F(1),F(1),3),
              ('accepted_N1567_two_linkage_nonCB_demonstration',8,F(2),F(1),3)]
    rows=[]
    for name,m,R,q,depth in fixtures:
        cert=acquire(m,R,q,maxK=2**22,max_path_edges=depth);rows.append({'fixture':name,**cert})
        print(name,cert.get('alpha_exact',cert),cert.get('eta_ge_alpha_times_exact'),flush=True)
    out={'scope':'Finite acquired scalar-envelope certificates. Terminal rarity is proved by the governing source for one-linkage binary lists, and is explicitly FALSE for the ordered higher-degree obstruction.',
         'certificates':rows,'elapsed_seconds':time.monotonic()-begin}
    (P/'results/mgf_envelope_certificates.json').write_text(json.dumps(out,indent=2)+'\n')
