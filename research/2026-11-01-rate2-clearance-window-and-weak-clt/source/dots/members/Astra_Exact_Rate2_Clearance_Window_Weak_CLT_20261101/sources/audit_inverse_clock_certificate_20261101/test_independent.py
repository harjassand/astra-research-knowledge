#!/usr/bin/env python3
"""Independent rational negative controls and different Taylor recurrence."""
from copy import deepcopy
from fractions import Fraction as R
import importlib.util
import json
from pathlib import Path
import sys
import independent_check as ic


def exact_implicit_coefficients(x,z,N):
    # Repeatedly extract coefficient n from 2*w(h)^2*s'(h)=1.
    # This does not use the reciprocal-series recurrence in either solver.
    c=[z]
    for n in range(N):
        w=[c[k]+(R(3,4)*[x*x,2*x,R(1)][k] if k<3 else 0) for k in range(n+1)]
        square=[sum((w[j]*w[k-j] for j in range(k+1)),R(0)) for k in range(n+1)]
        c.append((R(1,2) if n==0 else -sum((square[j]*(n-j+1)*c[n-j+1] for j in range(1,n+1)),R(0)))/((n+1)*square[0]))
    return c


def derivative_checks():
    # Test all Taylor coefficients through 13 at rational interior/edge points
    # of broad positive rectangles; a formula-level induction is in RECEIPT.md.
    rectangles=[(R(1,12),R(1,10),R(1,2),R(51,100)),
                (R(1),R(5,4),R(3,4),R(5,4)),
                (R(10),R(11),R(1),R(6,5)),
                (R(255),R(256),R(1),R(6,5))]
    n=0
    for xa,xb,za,zb in rectangles:
        box_coeff=ic.series(ic.Box(xa,xb),ic.Box(za,zb),13)
        for x in (xa,(xa+xb)/2,xb):
            for z in (za,(za+zb)/2,zb):
                exact=exact_implicit_coefficients(x,z,13)
                point_coeff=ic.series(ic.Box(x),ic.Box(z),13)
                for a,b,v in zip(box_coeff,point_coeff,exact):
                    assert a.contains(v) and b.contains(v)
                    n+=1
    return n


def rounding_checks():
    points=[R(n,d) for d in (1,3,7,11) for n in range(-4,5)]
    checked=0
    for x in points:
        for y in points:
            a,b=ic.Box(x-R(1,37),x+R(1,41)),ic.Box(y-R(1,43),y+R(1,47))
            assert (a+b).contains(x+y)
            assert (a*b).contains(x*y)
            if b.lower>0 or b.upper<0:
                assert (a/b).contains(x/y)
            checked+=1
    for a,b in ((-1,1),(0,1),(-1,0),(0,0)):
        try: ic.Box(a,b).inv()
        except AssertionError: pass
        else: raise AssertionError('accepted reciprocal through zero')
    return checked


def negative_controls(data,replayed):
    mutations={
        'lower_endpoint_plus_one':('s_star_lower',str(R(data['s_star_lower'])+1)),
        'upper_endpoint_minus_one':('s_star_upper',str(R(data['s_star_upper'])-1)),
        'inward_lower_decimal':('s_star_decimal_outward',[data['s_star_decimal_outward'][1],data['s_star_decimal_outward'][1]]),
        'omitted_tail':('s_star_upper',data['s_at_E_upper']),
        'wrong_operation_count':('integer_interval_operations',dict(data['integer_interval_operations'],mul=0)),
        'wrong_startup':('startup',dict(data['startup'],forward_e_lower='0')),
        'wrong_grid_precision':('bits',119),
    }
    rejected=[]
    for name,(field,bad) in mutations.items():
        modified=deepcopy(data);modified[field]=bad
        if all(modified.get(k)==v for k,v in replayed.items()):
            raise AssertionError('missed mutation: '+name)
        rejected.append(name)
    bad=deepcopy(data);bad['checkpoints'][0]['s_lower']='0'
    assert bad['checkpoints']!=replayed['checkpoints']
    rejected.append('wrong_first_checkpoint')
    # Exact separation certifies that omitting the tail is genuinely wrong,
    # not merely a failure to match a textual field.
    assert R(data['s_at_E_upper'])<R(data['s_star_lower'])
    return rejected


def main():
    directory=Path(sys.argv[1])
    data=json.loads((directory/'CERTIFICATE_FINE.json').read_text())
    replayed,extra=ic.compute(data['taylor_order'],data['grid_power'],R(data['terminal_e']),data['startup']['polynomial_degree'])
    assert all(data.get(k)==v for k,v in replayed.items())
    negatives=negative_controls(data,replayed)
    nder=derivative_checks()
    narith=rounding_checks()
    result={'status':'PASS','alternative_implicit_recurrence_coefficient_checks':nder,
       'rational_rounding_test_pairs':narith,'zero_containing_reciprocals_rejected':4,
       'certificate_mutations_rejected':negatives,'omitting_tail_is_disjoint_from_valid_enclosure':True,
       'exact_tail_omission_separation':str(R(data['s_star_lower'])-R(data['s_at_E_upper']))}
    output=Path(__file__).with_name('INDEPENDENT_TEST_RESULTS.json')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
