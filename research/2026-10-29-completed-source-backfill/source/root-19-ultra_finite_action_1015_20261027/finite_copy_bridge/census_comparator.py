#!/usr/bin/env python3
"""Ordinary sequential exact-N census: zero-error autonomous action comparator.

It receives strictly MORE input knowledge than an upper-bound-only controller:
the exact number of fresh tokens is known. No claim of a new algorithm.
"""
from collections import deque
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib,json,math

HERE=Path(__file__).resolve().parent


def compile_census(n):
    assert n>=1
    leaders=[f'L_{j}_{d}' for j in range(n) for d in range(-j,j+1)]
    rules=[]
    for j in range(n):
        for d in range(-j,j+1):
            for token,step in [('A',1),('B',-1),('S',0)]:
                nxt=(f'L_{j+1}_{d+step}' if j+1<n
                     else 'ACTION_YES' if d+step>0 else 'ACTION_NO')
                rules.append({'reactants':[f'L_{j}_{d}',token],
                              'products':[nxt,'SPENT']})
    assert len(leaders)==n*n and len(rules)==3*n*n
    return {'exact_fresh_token_count_REQUIRED':n,
            'input_species':['A','B','S'],
            'initial_context':{'L_0_0':1},
            'species':['A','B','S','SPENT']+leaders+['ACTION_YES','ACTION_NO'],
            'reactions':rules,'exact_updates_until_action':n,
            'leader_states':n*n+2,'all_species':n*n+6,
            'logical_error':'0 for every finite input with exactly N tokens and all positive rates',
            'acquisition':'Exact N is supplied, never inferred from a timer or free concentration readout'}


def exact_mean(a,b,s,volume):
    n=a+b+s
    @lru_cache(None)
    def rec(x,y,z):
        left=x+y+z
        j=n-left;d=(a-x)-(b-y)
        assert -j<=d<=j
        if not left:
            assert (d>0)==(a>b)
            return F(0)
        # Unit rate constants: total rate is left/volume in every configuration.
        out=F(volume,left)
        for q,(xx,yy,zz) in [(x,(x-1,y,z)),(y,(x,y-1,z)),(z,(x,y,z-1))]:
            if q:out+=F(q,left)*rec(xx,yy,zz)
        return out
    t=rec(a,b,s)
    harmonic=sum((F(1,j) for j in range(1,n+1)),F(0))
    assert t==volume*harmonic
    return t,rec.cache_info().currsize


def main():
    n=9;V=9;eps=.05
    spec=compile_census(n)
    checks=[]
    for a,b,s in [(2,2,5),(3,2,4),(2,3,4),(0,0,9),(9,0,0)]:
        mean,states=exact_mean(a,b,s,V)
        checks.append({'a':a,'b':b,'neutral':s,'mean_time_exact':str(mean),
                       'mean_time_decimal':float(mean),'exact_recursion_states':states,
                       'deadline_failure_at_most_epsilon':V*math.log(n/eps)})
    r={'status':'ORDINARY_EXACT_POPULATION_CENSUS_CONSTRUCTED',
       'same_local_pair_access_but_stronger_exact_N_knowledge':True,
       'spec':spec,'checks':checks,
       'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'physical_device_and_energy':'NOT_ACQUIRED'}
    (HERE/'CENSUS_RESULTS.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='spec'},indent=2))


if __name__=='__main__':main()
