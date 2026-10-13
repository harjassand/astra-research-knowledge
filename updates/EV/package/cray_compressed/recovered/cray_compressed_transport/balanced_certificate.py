"""Compressed second-moment bound for balanced full-frame routing.

This produces a rigorous but scientifically uninformative dense lower bound.
No state-space graph or microscopic path is expanded by this calculation.
All probability lower bounds and moment upper bounds are rounded outwards.
"""
from __future__ import annotations
from fractions import Fraction as F
from hashlib import sha256
import json,sys,time
from probability_certificate import BITS,Q,down,gate_table
sys.set_int_max_str_digits(0)


def up(x:F)->F:
    return F(-((-x.numerator*Q)//x.denominator),Q)


def exact_strip_moment(m:int,p:F)->F:
    """m E[1/K; K>0], K binomial(m,1-p), evaluated by a scalar recurrence."""
    if m<1:raise ValueError('m must be positive')
    value=1-p;pp=p
    for k in range(2,m+1):
        pp*=p
        value=F(k,k-1)*p*value+1-pp
    return value


def frame_moment_upper(p:F,L:int):
    """16 times a product of max(1,V_m) factors, each strip used once."""
    values={1:up(1-p)};pp=down(p)
    for m in range(2,L+1):
        pp=down(pp*p)
        values[m]=up(F(m,m-1)*p*values[m-1]+1-pp)
    bound=F(16)
    for m in range(2,L):
        bound=up(bound*max(F(1),values[m]))
        bound=up(bound*max(F(1),values[m+1]))
    return bound,values


def evaluate(p:F=F(4,5),L:int=4096):
    f,rows=gate_table(p,L);b=1-f;delta=1-4*b-b*b
    if delta<=0:raise ValueError('coarse tail threshold not proved')
    K=1+8*(4*b+32*b*b*(3-4*b+b*b)/(delta*delta))
    R,values=frame_moment_upper(p,L)
    N=2*L*L;S=L**4//16;T=256*L**3
    inverse=8*T*T*S*S*N**6*L*L*R*R*K/(p*p*f*f)
    exponent=max(0,len(str(inverse.numerator))-len(str(inverse.denominator)))
    while inverse>10**exponent:exponent+=1
    while exponent>0 and inverse<=10**(exponent-1):exponent-=1
    assert inverse<=10**exponent
    selected={str(m):dict(upper=str(values[m]),decimal=float(values[m]))
              for m in (2,4,8,16,32,64,128,256,512,1024,2048,4096) if m<=L}
    return dict(p=str(p),L=L,bits=BITS,gate_lower=str(f),gate_lower_decimal=float(f),
                bad_upper=str(b),coarse_energy_upper=str(K),coarse_energy_upper_decimal=float(K),
                strip_moment_samples=selected,
                frame_moment_numerator_bits=R.numerator.bit_length(),
                frame_moment_sha256=sha256(str(R).encode()).hexdigest(),
                seed_pairs=S,sites=N,microinstruction_upper=T,
                lower_endpoint=f'10^(-{exponent})',exponent=exponent,
                status='Rigorous analytical certificate; too weak for a useful dense transport prediction.',
                pointwise_caveat='The certificate does not claim affordable exact evaluation of the full current.')


if __name__=='__main__':
    start=time.perf_counter();result=evaluate();result['evaluation_seconds']=time.perf_counter()-start
    print(json.dumps(result,indent=2))
