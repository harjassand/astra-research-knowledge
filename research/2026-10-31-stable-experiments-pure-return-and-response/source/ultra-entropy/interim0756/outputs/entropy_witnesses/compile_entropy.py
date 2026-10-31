#!/usr/bin/env python3
"""Propose a full predictive-flow entropy dual, then certify every column.

The input word law supplies acquisition-dependent information. A proposed
dual must be frozen or its same-record selection cost must be charged before
using it for inference. Solver status is not a certificate.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
import argparse
import json
import sys
import time

import numpy as np
import cvxpy as cp

from entropy_cone import prepare,normalization
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'predictive_flow'))
from flow_grid import geometry,prefix,word_feature


def compile_certificate(source,mesh,max_states=100,bits=20):
    start=time.perf_counter()
    s,L=source['alphabet_size'],source['depth']
    leaves,nodes,descriptors,words=geometry(s,L,mesh,max_states)
    p=list(map(Q,source['probabilities']));n,d=len(nodes),len(descriptors)
    assert len(p)==len(words) and min(p)>=0 and sum(p)==1
    J=cp.Variable((n,n),nonneg=True)
    row,col=cp.sum(J,axis=1),cp.sum(J,axis=0)
    balance=row==col;norm=cp.sum(J)==1
    constraints=[balance,norm];row_constraints=[]
    for side in (0,1):
        for b in range(s):
            for w in [w for length in range(L) for w in product(range(s),repeat=length)]:
                next_f=np.array([float(prefix(node,side,w,leaves,mesh)) if node[0]==b else 0. for node in nodes])
                current=np.array([float(prefix(node,side,(b,)+w,leaves,mesh)) for node in nodes])
                mass=row if side==0 else col
                residual=(J if side==0 else J.T)@next_f-cp.multiply(mass,current)
                for sign in (1,-1):
                    constraint=sign*residual-mass/mesh<=0
                    constraints.append(constraint);row_constraints.append(constraint)
    F=np.array([[float(word_feature(node,w,leaves,L,mesh)) for node in nodes] for w in words])
    data=F@row==np.array(list(map(float,p)));constraints.append(data)
    epi=cp.Variable((n,n));cone=cp.ExpCone(-epi,J,J.T)
    problem=cp.Problem(cp.Minimize(cp.sum(epi)),constraints+[cone])
    value=problem.solve(solver='CLARABEL',max_iter=200,tol_gap_abs=1e-8,tol_gap_rel=1e-8,tol_feas=1e-8)
    result={'scope':__doc__,'alphabet_size':s,'depth':L,'mesh':mesh,
        'grid_states':n,'flow_variables':n*n,'input_probabilities':list(map(str,p)),
        'solver_status':problem.status,'raw_objective':float(value),
        'conjugate_bits':bits,'backward_residual_marginal':'column; equal to row on stationary flows'}
    result['conjugate_root_method']='dyadic_initial_bracket'
    if data.dual_value is None or balance.dual_value is None or any(c.dual_value is None for c in row_constraints):
        result.update(status='NO_DUAL_PROPOSAL',seconds=time.perf_counter()-start)
        return result
    rat=lambda x:Q(str(float(x))).limit_denominator(10**5)
    a=[-rat(x) for x in data.dual_value]
    potential=[-rat(x) for x in balance.dual_value]
    gauge=potential[0];potential=[x-gauge for x in potential]
    y=[Q(0)]*(n*d)
    assert len(row_constraints)==d
    for r,c in enumerate(row_constraints):
        for i,x in enumerate(c.dual_value):y[i*d+r]=min(Q(0),-rat(x))
    result.update(word_coefficients=list(map(str,a)),state_potential=list(map(str,potential)),
                  row_duals=list(map(str,y)))
    prepared=prepare(result,max_states)
    checked=normalization(prepared,bits)
    z=checked['z'];lower=z+sum((x*prob for x,prob in zip(a,p)),Q(0))
    result.update(normalization_dual=str(z),word_statistic=list(map(str,[z+x for x in a])),
        exact_lower_bound=str(lower),lower_preview=float(lower),
        exact_columns_checked=checked['columns'],distinct_conjugate_arguments=checked['distinct_conjugate_arguments'],
        status='EXACT_POSITIVE_ENTROPY_DUAL' if lower>0 else 'EXACT_DUAL_WITHOUT_POSITIVE_SOURCE_BOUND',
        seconds=time.perf_counter()-start)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path);p.add_argument('--mesh',type=int,default=6)
    p.add_argument('--max-states',type=int,default=100);p.add_argument('--bits',type=int,default=20)
    p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    result=compile_certificate(json.loads(args.input.read_text()),args.mesh,args.max_states,args.bits)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in
        ['scope','input_probabilities','word_coefficients','state_potential','row_duals','word_statistic']},indent=2))


if __name__=='__main__':main()
