"""Outward-rounded rational high-density gate and coarse-completion certificate."""
from fractions import Fraction as F
from math import factorial
import json,sys,time
sys.set_int_max_str_digits(0)
BITS=96;Q=1<<BITS

def down(x:F)->F:
    return F(x.numerator*Q//x.denominator,Q)

def extension_lower(p:F,n:int)->F:
    q=1-p
    if n<256:
        r=F(1)
        for k in range(n,2*n):
            r=down(r*(1-p**k));r=down(r*(1-p**(k+1)))
    else:
        r=down(max(F(0),1-2*p**n/q))
    # At most one original protected port lies outside the chosen child.
    return down(r*(1-p**(n-1))/(1-p**n))

def gate_table(p:F,L:int):
    q=1-p;f=down(q**3);n=2
    rows=[dict(L=n,lower=str(f),decimal=float(f))]
    while n<L:
        r=extension_lower(p,n)
        f=down(4*f*r*r/(r+3*f));n*=2
        rows.append(dict(L=n,extension_lower=str(r),lower=str(f),decimal=float(f)))
    return f,rows

def evaluate(p:F=F(4,5),L:int=4096):
    gamma,rows=gate_table(p,L)
    b=1-gamma;delta=1-4*b-b*b
    if delta<=0:raise ValueError('proved coarse tail condition not satisfied')
    m2=4*b+32*b*b*(3-4*b+b*b)/(delta*delta)
    K=1+8*m2
    histories=5*L*L*factorial(L-1)*factorial(L)//8
    T=96*L**3
    C=8*histories*histories*T*T
    denominator=K*C
    # Exact power-of-ten lower endpoint, with the exponent proposed from lengths
    # and then checked by integer comparison, never by a floating logarithm.
    exponent=max(0,len(str(denominator.numerator))-len(str(denominator.denominator)))
    while denominator>10**exponent:exponent+=1
    while exponent>0 and denominator<=10**(exponent-1):exponent-=1
    assert denominator<=10**exponent
    return dict(p=str(p),L=L,bits=BITS,gate_table=rows,
                gamma_lower=str(gamma),bad_upper=str(b),coarse_energy_upper=str(K),
                coarse_energy_upper_decimal=float(K),microinstruction_upper=T,
                histories_one_block_decimal_digits=len(str(histories)),
                lower_endpoint=f'10^(-{exponent})',exponent=exponent,
                caveat='Valid but not quantitatively informative; not a successful dense prediction.')

if __name__=='__main__':
    t=time.perf_counter();result=evaluate();result['evaluation_seconds']=time.perf_counter()-t
    print(json.dumps(result,indent=2))
