#!/usr/bin/env python3
"""Independent exact final-scope audit. No experimental data are used."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sympy as sp

BASE=Path(__file__).resolve().parent
checks={}

def check(name, value):
    checks[name]=bool(value)
    if not value: raise AssertionError(name)

def box_slice_vertices(w,f,squared_floor):
    """Independent vertex enumeration, not the root water-filling algorithm."""
    lo=list(w);hi=[x/squared_floor for x in w];ans=set()
    n=len(w)
    for free in range(n):
        rest=[k for k in range(n) if k!=free]
        for choices in product([0,1],repeat=n-1):
            m=[F(0)]*n
            for k,c in zip(rest,choices):m[k]=(lo,hi)[c][k]
            m[free]=f-sum(m)
            if all(lo[k]<=m[k]<=hi[k] for k in range(n)):
                ans.add(tuple(m))
    return sorted(ans)

def main():
    ex=sp.Matrix([1,0,0]);ey=sp.Matrix([0,1,0])
    volumes=[sp.Rational(1,2)]*2
    axes=[ex,ey]
    orders=[[sp.Rational(4,5),sp.Rational(2,5)],
            [sp.Rational(2,5),sp.Rational(4,5)]]
    Ms=[];Ws=[]
    for arm in orders:
        Ms.append(sum((v*n*n.T for v,n in zip(volumes,axes)),sp.zeros(3)))
        Ws.append(sum((v*S*S*n*n.T for v,S,n in zip(volumes,arm,axes)),sp.zeros(3)))
    check('independent_domain_sums_M_equal',Ms[0]==Ms[1]==sp.diag(sp.Rational(1,2),sp.Rational(1,2),0))
    check('independent_domain_sums_W_match',Ws[0]==sp.diag(sp.Rational(8,25),sp.Rational(2,25),0) and Ws[1]==sp.diag(sp.Rational(2,25),sp.Rational(8,25),0))
    difference=(Ws[0][0,0]-Ws[0][1,1])/sp.trace(Ws[0])-(Ws[1][0,0]-Ws[1][1,1])/sp.trace(Ws[1])
    check('normalized_false_positive_exact',difference==sp.Rational(6,5))
    results=[]
    for w in [[F(8,25),F(2,25),F(0)],[F(2,25),F(8,25),F(0)]]:
        vertices=box_slice_vertices(w,F(1),F(4,25))
        values=[m[0]-m[1] for m in vertices]
        results.append({'lower':str(min(values)),'upper':str(max(values)),
                        'vertices':[[str(x) for x in m] for m in vertices]})
    check('independent_box_vertex_bounds',[(x['lower'],x['upper']) for x in results]==[('0','21/25'),('-21/25','0')])
    lo=F(results[0]['lower'])-F(results[1]['upper'])
    hi=F(results[0]['upper'])-F(results[1]['lower'])
    check('independent_contrast_difference_bounds',(lo,hi)==(F(0),F(42,25)))
    check('all_extrema_keep_zero_z_volume',all(F(v[2])==0 for r in results for v in r['vertices']))

    # Fixed-W singular fiber is closed; broader zero-order set is joint closure.
    W=sp.diag(1,0,0);M_bad=sp.diag(1,1,0);M_exact=sp.diag(2,0,0)
    check('fixed_W_equal_kernel_example',W.nullspace()==M_exact.nullspace())
    check('broader_point_not_equal_kernel',W.nullspace()!=M_bad.nullspace())
    check('both_candidate_volumes_two',sp.trace(M_bad)==sp.trace(M_exact)==2)
    check('broader_point_positive_distance_from_fixed_fiber',sum(x*x for x in M_bad-M_exact)==2)
    joint=[]
    for eps in [sp.Rational(1,10),sp.Rational(1,100),sp.Rational(1,1000)]:
        W_eps=W+eps*(M_bad-W)
        check(f'joint_approximation_equal_kernel_{eps}',W_eps.nullspace()==M_bad.nullspace())
        check(f'joint_approximation_realized_positive_order_{eps}',W_eps==sp.diag(1,eps,0))
        joint.append({'epsilon':str(eps),'W_diagonal':[str(x) for x in W_eps.diagonal()]})
    check('W_zero_positive_volume_fiber_empty_reason',sp.zeros(3).nullspace()!=sp.diag(1,0,0).nullspace())
    out={'status':'PASS','checks':checks,'count':len(checks),
         'independent_vertex_enumeration':results,
         'difference_bounds':[str(lo),str(hi)],
         'joint_zero_floor_approximations':joint,
         'scope':'Exact mathematical checks only. No acquired W, f, uniform order floor, physical response or same-domain rewrite.'}
    (BASE/'INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
