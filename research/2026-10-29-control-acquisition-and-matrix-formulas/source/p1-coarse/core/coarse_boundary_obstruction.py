"""Exact obstruction to treating a coarse label as a regenerative state."""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'branches'/'physical'))
from rational_linalg import Mat, diag


def enc(x):
    if isinstance(x,F):
        if max(x.numerator.bit_length(),x.denominator.bit_length())<1000:
            exact={'fraction':str(x)}
        else:
            exact={'numerator_hex':hex(x.numerator),'denominator_hex':hex(x.denominator)}
        return dict(exact,diagnostic=float(x))
    if isinstance(x,dict):return {k:enc(v) for k,v in x.items()}
    if isinstance(x,list):return [enc(v) for v in x]
    return x


def run():
    refresh=Mat([[F(1,2),F(1,2)],[F(1,2),F(1,2)]])
    v=Mat([F(1,2),F(1,2)]) # probability preparation, not Hilbert unit vector
    ones=Mat([1,1])
    assert sum((F(5**k,factorial(k)) for k in range(20)),F(0))>100
    cases=[]
    for m in [32,64,128,256]:
        g=F(1,m)
        slow,fast=1-g**3,1-g
        p=(slow+fast)/2
        a=diag(slow,fast)
        indistinguishable=p*diag(1,1)
        horizon=10*m
        true_response=(slow**horizon+fast**horizon)/2
        scalar_prediction=p**horizon
        gap_lower=F(49,100)-5*g*g
        assert true_response-scalar_prediction>gap_lower>F(48,100)
        assert (ones.T*a*v)[0]==(ones.T*indistinguishable*v)[0]==p
        assert refresh*a*refresh==p*refresh
        second=Mat([[F(3,5),F(1,10)],[F(1,10),F(7,10)]])
        p_second=(ones.T*second*v)[0]
        assert a*second!=second*a
        assert refresh*second*refresh==p_second*refresh
        # Three nontrivial words confirm the ordinary all-word projection identity.
        refreshed_checks=[]
        for word in [(0,1,0),(1,0,0,1),(0,1,1,0,1)]:
            x=v
            prediction=F(1)
            for mode in word:
                op=[a,second][mode]
                x=refresh*op*x
                prediction*=[p,p_second][mode]
            assert (ones.T*x)[0]==prediction
            refreshed_checks.append({'word':list(word),'response':prediction})
        cases.append(dict(g=g,horizon=horizon,original_kernel=a.a,
            comparison_kernel=indistinguishable.a,one_step_boundary_probability=p,
            excursion_return_probability=F(0),alive_outside_probability=F(0),
            observed_absorption_probability=1-p,first_return_record_laws_identical=True,
            original_long_response=true_response,coarse_scalar_prediction=scalar_prediction,
            exact_response_gap=true_response-scalar_prediction,gap_lower=gap_lower,
            original_norm_strictly_below_one=True,refresh_projection=refresh.a,
            refreshed_word_checks=refreshed_checks,
            standardized_refreshed_program_cost={'original_operations':horizon,'refresh_operations':horizon,
                'scope':'One refresh after each source step; final refresh may be omitted for a single coarse endpoint read.'}))
    result=dict(scope='Ordinary exact two-state counterexample and physically altered refresh construction; no sampled trajectories.',
        interface='Uniform initial preparation; only live coarse-cell / absorbed reports; both microstates share the same coarse cell.',
        obstruction='Every fresh first-return record has the same one-step Bernoulli law for both sources, however many such trials are acquired.',
        reuse_caution='Fresh preparation is used for the indistinguishability claim; recycling a coarse positive report is not a valid restart.',
        refresh_caution='The positive construction changes the permitted operation language and pays for an actual conditional randomization operation.',cases=cases)
    (ROOT/'results'/'COARSE_BOUNDARY_OBSTRUCTION.json').write_text(json.dumps(enc(result),indent=2)+'\n')
    for x in cases:print(x['g'],x['horizon'],float(x['exact_response_gap']),float(x['gap_lower']))


if __name__=='__main__':run()
