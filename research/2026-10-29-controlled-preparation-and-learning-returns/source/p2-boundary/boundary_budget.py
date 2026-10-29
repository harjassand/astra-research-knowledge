#!/usr/bin/env python3
"""Exact ordered-edge budget for BOUNDARY_CONTROLLED_RENEWAL.md.

Inputs are certified nonnegative rational edge-norm upper bounds and durations.
The tool does not establish the physical grade, domain, or fresh-supply premises.
No floating solver is used. Run --self-check or pass --input budget.json.
"""
from fractions import Fraction as F
from math import factorial,isqrt
from pathlib import Path
import argparse,json


def rational(value):
    if isinstance(value,bool) or not isinstance(value,(int,str)):
        raise TypeError('Use integers or rational/decimal strings, not binary floats.')
    result=F(value)
    if result<0: raise ValueError('Durations and norm bounds must be nonnegative.')
    return result


def ordered_bound(segments,order,start_grade=0):
    if not isinstance(order,int) or order<0: raise ValueError('Invalid order')
    if not isinstance(start_grade,int) or not 0<=start_grade<=order:
        raise ValueError('Invalid maximum initially occupied grade')
    depth=order+1-start_grade
    amplitudes=[F(1)]+[F(0)]*depth
    for segment in segments:
        dt=rational(segment['duration'])
        edges=list(map(rational,segment['edge_bounds']))
        if len(edges)!=order+1: raise ValueError('Need one bound per grade edge, including escape')
        edges=edges[start_grade:]
        # exp(dt L) is a finite polynomial for this lower-shift cascade.
        term=amplitudes[:]; updated=amplitudes[:]; weight=F(1)
        for power in range(1,depth+1):
            term=[F(0)]+[edges[i-1]*term[i-1] for i in range(1,depth+1)]
            weight*=dt/power
            updated=[x+weight*y for x,y in zip(updated,term)]
        amplitudes=updated
    return amplitudes[-1]


def sqrt_upper(integer,decimal_places=12):
    if integer<0 or decimal_places<0: raise ValueError('Invalid square-root input')
    scale=10**decimal_places
    radicand=integer*scale*scale
    root=isqrt(radicand)
    if root*root<radicand: root+=1
    upper=F(root,scale)
    assert upper*upper>=integer
    return upper


def bosonic_edge_upper(order,coupling_norm_sum,decimal_places=12):
    """Outward rational version of [sqrt(N+q)+sqrt(N+q+1)] sum||C||."""
    if not isinstance(order,int) or order<1: raise ValueError('Bosonic family needs q>=1')
    n=(order+1)**2
    return (sqrt_upper(n+order,decimal_places)+sqrt_upper(n+order+1,decimal_places))*rational(coupling_norm_sum)


def workload(payload):
    results=[]; total=F(0)
    for index,lifetime in enumerate(payload['lifetimes']):
        initial=lifetime.get('max_initial_grade',0)
        bound=ordered_bound(lifetime['segments'],lifetime['order'],initial)
        total+=bound
        results.append({'lifetime':index,'order':lifetime['order'],
                        'max_initial_grade':initial,
                        'complete_isometry_bound':str(bound),
                        'complete_half_diamond_upper_bound':str(min(F(1),bound))})
    return {'scope':'Bounded-edge comparison at supplied physical premises; not a device fault rate.',
            'arithmetic':'exact rational; solver error zero for the supplied piecewise-constant upper bounds',
            'lifetimes':results,'sum_before_cap':str(total),
            'complete_workload_half_diamond_upper_bound':str(min(F(1),total))}


def self_check():
    constant_cases=0
    for q in range(8):
        edges=[F(r+1,r+3) for r in range(q+1)]
        duration=F(3,7)
        segments=[{'duration':str(duration),'edge_bounds':list(map(str,edges))}]
        product=F(1)
        for edge in edges: product*=edge
        assert ordered_bound(segments,q)==product*duration**(q+1)/factorial(q+1)
        constant_cases+=1
    forward=[{'duration':'1','edge_bounds':['1','0']},
             {'duration':'1','edge_bounds':['0','1']}]
    reverse=list(reversed(forward))
    assert ordered_bound(forward,1)==1
    assert ordered_bound(reverse,1)==0
    # Product of the two separate integrated bounds divided by 2! is invalid.
    assert ordered_bound(forward,1)>F(1,2)
    uniform=[{'duration':'1/10','edge_bounds':['1','1','1']}]
    fresh=ordered_bound(uniform,2)
    occupied=ordered_bound(uniform,2,2)
    assert fresh==F(1,6000) and occupied==F(1,10)
    # Subdividing a constant contact is exactly the same calculation.
    split=[{'duration':'1/20','edge_bounds':['1','1','1']}]*2
    assert ordered_bound(split,2)==fresh
    root_cases=0
    for integer in range(101):
        u=sqrt_upper(integer,6)
        assert u*u>=integer
        if u: assert (u-F(1,10**6))**2<integer
        root_cases+=1
    try: rational(0.1)
    except TypeError: pass
    else: raise AssertionError('Unqualified binary float input accepted')
    result={'status':'PASS','constant_profile_cases':constant_cases,
            'exact_time_order_positive':'1','reversed_order_exact_bound':'0',
            'separate_integrated_edge_factorial_negative':'1 > 1/2',
            'fresh_order_two_bound':str(fresh),
            'occupied_final_grade_bound':str(occupied),
            'outward_square_root_cases':root_cases,
            'scope':'Author check of an exact budget calculator; physical premises separately proved/reviewed.'}
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--self-check',action='store_true')
    args=parser.parse_args()
    if args.self_check: result=self_check()
    elif args.input: result=workload(json.loads(args.input.read_text()))
    else: parser.error('Choose --self-check or --input')
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output: args.output.write_text(text)
    print(text,end='')


if __name__=='__main__':main()
