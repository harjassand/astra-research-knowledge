"""Exact transfer of a tracial functional through regular recompression.

The acquired matrices are in nonorthonormal coordinates. This checks that the
physical G-adjoint, rather than a plain transpose, is used for the regular metric.
No source actions are needed after the supplied finite representation is fixed.
"""
from fractions import Fraction as F
from pathlib import Path
import sys
import json
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'planning_agent'))
from check_cyclic_exact import eye, transpose, mm, add, scale, cols, inverse, rank, solve_columns, rational_task
from check_centre_exact import algebra_basis, trace


def run():
    # Two inequivalent components M_2 tensor I_3 and C tensor I_2: N=8,d=5.
    n=8
    A1=eye(n)
    for i in range(3,6): A1[i][i]=F(-1)
    A1[6][6]=A1[7][7]=F(2)
    A2=[[F(0)]*n for _ in range(n)]
    for i in range(3): A2[i][i+3]=A2[i+3][i]=F(1)
    A2[6][6]=A2[7][7]=F(3)
    P=eye(n)
    for i in range(n-1): P[i][i+1]=F(i+1,7)
    Pinv=inverse(P)
    G=mm(transpose(P),P)
    Ginv=inverse(G)
    C=[mm(mm(Pinv,A),P) for A in (A1,A2)]
    basis=algebra_basis(C)
    d=len(basis)
    assert d==5
    assert any(X!=transpose(X) for X in C)
    for X in C: assert mm(G,X)==mm(transpose(X),G)
    flat=[sum(X,[]) for X in basis]
    e=solve_columns(flat,sum(eye(n),[]))
    left=[cols([solve_columns(flat,sum(mm(X,B),[])) for B in basis]) for X in C]
    adj=[mm(mm(Ginv,transpose(B)),G) for B in basis]
    H=[[trace(mm(Ba,B)) for B in basis] for Ba in adj]
    assert H==transpose(H) and rank(transpose(H))==d
    for L in left: assert mm(H,L)==mm(transpose(L),H)

    # A strictly positive central weight, transferred without ambient access.
    weight=eye(n)
    for i in range(6): weight[i][i]=F(7,3)
    for i in (6,7): weight[i][i]=F(5,2)
    weight=mm(mm(Pinv,weight),P)
    functional=[trace(mm(weight,B)) for B in basis]
    original_task=rational_task(*C)
    regular_task=rational_task(*left)
    coefficients=[r[0] for r in mm(regular_task,cols([e]))]
    reconstruction=scale(F(0),basis[0])
    for c,B in zip(coefficients,basis): reconstruction=add(reconstruction,scale(c,B))
    assert reconstruction==original_task
    direct=trace(mm(weight,original_task))
    retained=sum(f*x for f,x in zip(functional,coefficients))
    assert direct==retained
    return {'status':'exact_regular_trace_transfer_passed','input_dimension':n,
            'regular_dimension':d,'metric_rank':rank(transpose(H)),
            'nonorthonormal_input_metric':True,'additional_source_actions':0,
            'direct_trace':str(direct),'retained_trace':str(retained),
            'qualification':'Finite exact mechanism check; regular representation is established mathematics.'}


if __name__=='__main__':
    result=run()
    Path(__file__).with_name('regular_trace_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
