#!/usr/bin/env python3
"""Capped near-identity roots: actual generator, exact cost and word error."""
from fractions import Fraction as Q
from pathlib import Path
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1];HERE=ROOT/'outputs/coherent_generator'
sys.path.insert(0,str(ROOT/'work'))
from coherent_generator_control import identity,mm,source_model
from ctmc_reflection_control import exp_negative_bounds


def mpow(A,n):
    out=identity(len(A))
    while n:
        if n%2:out=mm(out,A)
        A=mm(A,A);n//=2
    return out


def main():
    start=time.perf_counter();P,pi,labels=source_model();n=len(P);I=identity(n)
    # Physical Delta=Lambda=1, so the semigroup is exp(P-I).
    order=80;power=I;weight=Q(1);total=[[Q(0)]*n for _ in range(n)];mass=Q(0)
    for k in range(order+1):
        mass+=weight
        total=[[total[i][j]+weight*power[i][j] for j in range(n)] for i in range(n)]
        power=mm(power,P);weight/=k+1
    el,eu=exp_negative_bounds(Q(1),160);tail=1-el*mass
    low=[[el*x for x in row] for row in total]
    high=[[eu*x+tail for x in row] for row in total]
    results=[]
    for m in (2,4,8,16,32,64,128):
        h=Q(1,m);R=[[(1-h)*I[i][j]+h*P[i][j] for j in range(n)] for i in range(n)]
        generator=[[(R[i][j]-I[i][j])/h for j in range(n)] for i in range(n)]
        assert generator==[[P[i][j]-I[i][j] for j in range(n)] for i in range(n)]
        assert all(R[i][i]>=1-h for i in range(n))
        # Reciprocal flows, and each exact entropy contribution, scale by h.
        pair_checks=0
        for i in range(n):
            for j in range(i+1,n):
                x,y=pi[i]*R[i][j],pi[j]*R[j][i]
                u,v=pi[i]*P[i][j],pi[j]*P[j][i]
                assert (x,y)==(h*u,h*v)
                if u and v:assert x/y==u/v
                pair_checks+=1
        coarse=mpow(R,m)
        upper=max(sum(max(abs(coarse[i][j]-low[i][j]),abs(coarse[i][j]-high[i][j]))
                      for j in range(n))/2 for i in range(n))
        assert upper<=Q(1,m)
        results.append({'fine_root_steps':m,'fine_spacing':str(h),
                        'same_actual_generator_exact':True,'exact_entropy_scaling_pair_checks':pair_checks,
                        'coarse_kernel_TV_upper':float(upper),'general_TV_bound':str(Q(1,m)),
                        'length_5_word_TV_upper_by_coupling':float(min(Q(1),4*upper))})
    data={'status':'CAPPED_ROOT_TO_GENERATOR_CONTROLS_PASSED','maximum_escape_rate':'1',
          'coarse_spacing':'1','fixture_hidden_states':n,'new_acquisitions':0,
          'semigroup_uniformization_truncation_order':order,'Poisson_tail_upper':float(tail),
          'roots':results,'elapsed_wall_seconds':time.perf_counter()-start,
          'scope':'algebra and finite fixture; population convergence proof in ROOT_LIMIT.txt',
          'no_generic_cost_convergence_rate_claimed':True}
    (HERE/'root_limit_receipt.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))


if __name__=='__main__':main()
