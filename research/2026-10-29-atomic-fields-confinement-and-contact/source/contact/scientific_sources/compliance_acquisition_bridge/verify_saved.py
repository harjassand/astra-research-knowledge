"""Replay serialized interval coverage and exact upper computations.

This checks implementation/evidence transport. The analytical inequalities
and physical premises have separate scopes in PRIMARY_PROOF.md.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

from contact_certificate import (
    PI_LO, PI_HI, Parameters, certify, corrected_upper, inverse_quadratic,
    interval_upper, reference_mass_bounds,
)


def atan_bounds(x, n=80):
    s=sum(((-1)**j)*x**(2*j+1)/F(2*j+1) for j in range(n))
    next_term=((-1)**n)*x**(2*n+1)/F(2*n+1)
    return min(s,s+next_term),max(s,s+next_term)


def main():
    started=time.monotonic()
    a0,a1=atan_bounds(F(1,5))
    b0,b1=atan_bounds(F(1,239))
    # Machin's identity pi=16 atan(1/5)-4 atan(1/239).
    assert PI_LO < 16*a0-4*b1 < 16*a1-4*b0 < PI_HI
    root=Path(__file__).resolve().parent
    core_hash=hashlib.sha256((root/'contact_certificate.py').read_bytes()).hexdigest()
    result=json.loads((root/'bridge_results.json').read_text())
    assert result['code_sha256']==core_hash
    receipts=result['contact_sweep']+result['nuisance_sweep']+result['matched_service_residual_screen']+[
        result['ordinary_absolute_total_compliance'],
        result['ordinary_uniform_contrast_only'],
    ]
    leaf_count=0
    max_bits=0
    for record in receipts:
        params=Parameters(**{k:F(v) for k,v in record['parameter_rationals'].items()})
        params.check()
        q=inverse_quadratic(record['U_dimensionless_triple'])
        k=record['contact_lower_Pa_per_m']
        k=None if k is None else F(k)
        left,right=map(F,record['depth_interval'])
        header=certify(record['U_dimensionless_triple'],params,k,
                       depth=(left,right),max_cells=1)
        assert header['thickness_burial_clearance_m']==record['thickness_burial_clearance_m']
        leaves=record['coverage_leaves']
        assert len(leaves)==record['leaf_count']
        assert F(leaves[0]['left'])==left and F(leaves[-1]['right'])==right
        previous=left
        uppers=[]
        for leaf in leaves:
            l,r=F(leaf['left']),F(leaf['right'])
            assert l==previous and l<r
            previous=r
            actual=interval_upper(l,r,q,params,k)
            assert actual==F(leaf['upper_Pa_sqrt_m'])
            uppers.append(actual)
            max_bits=max(max_bits,abs(actual.numerator).bit_length(),actual.denominator.bit_length())
            leaf_count+=1
        assert max(uppers)==F(record['upper_Pa_sqrt_m'])

    # These are invalid-input checks, not additional mechanical fixtures.
    _,m=reference_mass_bounds()
    U=(m,0,m)
    guards=0
    for run in [
        lambda: certify((1,2,1),Parameters(),10**15),
        lambda: certify(U,Parameters(),0),
        lambda: certify(U,Parameters(),10**15,depth=(-1,F(4,5))),
        lambda: certify(U,Parameters(a_max=F(1,100)),10**15),
        lambda: certify(U,Parameters(service0=F(1)),10**15),
        lambda: corrected_upper((1,0,1),(-1,0,0)),
    ]:
        try:run()
        except ValueError:guards+=1
        else:raise AssertionError('invalid input accepted')
    out={
        'status':'SAVED_INTERVAL_REPLAY_PASSED',
        'saved_certificates':len(receipts),'coverage_leaves':leaf_count,
        'pi_bracket':'VERIFIED_BY_RATIONAL_MACHIN_SERIES',
        'invalid_input_guards':guards,
        'largest_saved_leaf_numerator_or_denominator_bits':max_bits,
        'core_sha256':core_hash,
        'results_sha256':hashlib.sha256((root/'bridge_results.json').read_bytes()).hexdigest(),
        'wall_seconds':time.monotonic()-started,
        'scope':'IMPLEMENTATION_AND_TRANSPORT; PHYSICAL_PREMISES_NOT_ACQUIRED',
    }
    (root/'replay_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
