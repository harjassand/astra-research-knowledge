#!/usr/bin/env python3
"""Propose and exactly check a capped common-generator entropy certificate.

Population input: an explicitly supplied Poisson-inspection word law.
Finite observations need their own valid probability intervals/preparations.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
import argparse
import json
import sys
import time

import cvxpy as cp
import numpy as np

from flow import prepare,normalization
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'predictive_flow'))
from flow_grid import geometry,prefix,word_feature


def compile_certificate(source,mesh=3,max_states=100,bits=24):
    start=time.perf_counter();s,L=source['alphabet_size'],source['depth']
    cap,clock=Q(source['kinetic_cap']),Q(source['inspection_rate'])
    leaves,nodes,descriptors,words=geometry(s,L,mesh,max_states);n,d=len(nodes),len(descriptors)
    probabilities=list(map(Q,source['probabilities']));J=cp.Variable((n,n),nonneg=True)
    row,col=cp.sum(J,axis=1),cp.sum(J,axis=0);balance=row==col;normal=cp.sum(J)==1
    constraints=[balance,normal];directed=[]
    for side,b,w,sign in descriptors:
        next_value=np.array([float(prefix(node,side,(b,)+w,leaves,mesh)) for node in nodes])
        current=np.array([float((cap+clock)*prefix(node,side,(b,)+w,leaves,mesh)
                          -(clock*prefix(node,side,w,leaves,mesh) if node[0]==b else 0)) for node in nodes])
        mass=row if side==0 else col
        residual=float(cap)*(J if side==0 else J.T)@next_value-cp.multiply(mass,current)
        delta=float((cap+clock+(clock if w else 0))/mesh)
        bound=sign*residual-delta*mass<=0;constraints.append(bound);directed.append(bound)
    F=np.array([[float(word_feature(node,w,leaves,L,mesh)) for node in nodes] for w in words])
    data=F@row==np.array(list(map(float,probabilities)));constraints.append(data)
    epi=cp.Variable((n,n));cone=cp.ExpCone(-epi,J,J.T)
    problem=cp.Problem(cp.Minimize(float(cap)*cp.sum(epi)),constraints+[cone])
    value=problem.solve(solver='CLARABEL',max_iter=150,tol_gap_abs=1e-8,tol_gap_rel=1e-8,tol_feas=1e-8)
    result={'scope':__doc__,'alphabet_size':s,'depth':L,'mesh':mesh,
            'kinetic_cap':str(cap),'inspection_rate':str(clock),
            'predictive_grid_nodes':n,'flow_variables':n*n,
            'input_probabilities':list(map(str,probabilities)),
            'numerical_status':problem.status,'raw_objective':float(value),
            'conjugate_bits':bits,'input_status':'supplied exact-law mathematical fixture; no sample acquisition'}
    if data.dual_value is None or balance.dual_value is None or any(c.dual_value is None for c in directed):
        result.update(status='NO_DUAL_PROPOSAL',seconds=time.perf_counter()-start);return result
    rat=lambda x:Q(str(float(x))).limit_denominator(10**5)
    a=[-rat(x) for x in data.dual_value];potential=[-rat(x) for x in balance.dual_value]
    gauge=potential[0];potential=[x-gauge for x in potential];y=[Q(0)]*(n*d)
    for r,bound in enumerate(directed):
        for i,value in enumerate(bound.dual_value):y[i*d+r]=min(Q(0),-rat(value))
    result.update(word_coefficients=list(map(str,a)),state_potential=list(map(str,potential)),row_duals=list(map(str,y)))
    check=normalization(prepare(result,max_states),bits);z=check['z']
    lower=z+sum((x*p for x,p in zip(a,probabilities)),Q(0))
    result.update(normalization_dual=str(z),exact_lower_bound=str(lower),lower_preview=float(lower),
                  exact_columns_checked=check['columns'],distinct_conjugates=check['distinct_conjugates'],
                  status='EXACT_POSITIVE_COHERENT_CERTIFICATE' if lower>0 else 'EXACT_CERTIFICATE_WITHOUT_POSITIVE_BOUND',
                  seconds=time.perf_counter()-start)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--mesh',type=int,default=3);p.add_argument('--max-states',type=int,default=100)
    args=p.parse_args();result=compile_certificate(json.loads(args.input.read_text()),args.mesh,args.max_states)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['scope','word_coefficients','row_duals','state_potential','input_probabilities']},indent=2))


if __name__=='__main__':main()
