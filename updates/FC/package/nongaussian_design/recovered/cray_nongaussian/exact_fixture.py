"""Exact arithmetic for a CONDITIONAL statistical certificate.

Counts are simulated Hubbard measurements from diagnostics.json, not laboratory
observations. Given independent Gibbs samples, the proof converts their binomial
confidence interval and a local hopping bound into a rigorous free-energy
interval. It does not certify equilibrium, calibration, or a real material.
"""
from fractions import Fraction as Q
from math import factorial
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def exp_bounds(x:Q,n:int=100):
    if x<0:
        lo,hi=exp_bounds(-x,n); return 1/hi,1/lo
    terms=[x**j/Q(factorial(j)) for j in range(n)]
    lo=sum(terms,Q(0)); first=x**n/Q(factorial(n)); ratio=x/Q(n+1)
    assert ratio<1
    return lo,lo+first/(1-ratio)

def log_bounds(x:Q,n:int=130):
    if x<1:
        lo,hi=log_bounds(1/x,n); return -hi,-lo
    y=(x-1)/(x+1)
    lo=2*sum((y**(2*j+1)/Q(2*j+1) for j in range(n)),Q(0))
    rem=2*y**(2*n+1)/(Q(2*n+1)*(1-y*y))
    return lo,lo+rem

def dec(q:Q,places:int=12,up:bool=False):
    scale=10**places; n=q.numerator*scale; den=q.denominator
    a=-((-n)//den) if up else n//den
    sign='-' if a<0 else ''; a=abs(a)
    return sign+str(a//scale)+'.'+str(a%scale).zfill(places)

# beta=2, two incident spin-up hoppings each 1/40:
# (beta*kappa)^2 = beta^2 * 2*(1/40)^2 = 1/200.
sq=Q(1,200); terms=40
Clo=sum((sq**j/Q(factorial(2*j)) for j in range(terms)),Q(0))
first=sq**terms/Q(factorial(2*terms))
ratio=sq/Q((2*terms+1)*(2*terms+2)); Chi=Clo+first/(1-ratio)
eta=1-1/Chi
N=30000; ones=28780; radius=Q(1,100)
plo=Q(ones,N)-radius; phi=Q(ones,N)+radius
assert 0<eta<plo<phi<1
# Counterfactual lowering by 1, plus scalar cost 3/10; beta*v=(3/5,-7/5).
a_lo,a_hi=exp_bounds(-Q(3,5)); b_lo,b_hi=exp_bounds(Q(7,5))
ratio_lo=(1-plo)*a_lo+(plo-eta)*b_lo
ratio_hi=(1-phi)*a_hi+phi*b_hi
assert ratio_lo>1  # The sign decision uses this rational comparison alone.
loglo,_=log_bounds(ratio_lo); _,loghi=log_bounds(ratio_hi)
Flo=-loghi/2; Fhi=-loglo/2
# Adaptive candidate selection is covered by the same simultaneous histogram event.
# A cost 39/40 is intentionally chosen from the acquired threshold interval,
# not described as an independent external material benchmark.
adaptive_offset=Q(27,40)
assert Fhi+adaptive_offset<0
# Hoeffding failure <= 2*exp(-6) < 1/200.
e6lo,e6hi=exp_bounds(Q(6),35); assert e6lo>400
out={'provenance':'Conditional certificate using simulated counts, not experimental data',
     'counts':{'zero':N-ones,'one':ones},'sample_count':N,
     'assumptions':['independent equilibrium samples','correct fixed Nup=Ndown sector',
                    'beta=2 and incident up hoppings <=1/40','additive calibrated local shift'],
     'simultaneous_binary_coverage_greater_than':'0.995',
     'C_enclosure':[dec(Clo,16),dec(Chi,16,True)],
     'partition_ratio_lower_above_one_exact':True,
     'free_energy_interval_outward':[dec(Flo),dec(Fhi,up=True)],
     'free_energy_gain_without_scalar_cost_outward':[dec(Q(3,10)-Fhi),dec(Q(3,10)-Flo,up=True)],
     'adaptive_cost_threshold':'0.975',
     'adaptive_cost_free_energy_interval_outward':[dec(Flo+adaptive_offset),dec(Fhi+adaptive_offset,up=True)],
     'adaptive_decision_strictly_negative_exact':True,
     'method':'rational Taylor tails, rational log series, exact integer comparisons'}
(ROOT/'exact_certificate.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
