"""Construct a bounded complex terminal moment from a factored sign source.

The generating-polynomial operation is ordinary prior. Its covariance-scale
norm contract is proved in COMPLEX_INITIAL_SOURCE.md. This consumer does
not claim execution of root's improved full sampler on this source.
"""
from math import factorial
from pathlib import Path
from time import perf_counter
from itertools import product
import json
import sympy as sp
import mpmath as mp


def moment(q,z,vectors,kappa,simplify=None):
    coefficients=[1]+[0]*q
    multiplies=0
    for v in vectors:
        a=sum(z[i]*v[i] for i in range(3))
        a2=a*a
        local=[1]
        for j in range(1,q+1): local.append(local[-1]*a2/((2*j-1)*(2*j)))
        coefficients=[sum(coefficients[j]*local[r-j] for j in range(r+1))
                      for r in range(q+1)]
        if simplify: coefficients=[simplify(x) for x in coefficients]
        multiplies+=(q+1)*(q+2)//2
    value=2**q*factorial(q)*coefficients[q]/kappa**q
    return (simplify(value) if simplify else value),multiplies


def main():
    started=perf_counter()
    primes=list(sp.primerange(1024,2000))[:64]
    vectors=[(sp.Rational(p//8,p),sp.Integer(0),sp.Integer(0)) for p in primes]
    kappa=sum(v[0]**2 for v in vectors)
    radius=sum(v[0] for v in vectors)
    assert kappa>0
    z=(sp.Rational(3,5)+sp.I*sp.Rational(4,5),sp.Integer(0),sp.Integer(0))
    assert sp.expand(z[0]*sp.conjugate(z[0]))==1
    small=vectors[:6];small_k=sum(v[0]**2 for v in small)
    points=[sum(e*v[0] for e,v in zip(signs,small)) for signs in product([-1,1],repeat=6)]
    exact=[]
    for q in range(9):
        answer,_=moment(q,z,small,small_k,sp.expand)
        d=sp.factorial(2*q)/(2**q*sp.factorial(q))
        reference=sum((z[0]*v)**(2*q) for v in points)/(64*d*small_k**q)
        assert sp.simplify(answer-reference)==0
        assert sp.simplify(answer*sp.conjugate(answer))<=1
        exact.append(dict(q=q,real=str(sp.re(answer)),imag=str(sp.im(answer))))
    mp.mp.dps=90
    mv=[tuple(mp.mpf(int(sp.numer(x)))/int(sp.denom(x)) for x in v) for v in vectors]
    mk=mp.mpf(int(sp.numer(kappa)))/int(sp.denom(kappa))
    mz=(mp.mpc(3,4)/5,mp.mpf(0),mp.mpf(0))
    tick=perf_counter();value,work=moment(12,mz,mv,mk)
    numerical_seconds=perf_counter()-tick
    assert abs(value)<=1
    cumulant=-2*sum(v[0]**4 for v in vectors)
    input_bits=sum(int(sp.numer(v[0])).bit_length()+int(sp.denom(v[0])).bit_length()
                   for v in vectors)
    out=dict(scope='Exact terminal-source construction; no improved full-law rerun',
        exact_enumeration_controls=exact,source_vectors=64,
        source_rational_input_bits=input_bits,source_distinct_atoms=str(2**64),
        distinctness_proof='multiply by product of distinct odd primes, reduce modulo each',
        kappa_exact=str(kappa),support_radius_exact=str(radius),
        kappa=float(kappa),support_radius_squared=float(radius**2),
        support_squared_over_kappa=float(radius**2/kappa),
        old_sufficient_variance_threshold=float(4*radius**2),
        improved_sufficient_variance_threshold=float(kappa),
        individual_all_plus_q1_sample_magnitude=float(radius**2/kappa),
        active_fourth_cumulant=float(cumulant),
        q12_modulus=str(abs(value)),q12_complex_multiply_count=work,
        q12_seconds=numerical_seconds,seconds=perf_counter()-started,
        qualification='90-digit evaluation is not an outward arithmetic certificate; analytical norm proof is separate')
    path=Path(__file__).parent/'outputs'/'INITIAL_ORACLE.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['exact_enumeration_controls','kappa_exact','support_radius_exact']},indent=2))


if __name__=='__main__':main()
